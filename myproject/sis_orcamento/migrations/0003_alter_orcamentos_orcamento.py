# Generated by Django 5.1 on 2024-10-22 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sis_orcamento', '0002_remove_balancas_numero_serie_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orcamentos',
            name='orcamento',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]