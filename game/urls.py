from django.urls import path

from django.contrib.auth.views import LoginView

from .views import GameDetailView
from .views import GameCreateView

urlpatterns = [
    path('create/', GameCreateView.as_view(), name="create"),
    path('<uuid:pk>', GameDetailView.as_view(), name='GameDetailView'),
      path('login/', LoginView.as_view(), name="login"),
]