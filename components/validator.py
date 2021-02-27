import datetime
import re


def is_int(self, key, value):
    if isinstance(value, str):
        value = int(value)
    else:
        assert isinstance(value, int)
    return value


def is_string(self, key, value):
    column_type = getattr(type(self), key).expression.type
    max_length = column_type.length

    if len(value) > max_length:
        raise ValueError(
            f'Value "{value}" for column "{key}": '
            f'exceeds maximum length of "{max_length}"'
        )

    return value


def is_email(self, key, value):
    column_type = getattr(type(self), key).expression.type
    max_length = column_type.length

    if len(value) > max_length:
        raise ValueError(
            f'Value "{value}" for column "{key}": '
            f'exceeds maximum length of "{max_length}"'
        )
    # simplistic method but would like replace with a library for production
    if re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", value):
        return value
    else:
        raise ValueError(
            f'Value "{value}" for column "{key}": '
            f'syntax does not comply with RFC 6854'
        )

    return value


def is_datetime(self, key, value):
    assert isinstance(value, datetime.datetime)
    return value


def has_value(self, key, value, values=None):
    if values:
        if value in values:
            return value
        else:
            raise ValueError(
                f'Value "{value}" for column "{key}": '
                f'Value must be one of the following; {", ".join(values)}'
            )
    else:
        if not value:
            raise ValueError(
                f'Value "{value}" for column "{key}": '
                f'Value required'
            )