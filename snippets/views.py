from rest_framework import generics

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

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


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete snippet instance
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

