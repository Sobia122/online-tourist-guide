"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from users.views import homepage  

urlpatterns = [
        path('', homepage, name='homepage'),  # Now homepage is set

    path('admin/', admin.site.urls),                # Django admin URLs (admin login/logout here)
    path('users/', include('users.urls')),            # Custom user URLs
    path('captcha/', include('captcha.urls')),  # Add this line
    path('activities/', include('activities.urls')),
    path('tips/', include('tips.urls')),
    path('events/', include('events.urls')),
    path('bookings/', include('bookings.urls')),  # ✅ Correct - plural
    path('', include('events.urls')),
    path('destination/<int:pk>/', include('reviews.urls')),  # for detail + review
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('destinations/', include(('destinations.urls', 'destinations'), namespace='destinations')),

    path('destinations/', include(('destinations.urls', 'destinations'), namespace='destinations')),
    path('reviews/', include('reviews.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
