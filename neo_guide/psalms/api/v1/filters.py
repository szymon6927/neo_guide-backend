from functools import reduce
from operator import or_

from django.db.models import Q
from django_filters import rest_framework as filters
from rest_framework import serializers

from neo_guide.psalms.choices import CardColorChoices
from neo_guide.psalms.choices import LiturgicalPeriodChoices
from neo_guide.psalms.choices import NeoStageChoices
from neo_guide.psalms.choices import PsalmTypeChoices
from neo_guide.psalms.models import Psalm


class PsalmsFilter(filters.FilterSet):
    card_color = filters.CharFilter(method='card_color_filter', field_name='card_color')
    type = filters.CharFilter(method='type_filter', field_name='type')
    liturgical_period = filters.CharFilter(method='liturgical_period_filter', field_name='liturgical_period')
    neo_stage = filters.CharFilter(method='neo_stage_filter', field_name='neo_stage')

    def card_color_filter(self, queryset, field_name, value):
        if value:
            values = PsalmsFilter.convert_to_list(value)
            PsalmsFilter.validate_card_color_choices(values)
            return queryset.filter(card_color__in=values)

        return queryset

    def type_filter(self, queryset, field_name, value):
        if value:
            values = PsalmsFilter.convert_to_list(value)
            PsalmsFilter.validate_psalm_type_choices(values)
            query = reduce(or_, [Q(type__contains=type_value) for type_value in values])

            return queryset.filter(query)

        return queryset

    def liturgical_period_filter(self, queryset, field_name, value):
        if value:
            values = PsalmsFilter.convert_to_list(value)
            PsalmsFilter.validate_psalm_liturgical_period_choices(values)
            query = reduce(
                or_, [Q(liturgical_period__contains=liturgical_period_value) for liturgical_period_value in values]
            )

            return queryset.filter(query)

        return queryset

    def neo_stage_filter(self, queryset, field_name, value):
        if value:
            values = PsalmsFilter.convert_to_list(value)
            PsalmsFilter.validate_neo_stage_period_choices(values)
            query = reduce(or_, [Q(neo_stage__contains=neo_stage_value) for neo_stage_value in values])

            return queryset.filter(query)

        return queryset

    @staticmethod
    def convert_to_list(values: str):
        return [value.strip() for value in values.split(',')]

    @staticmethod
    def validate_card_color_choices(values: list):
        if not all(choice in CardColorChoices.values for choice in values):
            raise serializers.ValidationError(
                {'card_color': f'Select a valid choice. {values} is/are not valid choices.'}
            )

    @staticmethod
    def validate_psalm_type_choices(values: list):
        if not all(choice in PsalmTypeChoices.values for choice in values):
            raise serializers.ValidationError({'type': f'Select a valid choice. {values} is/are not valid choices.'})

    @staticmethod
    def validate_psalm_liturgical_period_choices(values: list):
        if not all(choice in LiturgicalPeriodChoices.values for choice in values):
            raise serializers.ValidationError(
                {'liturgical_period': f'Select a valid choice. {values} is/are not valid choices.'}
            )

    @staticmethod
    def validate_neo_stage_period_choices(values: list):
        if not all(choice in NeoStageChoices.values for choice in values):
            raise serializers.ValidationError(
                {'neo_stage': f'Select a valid choice. {values} is/are not valid choices.'}
            )

    class Meta:
        model = Psalm
        fields = ['card_color']
