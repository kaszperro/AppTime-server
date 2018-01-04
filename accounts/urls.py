from django.contrib import admin
from django.urls import path, include
from .views import register_json
urlpatterns = [
    #path('admin/', admin.site.urls),
    #path('accounts/', include('accounts.urls'))
    path('register/', register_json, name='register_json')
]
