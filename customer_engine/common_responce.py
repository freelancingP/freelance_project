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
                
          
                
#   if not data or data_count == 0:
#             status_code = status.HTTP_204_NO_CONTENT
#             response = JsonResponse(
#                 status=status_code,
#                 data=data,
#                 success=False,
#                 error={"No State Found"},
#                 count=len(data),
#             )
#         else:
#             status_code = status.HTTP_200_OK
#             message = "Success"
#             response = JsonResponse(
#                 status=status_code,
#                 msg=message,
#                 data=data,
#                 success=True,
#                 error={},
#                 count=len(data),
#             )