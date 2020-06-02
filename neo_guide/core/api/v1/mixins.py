from django.core.exceptions import ValidationError
from rest_framework import exceptions as rest_exceptions

from neo_guide.core.api.v1.exceptions import BusinessLogicAPIException
from neo_guide.core.exceptions import BusinessLogicException


class ApiErrorsMixin:
    """
    Mixin that transforms Django and Python exceptions into rest_framework ones.
    Without the mixin, they return 500 status code which is not desired.
    """

    expected_exceptions = {
        ValueError: rest_exceptions.ValidationError,
        ValidationError: rest_exceptions.ValidationError,
        PermissionError: rest_exceptions.PermissionDenied,
        BusinessLogicException: BusinessLogicAPIException,
    }

    @staticmethod
    def _get_first_matching_attr(obj, *attrs, default=None):
        for attr in attrs:
            if hasattr(obj, attr):
                return getattr(obj, attr)

        return default

    def _get_error_message(self, exc):
        if hasattr(exc, 'message_dict'):
            return exc.message_dict

        error_msg = self._get_first_matching_attr(exc, 'message', 'messages')

        if isinstance(error_msg, list):
            error_msg = ', '.join(error_msg)

        if error_msg is None:
            error_msg = str(exc)

        return error_msg

    def handle_exception(self, exc):
        if isinstance(exc, tuple(self.expected_exceptions.keys())):
            drf_exception_class = self.expected_exceptions[exc.__class__]
            drf_exception = drf_exception_class(self._get_error_message(exc))

            return super().handle_exception(drf_exception)

        return super().handle_exception(exc)
