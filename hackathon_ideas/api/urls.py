from django.urls import path
from .views import PromptListCreateView

urlpatterns = [
    path('prompts/', PromptListCreateView.as_view(), name='prompt-list-create'),
]