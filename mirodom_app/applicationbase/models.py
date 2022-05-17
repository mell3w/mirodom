from django.db import models
from django.contrib.auth.models import AbstractUser
from .utilities import get_timestamp_path



# Create your models here.


class Fine(models.Model):
    reason = models.CharField(max_length=50, verbose_name='Причина штрафа')
    amount = models.FloatField(verbose_name='Сумма штрафа')
    def __str__(self):
        return self.reason

    class Meta:
        verbose_name_plural = 'Штрафы'
        verbose_name = 'Штраф'


class Masters(models.Model):
    full_name = models.CharField(max_length=30, verbose_name='ФИО')
    tel = models.CharField(max_length=15, verbose_name='Телефон')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name_plural = 'Мастера'
        verbose_name = 'Мастер'



class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошел активацию?')
    send_messages = models.BooleanField(default=True, verbose_name='Присылать оповещения о новых комментариях?')

    def delete(self, *args, **kwargs):
        for Appliactions in self.applications_set.all():
            Appliactions.delete()
        super().delete(*args,**kwargs)

    class Meta(AbstractUser.Meta):
        pass


class Appliactions(models.Model):
    status_choice = (
        ('a','В работе'),
        ('b','Нужна сварка'),
        ('c', 'Выполнена')
    )
    master = models.ForeignKey(Masters, verbose_name='Мастер',on_delete=models.PROTECT)
    city = models.CharField(max_length=50, verbose_name='Город')
    address = models.CharField(max_length=20, verbose_name='Адрес')
    flat = models.CharField(max_length=10,null=True, blank=True, verbose_name='Квартира')
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE,
                               verbose_name='Автор заявки')
    full_name_client = models.CharField(max_length=30, null=True, blank=True, verbose_name='ФИО Клиента')
    reason_for_calling = models.TextField(null=True, blank=True, verbose_name='Причина вызова')
    treaty = models.BooleanField(default=False, verbose_name='Договор')
    door_closer = models.BooleanField(default=False, verbose_name='Замена доводчика')
    img_door_closer = models.ImageField(verbose_name='Фото доводчика', upload_to=get_timestamp_path, null=True, blank=True)
    monetary = models.BooleanField(default=False, verbose_name='Денежная заявка')
    sum = models.FloatField(null=True, blank=True, verbose_name='Общая сумма')
    premium = models.FloatField(null=True, blank=True, verbose_name='Премия')
    fine = models.BooleanField(default=False, verbose_name='Штраф')
    choose_fine = models.ForeignKey(Fine, null=True, blank=True, verbose_name='Причины штрафа', on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=True, verbose_name='Комментарий')
    published = models.DateTimeField(auto_now_add=True,db_index=True, verbose_name= 'Дата подачи заявки')
    closing_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20,choices=status_choice, default='a', verbose_name='Статус заявки')
    calcucalted = models.BooleanField(default=False, verbose_name='Деньги сданы')

    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)


    class Meta:
        verbose_name_plural = 'Заявки'
        verbose_name = 'Заявка'
        ordering = ['-published']


class Warehouse(models.Model):
    owner = models.ForeignKey(Masters, on_delete=models.CASCADE, verbose_name='Мастер')
    YKP7 = models.FloatField(null=True, blank=True, verbose_name='УКП-7')
    YKP12 = models.FloatField(null=True, blank=True, verbose_name='УКП-12')
    RF = models.FloatField(null=True, blank=True, verbose_name='RF')
    TM = models.FloatField(null=True, blank=True, verbose_name='TM')
    MD = models.FloatField(null=True, blank=True, verbose_name='MD')
    door_closer = models.FloatField(null=True, blank=True, verbose_name='Доводчик')

    class Meta:
        verbose_name_plural = 'Склад'
        verbose_name = 'Учет склада'


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, unique=True, verbose_name='Название')
    order = models.SmallIntegerField(default=0,db_index=True, verbose_name='Порядок')
    super_rubric = models.ForeignKey('SuperRubric', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Надрубрика')

class SuperRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)

class SuperRubric(Rubric):
    objects = SuperRubricManager()
    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = 'Недорубрика'
        verbose_name_plural = 'Надрубрика'


class SubRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)

class SubRubric(Rubric):
    objects = SubRubricManager()
    def __str__(self):
        return '%s - %s' % (self.super_rubric.name, self.name)

    class Meta:
        proxy = True
        ordering = ('super_rubric__order', 'super_rubric__name', 'order', 'name')
        verbose_name = 'Подрубрика'
        verbose_name_plural = 'Подрубрики'


class AdditionalImage (models.Model):
    Appliactions = models.ForeignKey(Appliactions, on_delete=models.CASCADE, verbose_name='Заявка')
    img_door_closer = models.ImageField(upload_to=get_timestamp_path, verbose_name='Фото доводичка')

    class Meta:
        verbose_name_plural = 'Доп фото доводчика'
        verbose_name = 'Доп фото'

class Commet(models.Model):
    app = models.ForeignKey(Appliactions, on_delete=models.CASCADE, verbose_name='Заявка')
    author = models.CharField(max_length=30, verbose_name='Автор')
    content = models.TextField(verbose_name='Содержание')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Выводить на экран?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликован')

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'
        ordering = ['created_at']

