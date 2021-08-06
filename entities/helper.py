from rest_framework.response import Response


class HttpResponse:
    def __init__(self, **kwargs):
        try:
            self.result = kwargs.get("result")
            self.message = kwargs.get("message")
            self.status = kwargs.get("status")
            self.value = None

            if "value" in kwargs:
                self.value = kwargs.get("value")
            if "id" in kwargs:
                self.id = kwargs.get("id")
            if "id_value" in kwargs:
                self.id_value = kwargs.get("id_value")
        except Exception as e:
            pass

    def get_response(self):
        response_dict = {
            'result': self.result,
            'message': self.message,
        }
        if self.value:
            response_dict['value'] = self.value
            print(response_dict)
        if hasattr(self, 'id'):
            response_dict['id'] = self.id
        if hasattr(self, 'id_value'):
            response_dict['id_value'] = self.id_value
        return Response(response_dict, status=self.status)
