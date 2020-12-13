from django import forms
from .models import Comment
class CommentForm(forms.ModelForm):
    comment = forms.TextInput(attrs={"placeholder":"Leave Comment"})
    class Meta:
        model = Comment
        fields=["comment"]