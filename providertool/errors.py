class Error(Exception):
    pass


class MissingRequiredParamsException(Error):
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     # self.message = message
    #     # self.result = result
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.message = kwargs.get('message')
        self.result = kwargs.get('result')
        self.status = kwargs.get('status')

        self.errors = {
            'result': self.result
        }


def default_error_response(serializer):
    """
    Prepare serializer error messages for response.
    :param serializer:
    :return:
    """
    error_message = []
    for key in serializer._errors:
        error_message.append("%s" % (serializer._errors[key][0]))
    return ",".join(error_message)
