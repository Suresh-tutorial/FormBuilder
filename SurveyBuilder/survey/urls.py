from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('404_error/', error_message, name='404_error'),
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('surveys/create/', create_survey, name='create_survey'),
    path('surveys/<int:pk>/', survey_detail, name='survey_detail'),
    path('surveys/<int:pk>/delete/', delete_survey, name='delete_survey'),
    path('user/dashboard/', user_dashboard, name='user_dashboard'),
    path('surveys/<int:pk>/take/', take_survey, name='take_survey'),
    path('surveys/<int:pk>/responses/', survey_responses, name='survey_responses'),
    path('surveys/<int:pk>/questions/create/', create_question, name='create_question'),
    path('questions/<int:pk>/delete/', delete_question, name='delete_question'),
    path('questions/<int:pk>/options/create/', create_option, name='create_option'),
    path('options/<int:pk>/delete/', delete_option, name='delete_option'),
    path('survey/thankyou/', survey_thankyou, name='survey_thankyou'),
]
