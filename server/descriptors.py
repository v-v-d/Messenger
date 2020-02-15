"""Server side descriptors for Messenger app."""
from math import log
from ipaddress import ip_address


class PortValidator:
    """Validator for server port."""
    def __get__(self, instance, owner):
        return instance.__dict__[self.attr]

    def __set__(self, instance, value):
        min_value = 1024
        max_value = 65536
        if min_value <= value <= max_value:
            instance.__dict__[self.attr] = value
        else:
            raise ValueError(
                f'{self.attr} must be {min_value}-{max_value}, {value} given.'
            )

    def __delete__(self, instance):
        del instance.__dict__[self.attr]

    def __set_name__(self, owner, attr):
        self.attr = attr


class HostValidator:
    """Validator for server host."""
    def __get__(self, instance, owner):
        return instance.__dict__[self.attr]

    def __set__(self, instance, value):
        try:
            value = ip_address(value)

        except Exception as error:
            raise ValueError(f'Wrong IP address. {error}.')

        instance.__dict__[self.attr] = str(value)

    def __delete__(self, instance):
        del instance.__dict__[self.attr]

    def __set_name__(self, owner, attr):
        self.attr = attr


class BufsizeValidator:
    """Validator for server buffersize."""
    def __get__(self, instance, owner):
        return instance.__dict__[self.attr]

    def __set__(self, instance, value):
        if not log(value, 2) % 1:
            instance.__dict__[self.attr] = value
        else:
            raise ValueError(
                f'{self.attr} must be result of raising 2 to the power, {value} given.'
            )

    def __delete__(self, instance):
        del instance.__dict__[self.attr]

    def __set_name__(self, owner, attr):
        self.attr = attr
