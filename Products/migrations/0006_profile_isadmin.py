# Generated by Django 3.2.3 on 2021-06-19 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0005_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='isAdmin',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]