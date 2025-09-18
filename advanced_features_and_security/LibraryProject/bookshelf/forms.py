from django import forms

class ExampleForm(forms.Form):
    """A basic form used for demonstration and security tests."""
    title = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Enter book title"})
    )


class SearchForm(forms.Form):
    q = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search books..."})
    )

    def clean_q(self):
        value = self.cleaned_data.get("q", "").strip()
        return "".join(ch for ch in value if ord(ch) >= 32)
