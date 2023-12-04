import json


class ReturnClass:
    def __init__(self, _color_type, _device_id, _button_id):
        self.color_type = _color_type
        self.device_id = _device_id
        self.button_id = _button_id

    def __iter__(self):
        yield self.color_type
        yield self.device_id
        yield self.button_id

    def get_convert_json(self):
        return json.dumps({'c': self.color_type,
                           'd': self.device_id,
                           'b': self.button_id})
