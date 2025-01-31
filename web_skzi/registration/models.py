from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Gost_key_user(models.Model):
    title = models.CharField('user_id', max_length=50)
    gost_q = models.CharField('gost_q', max_length=250)
    gost_p = models.CharField('gost_p', max_length=250)
    gost_a = models.CharField('gost_a', max_length=250)
    gost_openkey = models.CharField('gost_openkey', max_length=250)
    gost_secretkey = models.CharField('gost_secretkey', max_length=250)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ключи пользователя'
        verbose_name_plural = 'Ключи пользователей'

class DH_key(models.Model):
    title = models.CharField('user_one_id', max_length=50)
    user_two_id = models.CharField('user_two_id', max_length=50)
    dh_g = models.CharField('dh_g', max_length=250)
    dh_p = models.CharField('dh_p', max_length=250)
    user_one_ok = models.CharField('user_one_ok', max_length=250)
    user_two_ok = models.CharField('user_two_ok', max_length=250)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Обмен ключом'
        verbose_name_plural = 'Обмен ключами'

class Uploade_file_on_signature(models.Model):
    title = models.CharField('user_id', max_length=50)
    file = models.FileField(upload_to='files')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Загруженный файл'
        verbose_name_plural = 'Загруженные файлы'