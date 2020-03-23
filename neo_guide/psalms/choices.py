from django.db.models import TextChoices
from django.utils.translation import gettext as _


class CardColorChoices(TextChoices):
    WHITE = 'white', _('biały')
    YELLOW = 'yellow', _('żółty')
    GREY = 'grey', _('szary')
    GREEN = 'green', _('zielony')
    BLUE = 'blue', _('niebieski')


class PsalmTypeChoices(TextChoices):
    PEACE_SIGN = 'peace_sign', _('Śpiew na znak pokoju')
    FRACTION_OF_BREAD = 'fraction_of_bread', _('Śpiew na łamanie chleba')
    ADORATION = 'adoration', _('Śpiew na krew Pańską + uwielbienie')
    FINAL_PSALM = 'final_pslam', _('Śpiew na zakończenie eucharystii')
    SOLID_PSALM = 'solid_pslams', _('Śpiew części stałych')
    VIRGIN_MARY_PSALM = 'virgin_mary_psalm', _('Śpiew Maryjny')
    PENITENTIAL_LITURGY = 'penitential_liturgy', _('Śpiew na liturgię pokutną')


class LiturgicalPeriodChoices(TextChoices):
    ADVENT = 'advent', _('Śpiew na Adwent + Boże Narodzenie')
    LENT = 'lent', _('Śpiew na Wielki Post')
    EASTER = 'easter', _('Śpiew na Wielkanoc')
    NORMAL_PERIOD = 'normal_period', _('Śpiew okres zwykyły')


class NeoStageChoices(TextChoices):
    FIRST_SCRUTINIUM = 'first_scrutinium', _('Śpiew etapu "I Scrutinium"')
    SHEMA = 'shema', _('Śpiew etapu "Shema"')
    SECOND_SCRUTINIUM = 'second_scrutinium', _('Śpiew etapu "II Scrutinium"')
    INTRODUCTION_TO_PRAYER = 'introduction_to_prayer', _('Śpiew etapu "Wprowadzenie w modlitwę"')
    TRADITIO = 'traditio', _('Śpiew etapu "Traditio"')
    REDITIO = 'reditio', _('Śpiew etapu "Reditio"')
    OUR_FATHER = 'our_father', _('Śpiew etapu "Ojcze nasz"')
    CHOOSING = 'choosing', _('Śpiew etapu "Wybranie"')
    BAPTISM = 'baptism', _('Śpiew etapu "Odnowienie przyrzeczeń chrzcielnych"')
