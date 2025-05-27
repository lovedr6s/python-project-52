from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import CustomAuthForm
from .views import *


urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('create/', UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True, next_page='home', authentication_form=CustomAuthForm), name='login'),
]