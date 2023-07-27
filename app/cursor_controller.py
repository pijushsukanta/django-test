from django.db import connection


class CursorController:
    
    def __init__(self,query=None) -> None:
        self.query = query
        
    def __format_data(self,cursor):
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns,row))
            for row in cursor.fetchall()
        ]
        
    
    def query_execute(self):
        try:
            if self.query is None:
                return None
            with connection.cursor() as cursor:
                cursor.execute(self.query)
                data = self.__format_data(cursor)
                return data
        except Exception as e:
            return None
     