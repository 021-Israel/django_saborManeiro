# Generated by Django 5.1.7 on 2025-04-19 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservar', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pessoa',
            name='comentarios',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pessoa',
            name='convidados',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pessoa',
            name='data',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='nome',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='sobrenome',
            field=models.CharField(max_length=255),
        ),
    ]
