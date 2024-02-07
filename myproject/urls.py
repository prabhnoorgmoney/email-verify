"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# myproject/urls.py

from django.contrib import admin
from django.urls import path
from myapp.views import combined_function
# from myapp.views import check_email_existence

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('val/', check_email_existence, name='validate_and_verify_email'),
    path('val/', combined_function, name='validate_and_verify_email'),

]

