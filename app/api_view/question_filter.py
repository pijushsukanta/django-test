from typing import Any
from rest_framework.views import APIView
from app.app_enums import QuestionQueryEnum
from app.cursor_controller import CursorController
from app.models import Question
from app.pagination import get_paginated_data

from app.response_controller import ResponseController

class QuestionFilter(APIView,ResponseController,CursorController):
    
    def __init__(self,error=False,status=200, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        
        
    def get(self, request,*args,**kwargs):
        try:
            data = []
            choice = request.GET.get("choice")
            page = request.GET.get("page")
            total_page = int(self.__get_total_page()) 
            if page is None:
                page = 1
            if 0 > int(choice) > 5:
                raise Exception("Please Insert Query Parameter")
            data = self.__get_read_favourite_query(page,100,choice)
            data = get_paginated_data(int(page),total_page,data,100)
            
            self.error = False
            self.status = 200
            return self.success_response(success_message="List",data=data) 
        except Exception as e:
            return self.error_response(error_message=f"{e}")
        
    def __get_total_page(self):
        self.query = ''' SELECT COUNT(*) FROM app_question '''
        count = self.query_execute()
        key = [key for key in count[0].keys()][0]
        return count[0][key]
        
    def __get_read_favourite_query(self,page_no=1,per_page=100,choice="1"):
        
        self.query = '''
            SELECT
            app_question.id,
            question,
            answer,
            explain,
            option1,
            option2,
            option3,
            option4,
            option5
            FROM app_question
            
        '''
        
        print(choice)
        
        if QuestionQueryEnum.FAVOURITE.value == choice:
            self.query = self.query + ''' INNER JOIN app_favouritequestion ON app_question.id=app_favouritequestion.question_id_id'''
        if QuestionQueryEnum.UNFAVOURITE.value == choice:
            self.query = self.query + ''' INNER JOIN app_favouritequestion ON app_question.id != app_favouritequestion.question_id_id'''
        if QuestionQueryEnum.READ.value == choice:
            self.query = self.query + ''' INNER JOIN app_readquestion ON app_question.id=app_readquestion.question_id_id'''
        if QuestionQueryEnum.UNREAD.value == choice:
            self.query = self.query + ''' INNER JOIN app_readquestion ON app_question.id!=app_readquestion.question_id_id'''
                
        per_page = per_page
        if per_page is None:
            per_page = 25
        from_id = 0
        page : int = int(page_no)
        if page > 1:
            from_id = (page * per_page) - per_page
            
        offset = f''' LIMIT 100 OFFSET {from_id} '''
        self.query = self.query + offset
        print(self.query)
        data = self.query_execute()
        return data