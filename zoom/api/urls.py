from django.urls import path
from . import views
urlpatterns = [
    path('meeting/',views.Meetings.as_view()),
    path('meeting/create/',views.CreateMeeting.as_view()),
    path('meeting/<int:id>/',views.MeetingtDetail.as_view()),
]

