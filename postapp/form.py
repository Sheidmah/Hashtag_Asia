from .models import Comment, Askformovie
from django import forms


class AskformovieForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'id': "body_comment", 'class': 'wc_comment', 'required': "",'placeholder':"دیدگاه خودت رو ثبت کن..."}))
    name = forms.CharField(widget=forms.TextInput(attrs={'size': "30", 'maxlength': "245", 'class': 'input-comment', 'required': "", 'placeholder':"نام (الزامی)"}))
    email = forms.CharField(widget=forms.TextInput(attrs={'size': "30", 'type': 'email', 'maxlength': "245", 'class': 'input-comment', 'required': "", 'placeholder':"ایمیل (الزامی)"}))
    class Meta:
        model = Askformovie
        fields = ('name', 'email', 'body')

class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'id': "body_comment", 'class': 'wc_comment', 'required': "",'placeholder':"دیدگاه خودت رو ثبت کن..."}))
    name = forms.CharField(widget=forms.TextInput(attrs={'size': "30", 'maxlength': "245", 'class': 'input-comment', 'required': "", 'placeholder':"نام (الزامی)"}))
    email = forms.CharField(widget=forms.TextInput(attrs={'size': "30", 'type': 'email', 'maxlength': "245", 'class': 'input-comment', 'required': "", 'placeholder':"ایمیل (الزامی)"}))

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


