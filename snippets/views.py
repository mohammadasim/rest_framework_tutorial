from rest_framework.decorators import action
from rest_framework import viewsets
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


class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list', 'create'
    'retrieve', 'update', and 'destroy' actions.
    Additionally we also provide an extra 'highlight' action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides list and retrieve actions.
    """
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
