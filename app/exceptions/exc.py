class InvalidValueError(Exception):
    model_value = {
        "name": str,
        "email": str,
        "username": str,
        "password": str
    }

    def __init__(self, data):
        self.message = {
            "status": "error",
            "message": [f"key {key} must be type 'str'" for key, value in data.items() if type(value) != self.model_value[key]]
        }
        super().__init__(self.message)



class InvalidKeyError(Exception):
    model_key = ['name', 'email', 'username', 'password']

    def __init__(self, data):
        self.message = {
            "status": "error",
            "message": [f'key {key} invalid'for key in data.keys() if key not in self.model_key]
        }
        super().__init__(self.message)


class RequiredKeyError(Exception):
    model_required = ['name', 'email', 'username', 'password']

    def __init__(self, data):
        self.message = {
            "status": "error",
            "message": [f"{item} is required" for item in self.model_required if item not in data]
        }
        super().__init__(self.message)
