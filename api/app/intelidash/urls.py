"""intelidash URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from core.views import (EntryViewSet, EntryTypeViewSet, SourceViewSet, StrandViewSet,
                        InterpretationViewSet, MapEntryViewSet, MapEntryTypeViewSet, MapLayerViewSet, MapDrawingViewSet, MissionViewSet)
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from user.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'missions', MissionViewSet)
router.register(r'entrytypes', EntryTypeViewSet)
router.register(r'sources', SourceViewSet)
router.register(r'strands', StrandViewSet)
router.register(r'entries', EntryViewSet)
router.register(r'interpretations', InterpretationViewSet)
router.register(r'mapentries', MapEntryViewSet)
router.register(r'mapentrytypes', MapEntryTypeViewSet)
router.register(r'maplayers', MapLayerViewSet)
router.register(r'mapdrawings', MapDrawingViewSet)

urlpatterns = [
    url(r'^auth/token/', obtain_jwt_token),
    url(r'^auth/refresh_token/', refresh_jwt_token),
    url(r'^docs/', include('django_mkdocs.urls', namespace='documentation')),
    url(r'^oidc/', include('keycloak_oidc.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
