"""
If you open a browser and navigate to the browsable API at the
moment, you will find that you are no longer able to create
new code snippets. In order to do so we would need to be able
to login as a user.
We can add a login view for use with the browsable API
by ending the URLConf in out project-level file
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth', include('rest_framework.urls')),
    path('', include('snippets.urls')),
]
