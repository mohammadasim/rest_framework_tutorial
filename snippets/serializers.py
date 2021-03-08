from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

"""
The SnippetSerializer class is replicating a lot of information that's also
contained in the Snippet model. It would be nice if we could keep our code 
a bit more concise.
In the same way that Django provides both Form classes and ModelForm classes,
REST framework includes both Serializer classes and ModelSerializer classes.
We are now going to replace the serializer class with ModelSerializer.
"""


# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
#
#     def create(self, validated_data):
#         """
#         Create and return a new Snippet instance, given the validated data
#         :param validated_data:
#         :return:
#         """
#         return Snippet.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing Snippet instance, given the validated data
#         :param instance:
#         :param validated_data:
#         :return:
#         """
#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.lineons = validated_data.get('linenos', instance.lineons)
#         instance.language = validated_data.get('language', instance.language)
#         instance.style = validated_data.get('style', instance.style)
#         instance.save()
#         return instance

class SnippetSerializer(serializers.ModelSerializer):
    """
    The model serializer classes don't do anything particularly magical.
    They are simply a shortcut for creating serializer classes.
    They automatically determine the set of fields.
    They provide a simple default implementation of the create() and
    update() methods.
    """
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style']
    """
    One nice property that serializers have is that we can inspect all the
    fields in a serializer instance, by printing its representation.
    """