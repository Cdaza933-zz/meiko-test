"""
meiko_store URL Configuration
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import RefreshJSONWebToken

from utils.authtoken.views import ObtainAuthToken

urlpatterns = [
  path('admin/', admin.site.urls),
  # path('docs/', include_docs_urls(title='Invoice API', public=False)),
  path('api-token-auth/', ObtainAuthToken.as_view()),
  path('api-token-refresh/', RefreshJSONWebToken.as_view()),
  path('invoice/', include('invoice.urls', namespace='invoice')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
