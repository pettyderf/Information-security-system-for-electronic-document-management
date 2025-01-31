from django.contrib import admin
from .models import Gost_key_user, Uploade_file_on_signature, DH_key
# Register your models here.

admin.site.register(Gost_key_user)
admin.site.register(Uploade_file_on_signature)
admin.site.register(DH_key)