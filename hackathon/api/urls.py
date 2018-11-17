
from django.urls import path,include
from .views import postout
# from .views import speechtotext

urlpatterns = [
    path('post/',postout),
    # path('speechtotext/',speechtotext),
]
