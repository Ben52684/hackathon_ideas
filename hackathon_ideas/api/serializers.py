from rest_framework import serializers
from .models import Prompt, Idea

class IdeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idea
        fields = ['id', 'name', 'description', 'build_approach']

class PromptSerializer(serializers.ModelSerializer):
    ideas = IdeaSerializer(many=True, read_only=True)

    class Meta:
        model = Prompt
        fields = ['id', 'user_input', 'created_at', 'ideas']
        