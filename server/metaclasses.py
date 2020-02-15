"""Server side metaclasses for Messenger app."""
from dis import get_instructions


class ServerVerifier(type):
    """Server verifier metaclass."""
    def __init__(self, clsname, bases, clsdict):
        methods = list()
        attrs = list()
        funcs = [func for func in clsdict.values() if callable(func)]

        for func in funcs:
            self._get_methods_and_attrs(get_instructions(func), methods, attrs)

        self._validate_methods(methods)
        self._validate_attrs(attrs)

        super().__init__(clsname, bases, clsdict)

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
        if 'connect' in methods:
            raise TypeError(
                'You can\'t use socket "connect" method on server side.'
            )

    @staticmethod
    def _validate_attrs(attrs):
        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise TypeError(
                'You must use SOCK_STREAM and AF_INET args for initialize '
                'socket because of only TCP connection is available.'
            )
