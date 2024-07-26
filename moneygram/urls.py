from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cards/", views.cards, name="cards"),
    path("earned/", views.earned, name="earned"),
    path("accepted/<int:pk>/", views.accepted, name="accepted"),
    path("transfer/", views.transfer, name="transfer"),
    path("transfer/<str:name>", views.transferd, name="transfered"),
    path("report/", views.report, name="reports"),
]
