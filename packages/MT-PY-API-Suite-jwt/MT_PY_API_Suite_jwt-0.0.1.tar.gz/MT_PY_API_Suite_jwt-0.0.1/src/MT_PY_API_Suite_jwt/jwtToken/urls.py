from django.contrib import admin
from django.urls import path
from .views import Register,LoginView,User_info_view



urlpatterns = [
    path('sign_up/', Register.as_view(), name='Register'),
    path('sign_in/', LoginView.as_view(), name='LoginView'),
    path('user_info/', User_info_view.as_view(), name='User_info'),
    path("user_info/<int:pk>/",User_info_view.as_view(),name='user_info_get')
    # path('admin/', admin.site.urls),
]
