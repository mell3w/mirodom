# Generated by Django 3.2.11 on 2022-05-12 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applicationbase', '0006_appliactions_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commnet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=30, verbose_name='Автор')),
                ('content', models.TextField(verbose_name='Содержание')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='Выводить на экран?')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликован')),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='applicationbase.appliactions', verbose_name='Заявка')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ['created_at'],
            },
        ),
    ]
