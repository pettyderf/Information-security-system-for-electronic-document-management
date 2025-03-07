# Generated by Django 3.2.25 on 2024-11-09 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_auto_20241014_1412'),
    ]

    operations = [
        migrations.CreateModel(
            name='DH_key',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='user_one_id')),
                ('user_two_id', models.CharField(max_length=50, verbose_name='user_two_id')),
                ('dh_g', models.CharField(max_length=250, verbose_name='dh_g')),
                ('dh_p', models.CharField(max_length=250, verbose_name='dh_p')),
                ('user_one_ok', models.CharField(max_length=250, verbose_name='user_one_ok')),
                ('user_two_ok', models.CharField(max_length=250, verbose_name='user_two_ok')),
            ],
            options={
                'verbose_name': 'Обмен ключом',
                'verbose_name_plural': 'Обмен ключами',
            },
        ),
    ]
