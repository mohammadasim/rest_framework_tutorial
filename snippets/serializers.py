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
"""
Dealing with relationships between entities is on the more challenging
aspects of Web API design. There are a number of different ways that we
might choose to represent a relationship.
# Using primary keys.
# Using hperlinking between entities.
# Using a unique identifying slug field on the related entity.
# Using the default string representation of the related entity.
# Nesting the related entity inside the parent representation.
# Some other custom representation.

REST Framework supports all of these styles, and can apply them across
forward or reverse relationships, or apply them across custom managers such as
generic foreign keys.

In this case we would like to use hyperlinked style between entities. In order to do
so we will modify our serializers to extend HyperlinkedModelSerializer instead of the
existing ModelSerializer.
The HyperlinkedModelSerializer has the following differences from ModelSerializer.
# It does not include the id field by default.
# It includes a url field, using HyperlinkedIdentityField.
# Relationships use HyperlinkedRelatedField, instead of PrimaryKeyRelatedField.
"""


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
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
    # We have added a new 'highlight' field. This field is of the
    # same type as the url field, except that it points to the
    # 'snippet-highlight' url pattern, instead of 'snippet-detail' url pattern.

    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight')

    class Meta:
        model = Snippet
        fields = ['url', 'id', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style']

    """
    One nice property that serializers have is that we can inspect all the
    fields in a serializer instance, by printing its representation.
    """


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Because snippets is a reverse relationship on the User model, it will not
    be included by default when using the ModelSerializer class, so we need to
    add an explicit field for it.

    """
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail',
                                                   read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'snippets']
