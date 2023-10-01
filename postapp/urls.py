from django.urls import path, include
from postapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="homepage"),
    path('<slug:slug>', views.post_detail, name="post-detail"),
    path('pins/<slug:slug>', views.pin_detail, name="pin-detail"),





]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)