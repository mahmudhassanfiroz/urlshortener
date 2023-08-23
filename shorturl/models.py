from django.db import models
from django.utils import timezone
from datetime import timedelta 
from django.core.exceptions import ValidationError
from .utils import create_shortened_url


# Create your models here.

class Shortener(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(null=True, blank=True)
    times_followed = models.PositiveIntegerField(default=0)
    long_url = models.URLField()
    short_url = models.CharField(max_length=15, unique=True, blank=True)
    custom_shortcode = models.CharField(max_length=15, unique=True, blank=True, null=True)
    
    class Meta:
        ordering = ['-created']
        
    def __str__(self):
        return f'{self.long_url} to {self.short_url}'
    
    def save(self, *args, **kwargs):
        self.validate_custom_shortcode()
        if not self.short_url:
            self.short_url = create_shortened_url(self)
        if self.last_accessed and (timezone.now() - self.last_accessed) >= timedelta(days=730):
            self.short_url = ''
        self.last_accessed = timezone.now()
        super().save(*args, **kwargs)
        
    def validate_custom_shortcode(self):
        if self.custom_shortcode and Shortener.objects.filter(custom_shortcode=self.custom_shortcode).exists() and self.pk != Shortener.objects.get(custom_shortcode=self.custom_shortcode).pk:
            raise ValidationError("This custom shortcode is already in use.")

    
    


