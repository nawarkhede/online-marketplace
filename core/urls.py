from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from core import forms as core_forms


urlpatterns = [
    path("", views.index, name="index"),
    path("contact/", views.contact, name="contact"),
    path("signup/", views.signup, name="signup"),
    path("login/", auth_views.LoginView.as_view(
        template_name="core/login.html",
        authentication_form=core_forms.LoginForm), name="login"
        )
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

print(urlpatterns)