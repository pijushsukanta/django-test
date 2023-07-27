from enum import Enum


class DataGenerateEnum(Enum):
    CREATE_USER = "1"
    CREATE_FAVOURITE_QUESTION = "2"
    CREATE_READ_QUESTIOM = "3"
    CREATE_QUESTIOM = "4"
    
class QuestionQueryEnum(Enum):
    FAVOURITE = "1"
    UNFAVOURITE = "2"
    READ = "3"
    UNREAD = "5"