from django.urls import path
from notifications import views

urlpatterns = [
    path('notifications/', views.NotificationList.as_view()),
    path('notifications/<int:pk>/', views.NotificationDetail.as_view()),
    path('notifications/mark-all-as-read/', views.MarkAllNotificationsAsRead.as_view()),
]
