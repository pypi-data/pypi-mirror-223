
class FilterParams:
    def __init__(self, params: dict[str, str]):
        for key in params.keys():
            setattr(self, key, params[key])
