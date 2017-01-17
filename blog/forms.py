from django.forms import (ModelForm, CheckboxSelectMultiple, Form, CharField, TextInput)
from .models import Post, Tag


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'body', 'tags')
        widgets = {
            'tags': CheckboxSelectMultiple(),
        }


class TagForm(ModelForm):

    class Meta:
        model = Tag
        fields = '__all__'


class SearchForm(Form):
    comment = CharField(label='', required=True, max_length=100, widget=TextInput(attrs={'placeholder': 'Search'}))
