from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Leave a comment...'
        })

class UserSearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=False)