# Generated by Django 4.0.3 on 2022-03-03 20:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Quizker', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='multiplechoice',
            options={'verbose_name_plural': 'Multiple Choice Question'},
        ),
        migrations.AlterModelOptions(
            name='openended',
            options={'verbose_name_plural': 'Open ended Question'},
        ),
        migrations.AlterModelOptions(
            name='quiz',
            options={'verbose_name_plural': 'Quizzes'},
        ),
        migrations.AlterModelOptions(
            name='trueorfalse',
            options={'verbose_name_plural': 'True or False Question'},
        ),
    ]
