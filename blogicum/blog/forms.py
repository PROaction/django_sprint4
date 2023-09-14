from django import forms

from blog.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'location',
            'category',
        ]
        widgets = {
            'text': forms.Textarea(attrs={'col': 60, 'row': 10})
        }
