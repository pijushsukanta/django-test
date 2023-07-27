import string
from django.shortcuts import render

# Create your views here.
import random
from typing import Any
from django.shortcuts import render
from rest_framework.views import APIView
from faker import Faker
from app.app_enums import DataGenerateEnum
from app.models import FavouriteQuestion, Question, ReadQuestion, User
import concurrent.futures
import threading


from app.response_controller import ResponseController

# Create your views here.
class FakeUser(APIView,ResponseController):
    fake = Faker()
    users = []
    questions = []
    
    def __init__(self,message="",status=200,error=False, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        
    
    
    def post(self, request,*args,**kwargs):
        try:
            self.users  = []
            num_threads = 4
            total = 100
            thread_list = []
            
            data_generate_choice = request.GET.get("choice")
            if data_generate_choice is None:
                raise Exception("Data Generation Choice Not Given in Query") 
            
            
            chunks = [[j for j in range(i,i+total//num_threads)] for i in range(0,total,total//num_threads)]
            
            # We can use ThreadPooExecutor Also
            # with concurrent.futures.ThreadPoolExecutor() as executor:
            #     print("Started")
            #     executor.map(self.__create_user, chunks) 
            #     print("ended")
            # print(len(chunks))
            
            for thr in range(len(chunks)):
                if DataGenerateEnum.CREATE_USER.value == data_generate_choice:
                    thread = threading.Thread(target=self.__create_user(chunks[thr]), args=(chunks[thr]),)
                    thread_list.append(thread)
                elif DataGenerateEnum.CREATE_FAVOURITE_QUESTION.value == data_generate_choice:
                    thread = threading.Thread(target=self.__create_favourite_question(chunks[thr]), args=(chunks[thr]),)
                    thread_list.append(thread)
                elif DataGenerateEnum.CREATE_READ_QUESTIOM.value == data_generate_choice:
                    thread = threading.Thread(target=self.__create_read_question(chunks[thr]), args=(chunks[thr]),)
                    thread_list.append(thread)
                elif DataGenerateEnum.CREATE_QUESTIOM.value == data_generate_choice:
                    thread = threading.Thread(target=self.__create_question(chunks[thr]), args=(chunks[thr]),)
                    thread_list.append(thread)
                thread_list[thr].start()

            for thread in thread_list:
                thread.join()
            
                
            self.error = False
            self.status = 200
            
            return self.success_response(success_message="Fake User created")
        except Exception as e:
            return self.error_response(error_message=f"{e}")
    
    
    def __create_user(self,chunk):
        users = []
        for _ in range(len(chunk)):
            name = self.fake.unique.name()
            mobile = f"01{random.randint(3,9)}{random.randint(10000000,99999999)}"
            email = name.replace(" ",".")
            users.append(
                User(
                    idname=name,
                    display_name=name.split(" ")[0],
                    email=f"{email}@gmail.com",
                    phone=mobile
                )
            )
        User.objects.bulk_create(users)
        
        
        
    def __create_question(self,chunk):
        
        questions = []
        for _ in range(len(chunk)):
            questions.append(
                Question(
                    question = self.fake.sentence(),
                    answer = random.randint(1,5),
                    explain = ''.join(random.choice(string.ascii_letters) for i in range(10)),
                    option1 = ''.join(random.choice(string.ascii_letters) for i in range(10)),
                    option2 = ''.join(random.choice(string.ascii_letters) for i in range(10)),
                    option3 = ''.join(random.choice(string.ascii_letters) for i in range(10)),
                    option4 = ''.join(random.choice(string.ascii_letters) for i in range(10)),
                    option5 = ''.join(random.choice(string.ascii_letters) for i in range(10))   
                )
            )
        Question.objects.bulk_create(questions)
        
        
    def __create_read_question(self,chunk):
        questions = []
        for _ in range(len(chunk)):
            questions.append(
                ReadQuestion(
                  user_id = User.objects.get(pk=1),
                  question_id = Question.objects.get(pk=random.randint(0,100))    
                )
            )
        ReadQuestion.objects.bulk_create(questions)        
        
        
    def __create_favourite_question(self,chunk):
        questions = []
        for _ in range(len(chunk)):
            questions.append(
                FavouriteQuestion(
                  user_id = User.objects.get(pk=1),
                  question_id = Question.objects.get(pk=random.randint(0,100))    
                )
            )
        FavouriteQuestion.objects.bulk_create(questions)    
        