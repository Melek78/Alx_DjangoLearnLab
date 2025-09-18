from django import forms

class SearchForm(forms.Form):
    q = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search books..."}),
    )

    # Example of additional validation (strip control chars)
    def clean_q(self):
        q = self.cleaned_data.get("q", "")
        q = q.strip()
        # basic sanitation: disallow some control characters
        q = "".join(ch for ch in q if ord(ch) >= 32)
        return q