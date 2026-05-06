from django.db import models
from django.utils import timezone

class Book(models.Model):
    """
    Book model representing books in library
    """
    # Different genre choices
    GENRE_CHOICES = [
        ('FIC', 'Fiction'),
        ('NON-FIC', 'Non-Fiction'),
        ('SCI', 'Science Fiction'),
        ('FAN', 'Fantasy'),
        ('BIO', 'Biography'),
        ('MYS', 'Mystery'),
        ('ROM', 'Romance'),
        ('HIS', 'History'),
    ]
    #rating choice 
    RATING_CHOICES = [
        (1, '⭐ - Poor'),
        (2, '⭐⭐ - Fair'),
        (3, '⭐⭐⭐ - Good'),
        (4, '⭐⭐⭐⭐ - Very Good'),
        (5, '⭐⭐⭐⭐⭐ - Excellent'),
    ]
    # Model fields
    title = models.CharField(
        max_length=200,
        help_text="Enter the book title"
    )
    
    author = models.CharField(
        max_length=100,
        help_text="Enter author's name"
    )
    
    genre = models.CharField(
        max_length=20,
        choices=GENRE_CHOICES,
        default='FIC',
        help_text="Select book genre"
    )
    
    published_date = models.DateField(
        help_text="Enter publication date (YYYY-MM-DD)"
    )
    
    rating = models.IntegerField(choices = RATING_CHOICES,default = 5,)

    review = models.TextField(
        blank=True,
        null=True,
        help_text="Write your review here (optional)"
    )
    # Optional: Add metadata fields (good practice)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Define string representation
    def __str__(self):
        return f"{self.title} by {self.author}"
    
    # Meta class for ordering
    class Meta:
        ordering = ['-published_date']  # Most recent first
        verbose_name = "Book"
        verbose_name_plural = "Books"
        # Helper method to check if book is popular
    def is_popular(self):
        return self.rating >= 4
    # Optional: Add validation
    def save(self, *args, **kwargs):
        # Ensure published_date is not in future
        if self.published_date and self.published_date > timezone.now().date():
            raise ValueError("Published date cannot be in the future")
        super().save(*args, **kwargs)