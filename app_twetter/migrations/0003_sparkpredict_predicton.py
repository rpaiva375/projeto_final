# Generated by Django 4.0.2 on 2022-02-12 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_twetter', '0002_alter_sparkpredict_table_alter_twitter_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='sparkpredict',
            name='predicton',
            field=models.IntegerField(default=0),
        ),
    ]
