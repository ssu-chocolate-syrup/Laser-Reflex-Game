import json


class ReturnClass:
    def __init__(self, _color_type=None, _device_id=None, _button_id=None):
        self.color_type = _color_type
        self.device_id = _device_id
        self.button_id = _button_id

    def __iter__(self):
        yield self.color_type
        yield self.device_id
        yield self.button_id


class ReturnClassUtils:

    @staticmethod
    def set_return_class(_color_type, _device_id, _button_id):
        return ReturnClass(_color_type, _device_id, _button_id)

    def get_convert_return_class(self, data):
        _color_type = data.get('c', None)
        _device_id = data.get('d', None)
        _button_id = data.get('b', None)
        if _color_type and _device_id and _button_id:
            return self.set_return_class(_color_type, _device_id, _button_id)
        return data

    @staticmethod
    def get_convert_dict(data):
        _color_type, _device_id, _button_id = data
        return {'c': _color_type, 'd': _device_id, 'b': _button_id}

    def get_convert_json(self, data):
        return json.dumps(self.get_convert_dict(data))
