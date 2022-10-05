"""elevateSecurity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

from dockets.views import CrushOrderViewSet, FruitIntakeViewSet, ReportsViewSet, DataEntryViewSet

app = "winery"

urlpatterns = [
    path('data-entry/', DataEntryViewSet.as_view(), name='data-entry'),
    path('data-entry/<str:data_type>/', DataEntryViewSet.as_view(), name='data-entry-type'),
    path('fruit-intake/', FruitIntakeViewSet.as_view(), name='fruit-intake'),
    path('fruit-intake/<int:id>/', FruitIntakeViewSet.as_view(), name='fruit-intake-id'),
    path('crush-order/', CrushOrderViewSet.as_view(), name='crush-order'),
    path('crush-order/<int:id>/', CrushOrderViewSet.as_view(), name='crush-order-id'),
    path('reports/', ReportsViewSet.as_view(), name='reports'),
    path('reports/<int:id>/', ReportsViewSet.as_view(), name='reports-id'),
]
