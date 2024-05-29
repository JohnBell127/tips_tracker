from django import forms
from .models import Tip

class TipForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = ['amount', 'shift_type', 'hours_worked']
        widgets = {
            'shift_type': forms.Select(choices=Tip.SHIFT_TYPE_CHOICES),
        }
