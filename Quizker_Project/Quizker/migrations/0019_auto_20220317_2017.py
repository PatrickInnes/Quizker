# Generated by Django 2.1.5 on 2022-03-17 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quizker', '0018_auto_20220317_2013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quizattempt',
            name='quesitonsCompleted',
        ),
        migrations.AddField(
            model_name='quizattempt',
            name='questionsCompleted',
            field=models.IntegerField(default=1),
        ),
    ]
