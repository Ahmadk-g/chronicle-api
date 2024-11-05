from django.urls import path
from attendings import views

urlpatterns = [
    path('attendings/', views.AttendingList.as_view()),
    path('attendings/<int:pk>/', views.AttendingDetail.as_view()),
]
