# Generated by Django 4.2.1 on 2023-06-10 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_event_city_alter_user_is_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_valid',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='image',
            field=models.ImageField(blank=True, default='Default/user.png', null=True, upload_to='Client_images'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_client',
            field=models.BooleanField(default=True),
        ),
    ]
