# Generated by Django 4.1.5 on 2023-01-12 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="image",
            field=models.ImageField(
                blank=True, default="placeholder.png", null=True, upload_to=""
            ),
        ),
    ]