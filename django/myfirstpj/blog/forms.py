from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-input'}),
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-input form-textarea',
            'rows': 8,
        }),
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'imagen', 'categoria']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['imagen'].widget.attrs.update({
            'class': 'form-input',
        })
