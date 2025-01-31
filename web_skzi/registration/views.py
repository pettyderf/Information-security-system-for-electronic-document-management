from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, DH_key_exchange, DH_accept_key_exchange, CriptGostForm, DecriptMagmaForm, Create_sig, Check_sig, Create_author, Check_author
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.views.generic.edit import FormView,CreateView

from .models import Gost_key_user, DH_key, Uploade_file_on_signature
##########################
from algoritms.GOST import gen_key_gost, cript_gost, encript_gost, magma_cript, magma_encript
from algoritms.GOST_EP import gost_ep_keys, DS_gost, check_gost_ep
from algoritms.LSBM import Encode_LSBM, Decode
import hashlib
from transliterate import translit
import os
import random
from sympy import *
##########################

def index(request):
    return render(request, 'registration/index.html')

def check_author(request):
    if request.method == 'POST':
        form = Check_author(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if str(file)[-4:] == ".bmp":
                ansver = Decode(request.FILES['file'])
                return render(request, "registration/verified-author.html", {'ansver': ansver})
            else:
                ansver = 'Неподходящие параметры: убедитесь, что загружаемый вами файл имеет разсширение - .bmp'
                return render(request, 'registration/invalid-pic.html', {'ansver': ansver})
    else:
        form = Check_author()
    return render(request, 'registration/check-author.html', {'form': form})

def create_author(request):
    if request.method == 'POST':
        form = Create_author(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            if check_password(cd['password'], request.user.password):
                file = request.FILES['file']
                if str(file)[-4:] == ".bmp":
                    file_name = str(file)[:-4] + "_authorship.bmp"
                    message = "Author - " + translit(str(request.user.last_name), language_code='ru', reversed=True) + " " + translit(str(request.user.first_name), language_code='ru', reversed=True)
                    new_pic = Encode_LSBM(request.FILES['file'], message)
                    if new_pic == "big message":
                        ansver = 'Неподходящие параметры: Картинка слишком мала, чтобы добавить авторство.'
                        return render(request, 'registration/invalid-pic.html', {'ansver': ansver})

                    new_pic.save('files/' + str(file)[:-4] + "_authorship.bmp", format="BMP")

                    spot = translit(file_name, language_code='ru', reversed=True)

                    with open('files/' + file_name, 'rb') as file_open:
                        response = HttpResponse(file_open.read(), content_type='application/octet-stream')
                        response['Content-Disposition'] = f"attachment; filename={spot}"
                    os.remove('files/' + file_name)
                    return response

                else:
                    ansver = 'Неподходящие параметры: убедитесь, что загружаемый вами файл имеет разсширение - .bmp'
                    return render(request, 'registration/invalid-pic.html', {'ansver': ansver})

            else:
                ansver = "Неверный пароль"
                return render(request, 'registration/invalid-pass.html', {'ansver': ansver})
    else:
        form = Create_author()
    return render(request, 'registration/create-author.html', {'form': form})



def create_sig(request):
    if request.method == 'POST':
        form = Create_sig(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            if check_password(cd['password'], request.user.password):
                file = request.FILES['file']
                file_hash = hashlib.sha256()
                for chunk in file.chunks():
                    file_hash.update(chunk)
                hash_on = file_hash.hexdigest()
                user_keys = Gost_key_user.objects.all()
                for i in user_keys:
                    if str(i.title) == str(request.user.username):
                        q = i.gost_q
                        p = i.gost_p
                        a = i.gost_a
                        x = i.gost_secretkey
                        new_x = int(encript_gost(x, gen_key_gost(request.user.username, cd['password'])))
                        EP = DS_gost(str(hash_on),q,p,a,new_x)

                        #Создаем файл sig
                        file_name = str(file)[:-4] + '.sig'
                        file_sig = open('files/' + file_name, 'w')
                        file_sig.write(EP)
                        file_sig.close()
                        spot = translit(file_name, language_code='ru', reversed=True)


                        with open('files/' + file_name, 'rb') as file_open:
                            response = HttpResponse(file_open.read(), content_type='application/octet-stream')
                            response['Content-Disposition'] = f"attachment; filename={spot}"
                        os.remove('files/' + file_name)
                        return response

            else:
                ansver = "Неверный пароль"
                return render(request, 'registration/invalid-pass.html', {'ansver': ansver})
    else:
        form = Create_sig()
    return render(request, 'registration/create_sig.html', {'form': form})

def checking_sig(request):
    if request.method == 'POST':
        form = Check_sig(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            user_keys = Gost_key_user.objects.all()

            # получаем хэш файла
            file = request.FILES['file']
            file_hash = hashlib.sha256()
            for chunk in file.chunks():
                file_hash.update(chunk)
            hash_on = file_hash.hexdigest()

            # получаем r,s из файла sig
            EP_file = request.FILES['signature']
            EP = str(EP_file.read().decode('utf-8'))
            RS = EP.split()
            r = str(RS[0])
            s = str(RS[1])

            for i in user_keys:
                if str(i.title) == str(cd['user_tag']):
                    q = i.gost_q
                    p = i.gost_p
                    a = i.gost_a
                    y = i.gost_openkey
                    ansver = check_gost_ep(hash_on, r, s, q, p, a, y)
                    if ansver:
                        ansver_sig = "Подпись действительна!"
                        return render(request, 'registration/ansver-signature.html', {'ansver_sig': ansver_sig})
                    else:
                        ansver_sig = "Подпись НЕ действительна!"
                        return render(request, 'registration/ansver-signature.html', {'ansver_sig': ansver_sig})

            ansver = "Нет такого пользователя"
            return render(request, 'registration/invalid-pass.html', {'ansver': ansver})

    else:
        form = Check_sig()
    return render(request, 'registration/check_sig.html', {'form': form})

def key_exchange(request):
    if request.method == 'POST':
        form = DH_key_exchange(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if check_password(cd['password'], request.user.password):
                if str(cd['user_tag']) == str(request.user.username):
                    ansver = "Вы не можете отправить запрос сами себе"
                    return render(request, 'registration/ansver-key-exchange.html', {'ansver': ansver})

                user_key = DH_key.objects.all()
                for i in user_key:
                    if (str(i.title) == str(cd['user_tag']) and str(i.user_two_id) == str(request.user.username)) or (str(i.title) == str(request.user.username) and str(i.user_two_id) == str(cd['user_tag'])):
                        ansver = "Запрос уже был послан вам или вами"
                        return render(request, 'registration/ansver-key-exchange.html', {'ansver': ansver})
                p = random.randint(100000000000, 1000000000000000000000)
                g = random.randint(3, 30)
                while isprime(p) != True:
                    p = random.randint(100000000000, 1000000000000000000000)
                while isprime(g) != True:
                    g = random.randint(3, 30)
                us_ps = str(request.user.username) + str(cd['password'])
                ok_hash = hashlib.new('sha256')
                ok_hash.update(us_ps.encode())
                ok_hash_line = str(int(str(ok_hash.hexdigest()), 16))[:4]

                user_one_ok = (g ** int(ok_hash_line)) % p

                new_string_for_bd = DH_key(title=request.user.username,
                                                  user_two_id=str(cd['user_tag']),
                                                  dh_g=str(g),
                                                  dh_p=str(p),
                                                  user_one_ok=str(user_one_ok),
                                                  user_two_ok='none')
                new_string_for_bd.save()
                ansver = "Запрос был успешно отправлен, дождитесь пока пользователь примет его"
                return render(request, 'registration/ansver-key-exchange.html', {'ansver': ansver})
            else:
                ansver = "Неверный пароль"
                return render(request, 'registration/invalid-pass.html', {'ansver': ansver})
    else:
        form = DH_key_exchange()
    return render(request, 'registration/key_exchange.html', {'form': form})

def accept_key_exchange(request):
    if request.method == 'POST':
        form = DH_key_exchange(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if check_password(cd['password'], request.user.password):
                user_key = DH_key.objects.all()
                for i in user_key:
                    if str(i.title) == str(cd['user_tag']) and str(i.user_two_id) == str(request.user.username):
                        if str(i.user_two_ok) == 'none':
                            g = int(i.dh_g)
                            p = int(i.dh_p)

                            us_ps = str(request.user.username) + str(cd['password'])
                            ok_hash = hashlib.new('sha256')
                            ok_hash.update(us_ps.encode())
                            ok_hash_line = str(int(str(ok_hash.hexdigest()), 16))[:4]

                            user_two_ok = (g ** int(ok_hash_line)) % p
                            i.user_two_ok = user_two_ok
                            i.save()

                            ansver = "Обмен произведен"
                            return render(request, 'registration/ansver-key-exchange.html', {'ansver': ansver})

                        else:
                            ansver = "Обмен уже был произведен"
                            return render(request, 'registration/ansver-key-exchange.html', {'ansver': ansver})

                    if str(i.title) == str(request.user.username) and str(i.user_two_id) == str(cd['user_tag']):
                        ansver = "Вы уже отправляли запрос этому пользователю, дождитесь пока он его примет"
                        return render(request, 'registration/ansver-key-exchange.html', {'ansver': ansver})

                ansver = "Этот пользователь не отправлял вам запрос"
                return render(request, 'registration/ansver-key-exchange.html', {'ansver': ansver})


            else:
                ansver = "Неверный пароль"
                return render(request, 'registration/invalid-pass.html', {'ansver': ansver})
    else:
        form = DH_accept_key_exchange()
    return render(request, 'registration/accept_key_exchange.html', {'form': form})

def algoritms_cript(request):
    if request.method == 'POST':
        form = CriptGostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if check_password(cd['password'], request.user.password):
                user_keys = DH_key.objects.all()
                for i in user_keys:
                    if str(i.title) == str(cd['user_tag']) and str(i.user_two_id) == str(request.user.username):
                        p = int(i.dh_p)
                        ok = int(i.user_one_ok)
                        us_ps = str(request.user.username) + str(cd['password'])
                        ok_hash = hashlib.new('sha256')
                        ok_hash.update(us_ps.encode())
                        ok_hash_line = str(int(str(ok_hash.hexdigest()), 16))[:4]
                        key_gost = (ok**int(ok_hash_line)) % p

                        close_txt = magma_cript(str(cd['opentext']), gen_key_gost(key_gost,''))

                        file_name = 'close_text.txt'
                        file_shifr = open('files/' + file_name, 'w')
                        file_shifr.write(close_txt)
                        file_shifr.close()

                        with open('files/' + file_name, 'rb') as file_open:
                            response = HttpResponse(file_open.read(), content_type='application/octet-stream')
                            response['Content-Disposition'] = f"attachment; filename={file_name}"
                        os.remove('files/' + file_name)
                        return response

                        # ans = 'Сообщение было зашифровано:'
                        # return render(request, 'registration/ansver-cript-decript.html',
                        #               {'ansver': str(close_txt), 'ans': ans})

                    if str(i.user_two_id) == str(cd['user_tag']) and str(i.title) == str(request.user.username):
                        p = int(i.dh_p)
                        ok = int(i.user_two_ok)
                        us_ps = str(request.user.username) + str(cd['password'])
                        ok_hash = hashlib.new('sha256')
                        ok_hash.update(us_ps.encode())
                        ok_hash_line = str(int(str(ok_hash.hexdigest()), 16))[:4]
                        key_gost = (ok ** int(ok_hash_line)) % p

                        close_txt = magma_cript(str(cd['opentext']), gen_key_gost(key_gost, ''))

                        file_name = 'close_text.txt'
                        file_shifr = open('files/' + file_name, 'w')
                        file_shifr.write(close_txt)
                        file_shifr.close()

                        with open('files/' + file_name, 'rb') as file_open:
                            response = HttpResponse(file_open.read(), content_type='application/octet-stream')
                            response['Content-Disposition'] = f"attachment; filename={file_name}"
                        os.remove('files/' + file_name)
                        return response

                        # ans = 'Сообщение было зашифровано:'
                        # return render(request, 'registration/ansver-cript-decript.html',
                        #               {'ansver': str(close_txt), 'ans': ans})

                ansver = "Вы не обменивались ключами с этим пользователем"
                return render(request, 'registration/ansver-key-exchange.html', {'ansver': ansver})

            else:
                ansver = "Неверный пароль"
                return render(request, 'registration/invalid-pass.html', {'ansver': ansver})

    else:
        form = CriptGostForm()
    return render(request, 'registration/alg_cript.html', {'form': form})

def algoritms_decript(request):
    if request.method == 'POST':
        form = DecriptMagmaForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            if check_password(cd['password'], request.user.password):
                user_keys = DH_key.objects.all()
                close_text_file = request.FILES['file']
                close_text = str(close_text_file.read().decode('utf-8'))
                for i in user_keys:
                    if str(i.title) == str(cd['user_tag']) and str(i.user_two_id) == str(request.user.username):
                        p = int(i.dh_p)
                        ok = int(i.user_one_ok)
                        us_ps = str(request.user.username) + str(cd['password'])
                        ok_hash = hashlib.new('sha256')
                        ok_hash.update(us_ps.encode())
                        ok_hash_line = str(int(str(ok_hash.hexdigest()), 16))[:4]
                        key_gost = (ok ** int(ok_hash_line)) % p

                        open_txt = magma_encript(close_text, gen_key_gost(key_gost, ''))

                        ans = 'Сообщение было расшифровано:'
                        return render(request, 'registration/ansver-cript-decript.html',
                                      {'ansver': str(open_txt), 'ans': ans})

                    if str(i.user_two_id) == str(cd['user_tag']) and str(i.title) == str(request.user.username):
                        p = int(i.dh_p)
                        ok = int(i.user_two_ok)
                        us_ps = str(request.user.username) + str(cd['password'])
                        ok_hash = hashlib.new('sha256')
                        ok_hash.update(us_ps.encode())
                        ok_hash_line = str(int(str(ok_hash.hexdigest()), 16))[:4]
                        key_gost = (ok ** int(ok_hash_line)) % p

                        open_txt = magma_encript(close_text, gen_key_gost(key_gost, ''))

                        ans = 'Сообщение было расшифровано:'
                        return render(request, 'registration/ansver-cript-decript.html',
                                      {'ansver': str(open_txt), 'ans': ans})

                ansver = "Вы не обменивались ключами с этим пользователем"
                return render(request, 'registration/ansver-key-exchange.html', {'ansver': ansver})

            else:
                ansver = "Неверный пароль"
                return render(request, 'registration/invalid-pass.html', {'ansver': ansver})
    else:
        form = DecriptMagmaForm()
    return render(request, 'registration/alg_decript.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect("/")

def log_in(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("/")

                else:
                    return render(request, "registration/disabled_account.html", {'form': form})
            else:
                return render(request, "registration/invalid_login.html", {'form': form})
    else:
        form = LoginForm()
    return render(request, 'registration/log_in.html', {'form': form})

def Register_user(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create EP key's for User
            q, p, a, x, y = gost_ep_keys()
            # Cript closekey EP with GOST
            new_x = cript_gost(x,gen_key_gost(new_user.username, user_form.cleaned_data['password']))
            # Add user key's in BD
            new_string_for_bd = Gost_key_user(title = new_user.username,
                                          gost_q = q,
                                          gost_p = p,
                                          gost_a = a,
                                          gost_openkey = y,
                                          gost_secretkey = new_x)
            new_string_for_bd.save()

            return render(request, "registration/registr_done.html", {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/registr.html', {'user_form': user_form})

def registration_done(request):
    return render(request, "registration/registr_done.html")



