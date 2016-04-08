from django import forms

from .models import Edges,Vertices,Bus

class MyForm(forms.Form): 
    InitialP = forms.CharField(max_length=20)
    FinalP = forms.CharField(max_length=20)