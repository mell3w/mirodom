# Generated by Django 3.2.11 on 2022-04-26 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applicationbase', '0005_alter_appliactions_master'),
    ]

    operations = [
        migrations.AddField(
            model_name='appliactions',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='applicationbase.advuser', verbose_name='Автор заявки'),
            preserve_default=False,
        ),
    ]
