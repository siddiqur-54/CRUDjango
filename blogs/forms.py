from django import forms
from blogs.models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content']
        widgets = {
            'title' : forms.TextInput(attrs={'placeholder':'Enter Title'}),
            'content' : forms.Textarea(attrs={'placeholder':'Enter Content'})
        }


    def clean(self):
        data = self.cleaned_data
        title = data.get("title")
        qs = Blog.objects.filter(title__icontains=title)
        if self.instance and self.instance.id:
            qs=qs.exclude(id=self.instance.id)
        if qs.exists():
            self.add_error("title", f"\"{title}\" is already in use. Please pick another title.")
            raise forms.ValidationError("Similar title is not allowed")
        return data