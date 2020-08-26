class Bot:
    def __init__(self):
        self.routes = dict()

    def route(self, route_str):
        def decorator(f):
            self.routes.update({route_str: f})
            return f
        return decorator

    def serve(self, path):
        return self.routes.get(path)
