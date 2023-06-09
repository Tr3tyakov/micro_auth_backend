from inspect import isclass


class SerializerMixin:
    serializer_class = None

    def __init__(self, serializer_class=None, **kwargs):
        super().__init__(**kwargs)
        self.serializer_class = serializer_class

    def _get_serializer(self, data):
        if self.serializer_class is None:
            raise ValueError('serializer_class is not specified')

        if type(data) is list:
            return [self.serializer_class(**item[0].__dict__) for item in data]

        if isclass(type(data)):
            return self.serializer_class(**data.__dict__)
