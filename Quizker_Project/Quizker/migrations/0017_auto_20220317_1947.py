# Generated by Django 2.1.5 on 2022-03-17 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quizker', '0016_auto_20220317_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizattempt',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='quizattempt',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]