
from django import forms 
from .models import Shortener

class ShortenerForm(forms.ModelForm):
    long_url = forms.URLField(widget=forms.URLInput(
        attrs={"class": "form-control form-control-lg", "placeholder": "Your URL to shorten"}
    ))
    
    custom_shortcode = forms.CharField(max_length=15, required=False, widget=forms.TextInput(
        attrs={"class": "form-control form-control-lg", "placeholder": "Custom Shortcode (optional)"}
    ))
    
    class Meta:
        model = Shortener
        fields = ['long_url', 'custom_shortcode']
        

