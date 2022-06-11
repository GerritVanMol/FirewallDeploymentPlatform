# Generated by Django 4.0.4 on 2022-06-10 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_firewalls_vendor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='firewalls',
            name='premise_code',
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name='firewalls',
            name='state',
            field=models.BooleanField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')]),
        ),
        migrations.AlterField(
            model_name='firewalls',
            name='vendor',
            field=models.CharField(choices=[('Palo Alot', 'Palo Alto'), ('Fortinet', 'Fortinet'), ('Juniper', 'Juniper'), ('Barracuda', 'Barracuda')], max_length=20),
        ),
    ]
