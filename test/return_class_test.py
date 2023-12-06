from util.return_class import ReturnClass
from util.return_class import ReturnClassUtils


class ReturnClassTest:
    def __init__(self):
        self.return_class_utils = ReturnClassUtils()

    def run(self):
        print("< Test Start >")
        color_type, device_id, button_id = '/', 1, 1

        method_1_class = ReturnClass(_color_type=color_type, _device_id=device_id, _button_id=button_id)
        method_2_class = self.return_class_utils.set_return_class(color_type, device_id, button_id)
        method_1_class_dict = self.return_class_utils.get_convert_dict(method_1_class)
        method_1_class_json = self.return_class_utils.get_convert_json(method_1_class)
        _color_type, _device_id, _button_id = method_1_class
        dict2class = self.return_class_utils.get_convert_return_class(method_1_class_dict)

        none_return_class = ReturnClass(_color_type=None, _device_id=None, _button_id=None)
        _n_color_type, _n_device_id, _n_button_id = none_return_class

        print("Make Class #1: ", method_1_class)
        print("Make Class #2: ", method_2_class)
        print("Make Class and Convert Dict: ", method_1_class_dict)
        print("Make Class and Convert Json: ", method_1_class_json)
        print("Return Class Unpacking Test: ", _color_type, _device_id, _button_id)
        print("Make Class with dict: ", dict2class)
        print("Return Class with None Value Unpacking Test: ", _n_color_type, _n_device_id, _n_button_id)


if __name__ == '__main__':
    test = ReturnClassTest()
    test.run()
