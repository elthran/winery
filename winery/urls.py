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

from apps.views.crush_order import CrushOrderViewSet
from apps.views.data_entry import DataEntryViewSet
from apps.views.fruit_intake import FruitIntakeViewSet
from apps.views.lab_analysis import LabAnalysisViewSet
from apps.views.reports_view import ReportsViewSet

app = "winery"

urlpatterns = [
    path('data-entry/', DataEntryViewSet.as_view(), name='data-entry'),
    path('data-entry/<str:data_type>/', DataEntryViewSet.as_view(), name='data-entry-type'),
    path('fruit-intake/', FruitIntakeViewSet.as_view(), name='fruit-intake'),
    path('fruit-intake/<int:id_>/', FruitIntakeViewSet.as_view(), name='fruit-intake'),
    path('crush-order/', CrushOrderViewSet.as_view(), name='crush-order'),
    path('crush-order/<int:id_>/', CrushOrderViewSet.as_view(), name='crush-order'),
    path('lab-analysis/', LabAnalysisViewSet.as_view(), name='lab-analysis'),
    path('reports/', ReportsViewSet.as_view(), name='reports'),
]
