# Generated by Django 4.2.4 on 2023-11-14 22:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Seguridad', '0017_contenido_plantilla'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenido',
            name='comentario',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='contenido',
            name='estado',
            field=models.CharField(choices=[('Borrador', 'Borrador'), ('En Revisión', 'En Revisión'), ('Rechazado', 'Rechazado'), ('Publicado', 'Publicado'), ('Inactivo', 'Inactivo')], default='Borrador', max_length=20),
        ),
        migrations.AddField(
            model_name='contenido',
            name='posicion',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='ModificacionContenido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_modificacion', models.DateTimeField(auto_now_add=True)),
                ('estado_anterior', models.CharField(choices=[('Borrador', 'Borrador'), ('En Revisión', 'En Revisión'), ('Rechazado', 'Rechazado'), ('Publicado', 'Publicado'), ('Inactivo', 'Inactivo')], max_length=20)),
                ('comentario', models.TextField(blank=True, null=True)),
                ('contenido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Seguridad.contenido')),
                ('usuario_modificacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
