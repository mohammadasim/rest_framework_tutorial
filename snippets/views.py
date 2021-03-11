from rest_framework import generics
from rest_framework.reverse import reverse
from rest_framework import renderers
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

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


@api_view(['GET'])
def api_root(request, format=None):
    """
    Root view to our api
    :param request: 
    :param format: 
    :return: 
    """
    # We are using the rest_framework reverse function, not
    # django reverse
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


"""
Creating an endpoint for the highlighted snippets.
Unlike all our other API endpoints, we don't want to use JSON,
but instead just represent an HTML representation. There are two
styles of HTML renderers provided by REST framework. 
One for dealing with HTML rendered using templates.
The other for dealing with pre-rendered HTML.
We will use the second type of rederer for this endpoint.
"""


class SnippetHighlight(generics.GenericAPIView):
    """
    Instead of using a concrete generic view, we will use
    the base class for representing instances and create our
    own get() method.
    """
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
