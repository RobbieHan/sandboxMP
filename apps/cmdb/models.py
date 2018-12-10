from django.db import models

# Create your models here.


class AbstractMode(models.Model):
    parent = models.ForeignKey(
        'self', blank=True, null=True, on_delete=models.SET_NULL, related_name='child'
    )

    class Meta:
        abstract = True


class Code(AbstractMode):
    key = models.CharField(max_length=80, verbose_name='键')
    value = models.CharField(max_length=80, verbose_name='值')
    desc = models.BooleanField(default=True, verbose_name='备注')

    class Meta:
        verbose_name = '字典'
        verbose_name_plural = verbose_name
