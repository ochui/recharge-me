# Generated by Django 2.2.3 on 2019-07-25 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_remerge'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='can_merge',
            field=models.BooleanField(default=False),
        ),
    ]
