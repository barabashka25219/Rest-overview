from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]               # Language + extensions
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS]) # Language list
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])   # highlighting style

class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)                # Set date and time automatically
    title = models.CharField(max_length=100, blank=True, default='') # The field can be empty in forms
    code = models.TextField()                                       
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ['created']