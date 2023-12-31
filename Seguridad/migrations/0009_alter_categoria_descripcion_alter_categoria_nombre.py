# Generated by Django 4.2.4 on 2023-10-20 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Seguridad', '0008_merge_20231020_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='descripcion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='categoria',
            name='nombre',
            field=models.CharField(error_messages={'unique': 'Ya existe una categoría con este nombre. Por favor, elige otro nombre.'}, max_length=100, unique=True),
        ),
    ]
