# Generated by Django 3.2.11 on 2022-04-26 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applicationbase', '0004_additionalimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appliactions',
            name='master',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='applicationbase.masters', verbose_name='Мастер'),
        ),
    ]
