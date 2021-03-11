from django.urls import path, include
from rest_framework.routers import DefaultRouter
from snippets import views

# Create a router and register our viewsets with it.
# The r means that the string is to be treated as a raw string.
# which means all escape codes will be ignored. When a 'r' or 'R' prefix
# is present a character following a backslash is included in the string
# without change, and all backslashes are left in the string.
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]