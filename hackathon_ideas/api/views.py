from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Prompt, Idea
from .serializers import PromptSerializer
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

class PromptListCreateView(APIView):
    def get(self, request):
        prompts = Prompt.objects.all().order_by('created_at')
        serializer = PromptSerializer(prompts, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        user_input = request.data.get('user_input')
        if not user_input:
            return Response({"error": "user_input is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        prompt = Prompt.objects.create(user_input = user_input)

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages = [
                    {"role": "system", "content" : "You are an assistant that generates hackathon project ideas"},
                    {"role": "user", "content" : f"Generate 3 hackathon project ideas based on: {user_input} and seperate each new idea with two new lines"}
                ]
            )
            generated_text = response['choices'][0]['messages']['content']

            for idea_text in generated_text.split("\n\n"):
                if idea_text.strip():
                    lines = idea_text.split("\n")
                    name = lines[0].strip()
                    description = lines[1].strip() if len(lines) > 1 else ""
                    build_approach = lines[2].strip() if len(lines) > 2 else ""
                    Idea.objects.create(prompt=prompt, name=name, description=description, build_approach=build_approach)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = PromptSerializer(prompt)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
