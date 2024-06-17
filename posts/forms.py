from django import forms

from posts.models import Post


class PostForm(forms.ModelForm):
    title = forms.CharField(
        label='Заголовок',
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        max_length=120
    )

    slug = forms.SlugField(
        label='Ссылка',
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        max_length=120
    )

    body = forms.CharField(
        label='Текст',
        widget=forms.Textarea(attrs={'class': 'form-control', "id": "TextArea",
                                     'style': 'overflow: hidden; white-space: normal;'})
    )

    class Meta:
        model = Post
        fields = ['title', 'slug', 'body']

    # def __init__(self, *args, **kwargs):
    #     super(PostForm, self).__init__(*args, **kwargs)
    #     if kwargs.get('instance'):
    #         self.fields['group'].initial = kwargs['instance'].group_id
