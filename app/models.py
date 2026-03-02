from django.db import models

class App(models.Model):

    nomenclature = models.CharField('Номенклатура', max_length=255)
    unit = models.CharField('Единица', max_length=10)
    quantity = models.PositiveIntegerField('Количество', null=True, blank=True)

    class Meta:
        verbose_name = 'Склад инструмента'
        verbose_name_plural = 'Склад инструментов'

    def __str__(self):
        return f'{self.nomenclature} {self.unit} {self.quantity}'

