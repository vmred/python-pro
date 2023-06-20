class DBConnection:
    connection = None

    @staticmethod
    def create_connection():
        raise NotImplemented

    def get_connection(self, **kwargs):
        raise NotImplemented

    def execute_query(self, query):
        raise NotImplemented
