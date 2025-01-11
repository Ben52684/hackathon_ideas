from django.db import models

class Prompt(models.Model):
    user_input = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Prompt {self.id}: {self.user_input[:50]}" 

class Idea(models.Model):
    prompt = models.ForeignKey(Prompt, related_name='ideas', on_delete=models.CASCADE) 
    name = models.CharField(max_length=255)
    description = models.TextField()  
    build_approach = models.TextField()

    def __str__(self):
        return f"Idea {self.id}: {self.name}"
