# Generated by Django 4.2.4 on 2023-10-05 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Seguridad', '0003_categoria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rol',
            name='descripcion',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
