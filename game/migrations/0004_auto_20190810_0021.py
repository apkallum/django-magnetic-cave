# Generated by Django 2.2.3 on 2019-08-10 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_auto_20190809_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='id',
            field=models.UUIDField(default='6cbc593ca8b448b48fa49126fb8be752', editable=False, primary_key=True, serialize=False),
        ),
    ]
