from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeProfile.as_view(), name="profiles"),
    path('profile/<str:username>/', views.UserProfile.as_view(), name="user-profile"),
    path('skill/<slug:skill_slug>', views.ProfileBySkill.as_view(), name="skill"),
    path('login/', views.CustomLoginUser.as_view(), name="login-site"),
    path('logout/', views.UserLogout.as_view(), name="logout"),
    path('register/', views.RegisterUser.as_view(), name="register"),
    path('account/', views.UserAccount.as_view(), name="account"),
    path('edit-account/', views.EditAccount.as_view(), name="edit-account"),
    path('create-skill/', views.SkillCreate.as_view(), name="create-skill"),
    path('update-skill/<slug:slug>/', views.SkillUpdate.as_view(), name="update-skill"),
    path('delete-skill/<slug:slug>/', views.SkillDelete.as_view(), name="delete-skill"),
    path('inbox/', views.InboxView.as_view(), name="inbox"),
    path('create-message/<str:username>/', views.CreateMessage.as_view(), name="create-message"),
    path('message/<str:pk>/', views.MessageView.as_view(), name="message"),


]
