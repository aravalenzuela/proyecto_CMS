# Generated by Django 4.2.4 on 2023-11-03 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Gestion_Contenido', '0002_plantilla_predeterminada_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contenidoeditable',
            old_name='contenido',
            new_name='contenidoDePlantilla',
        ),
        migrations.RenameField(
            model_name='plantilla',
            old_name='contenido',
            new_name='contenidoDePlantilla',
        ),
        migrations.RenameField(
            model_name='plantillapredeterminada',
            old_name='contenido',
            new_name='contenidoDePlantilla',
        ),
    ]
