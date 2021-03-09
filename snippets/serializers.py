from rest_framework import serializers
from django.contrib.auth.models import User
from snippets.models import Snippet

"""
The SnippetSerializer class is replicating a lot of information that's also
contained in the Snippet model. It would be nice if we could keep our code 
a bit more concise.
In the same way that Django provides both Form classes and ModelForm classes,
REST framework includes both Serializer classes and ModelSerializer classes.
We are now going to replace the serializer class with ModelSerializer.
"""


class SnippetSerializer(serializers.ModelSerializer):
    """
    The model serializer classes don't do anything particularly magical.
    They are simply a shortcut for creating serializer classes.
    They automatically determine the set of fields.
    They provide a simple default implementation of the create() and
    update() methods.
    Now that we have updated the view that creates snippet to associate
    owner with snippet, we need to update the snippetSerializer class.
    We add owner field. The source argument controls which attribute is
    used to populate a field and can point at any attribute on serialized
    instance, which in this case is the User. It can also take the dotted notation shown below
    in which case it will traverse the given attribute, in a similar way as it is used
    with Django's template language.
    The field that we have added is untyped ReadOnlyField class, in contrast to the
    other typed fields such as charfield, BooleanField, etc.
    The untyped ReadOnlyField is always read-only and will be used to serialized
    representation, but will not be used for updating model instances when they
    are deserialized. We could have also used CharField(read_only=True) here.
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style', 'owner']

    """
    One nice property that serializers have is that we can inspect all the
    fields in a serializer instance, by printing its representation.
    """


class UserSerializer(serializers.ModelSerializer):
    """
    Because snippets is a reverse relationship on the User model, it will not
    be included by default when using the ModelSerializer class, so we need to
    add an explicit field for it.

    """
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']

