from django.forms import widgets
from django.utils.safestring import mark_safe

class CustomImageField(widgets.ClearableFileInput):

    def render(self, name, value, attrs=None, **kwargs):
        default_html = super().render(name, value, attrs=attrs, **kwargs)
        image_html = mark_safe(f'<img src="{value.url}" width="200" />')

        return f'{image_html}{default_html}'
