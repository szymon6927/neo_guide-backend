from dataclasses import dataclass

from django.contrib.auth.password_validation import validate_password
from django.db import transaction

from neo_guide.core.exceptions import BusinessLogicException
from neo_guide.users.models import User


@dataclass
class ChangePasswordInputDTO:
    current_password: str
    new_password: str
    confirm_new_password: str


def change_password(user: User, data: ChangePasswordInputDTO):
    if not user.check_password(data.current_password):
        raise BusinessLogicException('Current password is not correct!')

    validate_password(data.new_password, user=user)

    with transaction.atomic():
        user.set_password(data.new_password)
        user.save()
