class InvalidValueError(Exception):

    def __init__(self, data, model_to_compare):
        self.message = {
            "status": "error",
            "message": [f"key {key} must be type {(model_to_compare[key].__name__)}" for key, value in data.items() if type(value) != model_to_compare[key]]
        }
        super().__init__(self.message)


class InvalidKeyError(Exception):

    def __init__(self, data, model_to_compare):
        self.message = {
            "status": "error",
            "message": [f'key {key} invalid'for key in data.keys() if key not in model_to_compare]
        }
        super().__init__(self.message)


class RequiredKeyError(Exception):

    def __init__(self, data, model_to_compare):
        self.message = {
            "status": "error",
            "message": [f"{item} is required" for item in model_to_compare if item not in data]
        }
        super().__init__(self.message)
