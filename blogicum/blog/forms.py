from blog.models import Comment, Post
from django import forms


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'image',
            'location',
            'category',
            'pub_date',
        ]
        widgets = {
            'text': forms.Textarea(attrs={'col': 60, 'row': 10}),
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),

        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'text',
        ]
        widgets = {
            'text': forms.Textarea(attrs={'col': 10, 'row': 3})
        }
