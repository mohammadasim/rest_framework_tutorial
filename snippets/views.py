from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

"""
To take advantage of the fact that our responses are not longer hardwired to a
single content type, we add support for format suffix to our API endpoints. Using
format suffixes gives us URLs that explicitly refer to a given format, and means our
API will be able to handle URLs such as http://example.com/api/items/4.json
"""


class SnippetList(APIView):
    """
    List al snippets or create a new snippet
    """

    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):
    """
    Retrieve, update or delete snippet instance
    """

    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        serializer = SnippetSerializer(self.get_object(pk))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
