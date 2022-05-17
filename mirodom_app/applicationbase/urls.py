from django.urls import path
from applicationbase.views import index, by_master, AppLoginView, profile, AppLogoutView, ChangeUserInfoView, AppPasswordChangeView  #, AppCreateView
from .views import RegisterUserView, RegisterDoneView
from .views import user_activate
from .views import  DeleteUserView
from .views import detail, profile_app_detail, profile_app_add, profile_app_change, profile_app_delete




app_name = 'applicationbase'
urlpatterns = [
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/register/done', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/logout/', AppLogoutView.as_view(), name='logout'),
    path('accoutns/profile/delete/',DeleteUserView.as_view(), name='profile_delete'),
    path('accounts/password/change/', AppPasswordChangeView.as_view(), name='password_change'),
    path('accounts/profile/change/<int:pk>/', profile_app_change, name='profile_app_change'),
    path('accounts/profile/delete/<int:pk>/', profile_app_delete, name='profile_app_delete'),
    path('accounts/profile/add/', profile_app_add, name='profile_app_add'),
    path('accounts/profile/<int:pk>', profile_app_detail, name='profile_app_detail'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/login/', AppLoginView.as_view(),name='login'),
    path('<int:master_pk>/<int:pk>/', detail, name='detail'),
    path('<int:master_id>/', by_master, name = 'by_master'),
    path('',index, name='index'),
    #path('create/', AppCreateView.as_view(), name='create'),
]
