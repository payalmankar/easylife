# Generated by Django 3.1.2 on 2022-05-02 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletters', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newsletter',
            options={'ordering': ('-created_At',), 'verbose_name': 'News letter', 'verbose_name_plural': 'News letters'},
        ),
        migrations.RenameField(
            model_name='newsletter',
            old_name='email_date',
            new_name='created_At',
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='subscribed',
            field=models.BooleanField(default=True, verbose_name='Subscribed'),
        ),
    ]
