from django.core.exceptions import ValidationError
from django.utils.translation import gettext
from django.core.validators import BaseValidator

class CustomPasswordValidator(BaseValidator):
    def __init__(self, min_length=6, special_chars=1):
        self.min_length = min_length
        self.special_chars = special_chars

    def validate(self, password, user=None):
        print("hi")
        all_errors = []#instead of saying 1 error message at the same time this method does it all at once
        #instead of saying 1 error message at the same time this method does it all at once
        if len(password) < self.min_length:
            all_errors.append(
            ValidationError(
                gettext("The password must be at least %(min_length)d characters."),
                code='password_too_short',
                params={'min_length': self.min_length},
            ))
            # raise ValidationError(
            #     _("The password must be at least %(min_length)d characters."),
            #     code='password_too_short',
            #     params={'min_length': self.min_length},
            # )

        if not any(not char.isalpha() for char in password):
            all_errors.append(
            ValidationError(
                gettext("The password must contain at least %(special_chars)d number or special character."),
                code='password_missing_special_chars',
                params={'special_chars': self.special_chars},
            ))
            #     _("The password must contain at least %(special_chars)d number or special character."),
            #     code='password_missing_special_chars',
            #     params={'special_chars': self.special_chars},
            # )
        if not any(char.isupper() for char in password):
            all_errors.append(ValidationError(
                gettext("The password must contain at least 1 uppercase letter."),
                code='password_missing_uppercase_letter',
            ))
            # raise ValidationError(
            #     _("The password must contain at least %(1)d uppercase letter."),
            #     code='password_missing_uppercase_letter',
            # )
        if sum(1 for char in password if char.islower) < 1:
            all_errors.append(
                ValidationError(
                    gettext("The password must contain at least 1 lowercase letter."),
                    code = 'password_missing_uppercase_letter',
            ))
            # raise ValidationError(
            #     _("The password must contain at least %(1)d lowercase letter."),
            #     code='password_missing_uppercase_letter',
            # )
        if all_errors:
            raise ValidationError(all_errors)
    def get_help_text(self):
        return gettext(
            "The password must be at least %(min_length)d characters and contain "
            "at least %(special_chars)d special characters."
            "a uppercase and lowercase character"
        ) % {'min_length': self.min_length, 'special_chars': self.special_chars}