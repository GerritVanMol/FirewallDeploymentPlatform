# Generated by Django 4.0.4 on 2022-06-11 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_rename_firewall_firewalls'),
    ]

    operations = [
        migrations.AlterField(
            model_name='firewalls',
            name='state',
            field=models.BooleanField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default=False, null=True),
        ),
        migrations.AlterField(
            model_name='firewalls',
            name='vendor',
            field=models.CharField(choices=[('Palo Alto', 'Palo Alto'), ('Fortinet', 'Fortinet'), ('Juniper', 'Juniper'), ('Barracuda', 'Barracuda')], default='Fortinet', max_length=20),
        ),
    ]
