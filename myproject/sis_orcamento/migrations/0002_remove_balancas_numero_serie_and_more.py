# Generated by Django 5.1 on 2024-10-22 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sis_orcamento', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='balancas',
            name='numero_serie',
        ),
        migrations.AddField(
            model_name='orcamentos',
            name='num_serie_balanca',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]