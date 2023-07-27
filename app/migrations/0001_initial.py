# Generated by Django 4.1.4 on 2023-07-26 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idname', models.CharField(max_length=250, unique=True)),
                ('display_name', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=250)),
                ('phone', models.CharField(max_length=250)),
            ],
        ),
    ]
