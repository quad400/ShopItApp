from django import forms

from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'content','rate']

class SearchForm(forms.Form):
    query = forms.CharField(max_length=225)
    category_id = forms.IntegerField()