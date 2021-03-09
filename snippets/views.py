from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from snippets.serializers import UserSerializer
from snippets.permissions import IsOwnerOrReadOnly

"""
To take advantage of the fact that our responses are not longer hardwired to a
single content type, we add support for format suffix to our API endpoints. Using
format suffixes gives us URLs that explicitly refer to a given format, and means our
API will be able to handle URLs such as http://example.com/api/items/4.json
"""


class SnippetList(generics.ListCreateAPIView):
    """
    List al snippets or create a new snippet
    """

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete snippet instance
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer