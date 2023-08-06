from django.urls import path
from .views import BabelfishServiceCreate


urlpatterns = [
    # Other URL patterns
    path('babelfish-service-create/', BabelfishServiceCreate.as_view(), name='babelfish_service_create'),
]
