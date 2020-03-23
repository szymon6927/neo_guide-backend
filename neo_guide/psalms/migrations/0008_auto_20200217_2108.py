# Generated by Django 3.0.3 on 2020-02-17 21:08

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('psalms', '0007_auto_20200217_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='psalm',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Komentarz'),
        ),
        migrations.AlterField(
            model_name='psalm',
            name='liturgical_period',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('advent', 'Śpiew na Adwent + Boże Narodzenie'), ('lent', 'Śpiew na Wielki Post'), ('easter', 'Śpiew na Wielkanoc'), ('normal_period', 'Śpiew okres zwykyły')], default='normal_period', max_length=32, null=True, verbose_name='Okres liturgiczny'),
        ),
        migrations.AlterField(
            model_name='psalm',
            name='neo_stage',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('first_scrutinium', 'Śpiew etapu "I Scrutinium"'), ('shema', 'Śpiew etapu "Shema"'), ('second_scrutinium', 'Śpiew etapu "II Scrutinium"'), ('introduction_to_prayer', 'Śpiew etapu "Wprowadzenie w modlitwę"'), ('traditio', 'Śpiew etapu "Traditio"'), ('reditio', 'Śpiew etapu "Reditio"'), ('our_father', 'Śpiew etapu "Ojcze nasz"'), ('choosing', 'Śpiew etapu "Wybranie"'), ('baptism', 'Śpiew etapu "Odnowienie przyrzeczeń chrzcielnych"')], max_length=108, null=True, verbose_name='Etap'),
        ),
        migrations.AlterField(
            model_name='psalm',
            name='type',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('peace_sign', 'Śpiew na znak pokoju'), ('fraction_of_bread', 'Śpiew na łamanie chleba'), ('adoration', 'Śpiew na krew Pańską + uwielbienie'), ('final_pslam', 'Śpiew na zakończenie eucharystii'), ('solid_pslams', 'Śpiew części stałych'), ('virgin_mary_psalm', 'Śpiew Maryjny'), ('penitential_liturgy', 'Śpiew na liturgię pokutną')], max_length=101, null=True, verbose_name='Rodzaj'),
        ),
    ]