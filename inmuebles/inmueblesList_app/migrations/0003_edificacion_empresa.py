# Generated by Django 3.2.8 on 2024-01-15 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inmueblesList_app', '0002_auto_20240114_2332'),
    ]

    operations = [
        migrations.AddField(
            model_name='edificacion',
            name='empresa',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='edificacion', to='inmueblesList_app.empresa'),
            preserve_default=False,
        ),
    ]