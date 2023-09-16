from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # path for index view
    path('', views.get_dealerships, name='index'),

    # path for about view
    path('about', views.about, name='aboutpage'),

    # path for contact us view
    path('contact', views.contact, name='contactpage'),
    
    # path for registration
    path('registration', views.registration_request, name='registration'),

    # path for login
    path('login', views.login_request, name='login'),

    # path for logout
    path('logout', views.logout_request, name='logout'),
    
    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)