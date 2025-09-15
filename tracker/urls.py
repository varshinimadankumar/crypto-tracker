from django.urls import path
from django.contrib import admin
from tracker import views
from . import views

app_name = 'tracker'

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("api/prices/", views.api_prices, name="api_prices"),
    path("api/chart/<int:crypto_id>/", views.api_chart, name="api_chart"),
    path("alerts/create/", views.create_alert, name="create_alert"),
]