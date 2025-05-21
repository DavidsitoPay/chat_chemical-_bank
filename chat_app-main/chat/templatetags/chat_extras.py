from django import template
import os

register = template.Library()

@register.filter
def is_image(file_url):
    if not file_url:
        return False
    ext = os.path.splitext(file_url)[1].lower()
    return ext in ['.jpg', '.jpeg', '.png', '.gif']

@register.filter
def is_video(file_url):
    if not file_url:
        return False
    ext = os.path.splitext(file_url)[1].lower()
    return ext in ['.mp4', '.webm']
