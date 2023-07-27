from typing import Any
from rest_framework.views import APIView
from app.cursor_controller import CursorController
from app.models import Question
from app.pagination import get_paginated_data

from app.response_controller import ResponseController


class TotalFavouriteAndReadQs(APIView,ResponseController,CursorController):
    
    def __init__(self,error=False,status=200, **kwargs: Any) -> None:
        super().__init__(**kwargs)
    
    def get(self, request,*args,**kwargs):
        try:
            data = []
            page = request.GET.get("page")
            total_page = int(self.__get_total_page()) 
            if page is None:
                page = 1
                
            data = self.__get_total_favrourite_and_read(page)
            data = get_paginated_data(int(page),total_page,data,100)
            
            self.error = False
            self.status = 200
            return self.success_response(success_message="List",data=data) 
        except Exception as e:
            return self.success_response(success_message="List Not Found",data=[])
    
    def __get_total_page(self):
        self.query = ''' SELECT COUNT(*) FROM app_user '''
        count = self.query_execute()
        key = [key for key in count[0].keys()][0]
        return count[0][key]
    
    def __get_total_favrourite_and_read(self,page_no=1,per_page=100):
        self.query = '''
            SELECT
            app_user.id as id,
            idname, 
            COUNT(app_readquestion.id) as total_read_question,
            COUNT(app_favouritequestion.id) as total_favourite_question
            FROM app_user
            INNER JOIN app_readquestion ON app_user.id = app_readquestion.user_id_id
            INNER JOIN app_favouritequestion ON app_user.id = app_favouritequestion.user_id_id
        '''

        per_page = per_page
        if per_page is None:
            per_page = 25
        from_id = 0
        page : int = int(page_no)
        if page > 1:
            from_id = (page * per_page) - per_page
            
        offset = f''' LIMIT 100 OFFSET {from_id} '''
        
        self.query = self.query + offset
        data = self.query_execute()
        return data
    
        