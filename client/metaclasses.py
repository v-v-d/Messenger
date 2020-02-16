"""Client side metaclasses for Messenger app."""
from dis import get_instructions
from socket import socket


class ClientVerifier(type):
    """Client verifier metaclass."""
    def __init__(self, clsname, bases, clsdict):
        methods = list()
        attrs = list()
        funcs = self._get_funcs(clsdict)

        for func in funcs:
            self._get_methods_and_attrs(get_instructions(func), methods, attrs)

        self._validate_methods(methods)
        self._validate_attrs(attrs)

        super().__init__(clsname, bases, clsdict)

    def _get_funcs(self, clsdict):
        funcs = list()
        for value in clsdict.values():
            self._validate_socket_declaration(value)
            if callable(value):
                funcs.append(value)
        return funcs

    @staticmethod
    def _validate_socket_declaration(value):
        if isinstance(value, socket):
            raise TypeError(
                'You can\'t create a socket outside a method.'
            )

    @staticmethod
    def _get_methods_and_attrs(instructions_iterator, methods, attrs):
        for instruction in instructions_iterator:
            if instruction.opname == 'LOAD_METHOD':
                if instruction.argval not in methods:
                    methods.append(instruction.argval)
            elif instruction.opname == 'LOAD_GLOBAL':
                if instruction.argval not in attrs:
                    attrs.append(instruction.argval)

    @staticmethod
    def _validate_methods(methods):
        wrong_methods = ('accept', 'listen')
        if any(el in wrong_methods for el in methods):
            raise TypeError(
                'You can\'t use socket "accept" and "listen" methods on client side.'
            )

    @staticmethod
    def _validate_attrs(attrs):
        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise TypeError(
                'You must use SOCK_STREAM and AF_INET args for initialize '
                'socket because of only TCP connection is available.'
            )
