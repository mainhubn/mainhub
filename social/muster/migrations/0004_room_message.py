# Generated by Django 4.1.7 on 2023-03-22 01:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('muster', '0003_meep'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='muster.room')),
            ],
        ),
    ]
