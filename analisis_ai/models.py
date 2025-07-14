from django.db import models

# Create your models here.
from django.db import models

# --- MODEL TO STORE PREDICTION RESULTS ---
class HealthPredictionResult(models.Model):
    session = models.ForeignKey('session_app.Session', on_delete=models.CASCADE, related_name='predictions')
    health_recommendation = models.TextField()  # Health recommendation message
    criteria_details = models.JSONField()  # Store details as JSON
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of prediction creation

    def __str__(self):
        return f'Prediction {self.session.id} - Recommendation: {self.health_recommendation}'
