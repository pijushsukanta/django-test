from django.urls import path
from app.api_view.total_read_fav_qs import TotalFavouriteAndReadQs
from app.api_view.question_filter import QuestionFilter

from app.views import FakeUser

urlpatterns = [
    path('createFakeData', FakeUser.as_view()),
    path('questions/getTotalReadAndFavQs', TotalFavouriteAndReadQs.as_view()),
    path('questions', QuestionFilter.as_view())
]
