class DBConnection:
    def __init__(self):
        self.connection = None
        self.connection_pool = None

    def create_connection(self, **kwargs):
        raise NotImplementedError

    def get_connection(self, **kwargs):
        raise NotImplementedError

    def execute_query(self, query):
        raise NotImplementedError
