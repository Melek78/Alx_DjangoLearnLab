from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Tag
from django import forms
from django.db.models import Q

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required= True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio", "profile_picture")

class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text='Add tags separated by commas. Example: django, python, tips',
        widget=forms.TextInput(attrs={'placeholder': 'tag1, tag2, tag3'})
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'published_date', 'tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['tags'].initial = ', '.join([t.name for t in self.instance.tags.all()])

    def save(self, commit=True):
        tags_str = self.cleaned_data.pop('tags', '')
        post = super().save(commit=commit)

        new_tags = []
        tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]

        for name in tag_names:
            tag_qs = Tag.objects.filter(name__iexact=name)
            if tag_qs.exists():
                tag_obj = tag_qs.first()
            else:
                tag_obj = Tag.objects.create(name=name)
            new_tags.append(tag_obj)
        post.tags.set(new_tags)
        return post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a comment...'}),
        }