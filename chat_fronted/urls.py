from django.urls import path
from chat_fronted import views as chat_views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", chat_views.chatPage, name="chat-page"),

    # authentication section
    path("login/", LoginView.as_view(template_name="loginpage.html"), name="login-user"),
    path("logout/", LogoutView.as_view(next_page='login-user'), name="logout-user"),
]
