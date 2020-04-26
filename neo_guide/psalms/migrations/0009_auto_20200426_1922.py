# Generated by Django 3.0.3 on 2020-04-26 19:22

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('psalms', '0008_auto_20200217_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='psalm',
            name='liturgical_period',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('advent', 'Śpiew na Adwent'), ('christmas', 'Śpiew na Boże Narodzenie'), ('lent', 'Śpiew na Wielki Post'), ('easter', 'Śpiew na Wielkanoc'), ('normal_period', 'Śpiew okres zwykyły')], default='normal_period', max_length=42, null=True, verbose_name='Okres liturgiczny'),
        ),
    ]