# Generated by Django 4.2.2 on 2023-11-24 10:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('identifier', '0006_alter_password_storage_encrypted_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='username',
            name='User_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
