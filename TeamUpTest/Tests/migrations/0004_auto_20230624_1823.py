# Generated by Django 3.2 on 2023-06-24 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tests', '0003_auto_20230620_2043'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='answer_question_answer',
            new_name='answer_question',
        ),
        migrations.AlterField(
            model_name='poll',
            name='secret_key',
            field=models.CharField(default='gJsyxiDokw', max_length=10, unique=True),
        ),
    ]
