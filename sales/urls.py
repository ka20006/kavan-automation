from django.urls import path
from . import views
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("visit/new/", views.new_visit, name="new_visit"),
    path("order/<int:order_id>/", views.order_detail, name="order_detail"),
    path("order/<int:order_id>/whatsapp/", views.whatsapp, name="whatsapp"),
]
