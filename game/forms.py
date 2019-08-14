from django import forms
from .models import Move

class MoveForm(forms.ModelForm):
    class Meta:
        model = Move
        fields = ['move_coordinates']
      