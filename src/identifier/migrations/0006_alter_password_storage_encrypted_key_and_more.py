# Generated by Django 4.2.2 on 2023-09-12 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('identifier', '0005_remove_password_storage_login_informations_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='password_storage',
            name='encrypted_key',
            field=models.BinaryField(),
        ),
        migrations.AlterField(
            model_name='password_storage',
            name='nonce',
            field=models.BinaryField(),
        ),
        migrations.AlterField(
            model_name='password_storage',
            name='tag',
            field=models.BinaryField(),
        ),
    ]
