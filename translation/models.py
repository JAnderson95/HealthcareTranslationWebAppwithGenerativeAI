from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TranslationSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    input_language= models.CharField(max_length=50)
    output_language= models.CharField(max_length=50)
    created_at= models.DateTimeField(auto_now_add=True)
    session_id= models.CharField(max_length=100, unique=True)

    class Meta:
        permissions=[
            ("view_patient_data","can view patien translation data"),
        ]

class TranslationRecord(models.Model):
    session= models.ForeignKey(TranslationSession, on_delete=models.CASCADE)
    original_text=models.TextField()
    translated_text= models.TextField()
    original_audio= models.BinaryField(null=True, blank=True)
    transtaled_audio= models.BinaryField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Traduccion {self.id}"


