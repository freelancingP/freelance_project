from rest_framework.response import Response
from rest_framework.serializers import Serializer


class JsonResponse(Response):
    def __init__(self, data=None, msg=None, count=None,
                 status=None, success=bool, error=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None, **kwargs):
        super().__init__(None, status=status)

        if isinstance(data, Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)
        self.data = {'success': success,'statuscode':status , 'message': msg,  'error': error, 'count': count, 'data': data,}
        self.data.update(kwargs)
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in headers.items():
                self[name] = value
                