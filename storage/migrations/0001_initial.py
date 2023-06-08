# Generated by Django 3.2.15 on 2023-06-05 13:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import storage.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.ImageField(null=True, upload_to=storage.models.get_file_path)),
                ('image_probability', models.FloatField()),
                ('dirt_probability', models.FloatField()),
                ('chip_probability', models.FloatField()),
                ('bbox', models.TextField()),
                ('points', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]