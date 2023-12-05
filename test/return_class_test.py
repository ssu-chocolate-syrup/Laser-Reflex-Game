import json

from return_class import ReturnClass


class ReturnClassTest:
    def run(self):
        print("< Test Start >")
        color_type, device_id, button_id = '/', 1, 1

        method_1_class = ReturnClass(_color_type=color_type, _device_id=device_id, _button_id=button_id)
        method_2_class = ReturnClass().set_return_class(color_type, device_id, button_id)
        method_1_class_dict = method_1_class.get_convert_dict()
        method_1_class_json = method_1_class.get_convert_json()
        _color_type, _device_id, _button_id = method_1_class
        dict2class = ReturnClass().get_convert_return_class(method_1_class_dict)

        print("Make Class #1: ", method_1_class)
        print("Make Class #2: ", method_2_class)
        print("Make Class and Convert Dict: ", method_1_class_dict)
        print("Make Class and Convert Json: ", method_1_class_json)
        print("Return Class Unpacking Test: ", _color_type, _device_id, _button_id)
        print("Make Class with dict: ", dict2class)


if __name__ == '__main__':
    test = ReturnClassTest()
    test.run()