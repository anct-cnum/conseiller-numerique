"""djapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path

from . import views


urlpatterns = [
    path('', views.home),
    path('admin/', admin.site.urls),
]


if settings.MAINTENANCE:
    urlpatterns += [
        re_path('api/.*', views.api_maintenance),
    ]
else:
    urlpatterns += [
        path('api/coaches.add', views.CoachAddView.as_view()),
        path('api/coach.confirm_email', views.CoachConfirmEmailView.as_view()),
        path('api/hostorganizations.add', views.HostOrganizationAddView.as_view()),
        path('api/hostorganization.confirm_email', views.HostOrganizationConfirmEmailView.as_view()),
        path('api/matchings.get_by_key/<str:key>', views.MatchingGetView.as_view()),
        path('api/matchings.coach_accept/<str:key>', views.matching_coach_accept, name='matching-coach-accept'),
        path('api/matchings.coach_reject/<str:key>', views.matching_coach_reject, name='matching-coach-reject'),
        path('api/matchings.host_accept/<str:key>', views.matching_host_accept, name='matching-host-accept'),
        path('api/matchings.host_reject/<str:key>', views.matching_host_reject, name='matching-host-reject'),
        path('redirect/coach.confirm_email/<str:key>', views.redirect_coach_confirm_email,
             name='redirect-coach-confirm-email'),
        path('redirect/host.confirm_email/<str:key>', views.redirect_host_confirm_email,
             name='redirect-host-confirm-email'),
    ]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
