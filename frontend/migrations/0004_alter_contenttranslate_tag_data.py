# Generated by Django 4.1.2 on 2024-02-18 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("frontend", "0003_contenttranslate_lang"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contenttranslate",
            name="tag_data",
            field=models.TextField(blank=True, null=True),
        ),
    ]
