from django.urls import path

from .views import GameDetailView

urlpatterns = [
    path('<uuid:pk>', GameDetailView.as_view(), name='GameDetailView'),
]