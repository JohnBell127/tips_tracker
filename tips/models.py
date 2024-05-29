from django.db import models
from django.contrib.auth.models import User

class Tip(models.Model):
    SHIFT_TYPE_CHOICES = [
        ('cart', 'Cart'),
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    shift_type = models.CharField(max_length=10, choices=SHIFT_TYPE_CHOICES)
    hours_worked = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.user} - {self.date} - ${self.amount} - {self.get_shift_type_display()} - {self.hours_worked} hours"
