# Generated by Django 4.0.6 on 2022-11-30 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0018_alter_review_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='body',
            field=models.TextField(blank=True, default='without_comment', max_length=300),
        ),
    ]
