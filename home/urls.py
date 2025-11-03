"""
URL configuration for home project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# --- Add these two imports ---
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Backwards-compatible redirect: some links may point to /admin/start-chat/<id>/
    # but Django's admin captures the 'admin/' space. Redirect here to the
    # new application route which lives outside the admin namespace.
    path('admin/start-chat/<int:user_id>/', lambda req, user_id: redirect('webapp:admin_start_chat', user_id=user_id)),
    path('admin/', admin.site.urls),
    path('', include('webapp.urls')),
    path('chat/', include('chat.urls')),
]

# --- Add this block at the end ---
# This line is what allows images to be served in development mode.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

