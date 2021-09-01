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
