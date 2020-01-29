from django.db.models import TextChoices
from django.utils.translation import gettext as _


class CardColorChoices(TextChoices):
    WHITE = 'white', _('biały')
    YELLOW = 'yellow', _('żółty')
    GREY = 'grey', _('szary')
    GREEN = 'green', _('zielony')
    BLUE = 'blue', _('niebieski')
