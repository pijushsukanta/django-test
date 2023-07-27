import random
from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class User(models.Model):
    idname = models.CharField(max_length=250,unique=True)
    display_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    phone = models.CharField(max_length=250)
    
    
class Question(models.Model):
    question = models.TextField()
    option1 = models.TextField()
    option2 = models.TextField()
    option3 = models.TextField()
    option4 = models.TextField()
    option5 = models.TextField()
    answer = models.SmallIntegerField(default=random.randint(1,5))
    explain = models.TextField()
    
    
class FavouriteQuestion(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question,on_delete=models.CASCADE)
    
class ReadQuestion(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question,on_delete=models.CASCADE)