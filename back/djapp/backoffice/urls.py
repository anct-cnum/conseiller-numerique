from django.urls import path, include

from . import views

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'coaches', views.CoachViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
]

