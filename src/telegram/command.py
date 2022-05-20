class CommandHandler:
    def __init__(self):
        self.handlers: dict = {}

    def add_handler(self, function, command):
        self.handlers[command] = function

    def execute(self, request):
        return self.handlers[request.text](request)


class CallbackHandler(CommandHandler):
    def execute(self, request):
        # TODO ADD test for this
        return self.handlers[request.request](request)


class TextHandler(CommandHandler):
    pass
