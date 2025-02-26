from rest_framework import serializers
from courses.models import Subject, Course, Module, Content

class SubjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug']

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'title', 'description', 'order']



class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'overview', 'subject',
                'slug', 'modules', 'created','owner' ]        
        
class ItemRelatedField(serializers.RelatedField):
    ''' For Type Content Has a spicfic render method (video, image, text) '''
    def to_representation(self, value):
        return value.render() 

class ContentSerializer(serializers.ModelSerializer):
    item = ItemRelatedField(read_only=True)

    class Meta:
        model = Content
        fields = ['order', 'item']


class ModuleWithContentsSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True)

    class Meta:
        model = Module
        fields = ['order', 'title', 'description', 'contents']


class CourseWithContentsSerializer(serializers.ModelSerializer):
    modules = ModuleWithContentsSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug',
                  'overview', 'created', 'owner', 'modules']