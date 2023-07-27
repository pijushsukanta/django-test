from rest_framework.response import Response

class ResponseController:
    
    def __init__(self,data=None,message="",status=200,error=False):
        print(self)
        self.status = status
        self.error = error
        self.data = data
        self.message = message
        
    def __get_response(self):
        return Response({
            "error": self.error,
            "message":self.message,
            "status" : self.status,
            "data" : self.data
        })
        
    def success_response(self,success_message,data=[]):
       self.message = success_message
       self.data = data
       return self.__get_response()
   
    def error_response(self,error_message):
       print(error_message) 
       self.error = True
       self.message = error_message
       self.data = []
       self.status = 400
       return self.__get_response()