from django.urls import path
from events import views


urlpatterns = [
    path('events/', views.EventList.as_view()),
    path('events/<int:pk>/', views.EventDetail.as_view()),
    path('category_choices/', views.CategoryChoicesView.as_view(), name='category-choices'),
]