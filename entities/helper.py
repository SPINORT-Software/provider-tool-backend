from rest_framework.response import Response
from providertool.constants import *
import datetime
import math


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


class InputParser:
    @staticmethod
    def parse_input(input_type, input_value):
        def parse_int(value):
            return math.floor(int(value))

        def parse_decimal(value):
            return float(value)

        def parse_time(value):
            hours = math.floor(int(value.get('hours')))
            minutes = math.floor(int(value.get('minutes')))

            return datetime.time(hours, minutes, 00)

        def parse_date(value):
            year = int(value.get('year'))
            month = int(value.get('month'))
            day = int(value.get('day'))

            return datetime.date(year, month, day)

        def parse_text(value):
            return str(value)

        input_type_dict = {
            'value_int': parse_int,
            'value_decimal': parse_decimal,
            'value_time': parse_time,
            'value_date': parse_date,
            'value_text': parse_text
        }

        input_parser = input_type_dict.get(input_type)
        return input_parser(input_value)
