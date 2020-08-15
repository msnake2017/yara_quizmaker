from django.urls import path
from . import views


app_name = 'quiz_test'

urlpatterns = [
    path('', views.SignupOrLoginView.as_view(), name='signup_or_login'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('<int:user_id>/status/', views.user_table, name='user_table'),
    path('<int:user_id>/quiz_list/', views.quiz_list, name='quiz_list'),
    path('<int:user_id>/quiz_list/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
]
