# Generated by Django 3.2.12 on 2022-03-01 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0037_alter_product_prdisactive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='PRDISactive',
            field=models.CharField(blank=True, choices=[(True, 'Active'), (False, 'Inactive')], default=True, max_length=13, null=True),
        ),
    ]
