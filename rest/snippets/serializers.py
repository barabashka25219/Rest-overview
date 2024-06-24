# Serializers destroy python data and moving that into JSON format.

from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)                   # PK field of model Snippet
    title = serializers.CharField(required=False, allow_blank=True) # Not required, may be empty 
    code = serializers.CharField(style={'base_template': 'textarea.html'}) # 'style' like 'widget' in forms (how the field should be rendered)
    lineos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')


    def create(self, validated_data):
        """ 
        Create new instance of the model
    
        :type validated_data:
        :param validated_data: 
    
        :rtype: :class:Snippet
        """    
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """ 
        Update existing instance
    
        :type instance:
        :param instance:
    
        :type validated_data:
        :param validated_data:
    
        :rtype:
        """
        instance.title   = validated_data.get('title', instance.title)
        instance.code    = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style   = validated_data.get('style', instance.style)

        instance.save()

        return instance
    

# more short serializer definition that previous
# based on ModelSerializer
class SnippetSerializerShort(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style']

    def create(self, validated_data):
        """ 
        Create new instance of the model
    
        :type validated_data:
        :param validated_data: 
    
        :rtype: :class:Snippet
        """    
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """ 
        Update existing instance
    
        :type instance:
        :param instance:
    
        :type validated_data:
        :param validated_data:
    
        :rtype:
        """
        instance.title   = validated_data.get('title', instance.title)
        instance.code    = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style   = validated_data.get('style', instance.style)

        instance.save()

        return instance
    

# Actions with serializers
# 
# import io
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser
#
# Serialize Snippet instance:
# __________________________________________________
# snippet = Snippet(code='print("hello, world")**n')
# serializer = SnippetSerializer(snippet)
# jsonContent = JSONRenderer().render(serializer.data)
#
# Deserialize Snippet existing in JSON format:
# __________________________________________________
# stream = io.BytesIO(content)
# data = JSONParser().parse(stream)