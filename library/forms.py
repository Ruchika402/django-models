from django import forms
from .models import Book,Review

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title','author','pub_year']
        widgets = {
            'pub_year':forms.NumberInput(attrs={'placeholder':'e.g., 1997'}),

        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer_name', 'rating', 'comment']
        widgets = {
            'reviewer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }   