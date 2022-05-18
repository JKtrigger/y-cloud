class CommandHandler:
    def __init__(self):
        self.handlers: dict = {}

    def add_handler(self, function, command):
        self.handlers[command] = function

    def execute(self, request):
        return self.handlers[request.text](request)
