from django import forms
from blog.models import Post,Comment

class PostForm(forms.ModelForm):

    class Meta:
        model=Post
        # fiels is a tuple of fields that we want to include in our form
        fields=('author','title','text')

        # widgets is a dictionary of fields that we want to style
        # connectng specific widgets to specific styling
        widgets={
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }

class CommentForm(forms.ModelForm):

    class Meta:
        model=Comment
        # field is a tuple of fields that we want to include in our form
        fields=('author','text')

        # widgets is a dictionary of fields that we want to style
        # connecting specific widgets to specifying style
        widgets={
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
        }