from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext as _

from neo_guide.psalms.choices import LiturgicalPeriodChoices
from neo_guide.psalms.choices import NeoStageChoices
from neo_guide.psalms.choices import PsalmTypeChoices


class PsalmTypeAdminFilter(SimpleListFilter):
    title = _('Rodzaj')
    parameter_name = 'type'

    def lookups(self, request, model_admin):
        return PsalmTypeChoices.choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(type__contains=self.value())


class PsalmLiturgicalPeriodAdminFilter(SimpleListFilter):
    title = _('Okres liturginczy')
    parameter_name = 'liturgical_period'

    def lookups(self, request, model_admin):
        return LiturgicalPeriodChoices.choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(liturgical_period__contains=self.value())


class PsalmNeoStageAdminFilter(SimpleListFilter):
    title = _('Etap')
    parameter_name = 'neo_stage'

    def lookups(self, request, model_admin):
        return NeoStageChoices.choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(neo_stage__contains=self.value())
