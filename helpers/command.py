import json

from helpers.common import send_message


class Command(object):
    def __init__(self, command_action, command_string):
        self.command_action = command_action
        self.command_string = command_string

    def execute(self):
        data = {
            'type': 'command',
            'action': self.command_action,
            'body': self.command_string
        }

        send_message(json.dumps(data))
