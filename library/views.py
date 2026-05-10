from django.shortcuts import render
from django.db.models import Avg, Count
from .models import Book, Author
# Create your views here.

def stats_dashboard(request):
    avg_yr = Book.objects.aggregate(avg_yr = Avg('pub_year'))['avg_yr']
    author_leaderboard = Author.objects.values('id','name').annotate(book_count =Count('books')).order_by('-book_count')
    context = {'avg_yr': round(avg_yr,2) if avg_yr else None,'author_leaderboard': author_leaderboard,}
    return render (request,'library/stats.html',context)



from django.shortcuts import render
from .models import Book, Review

def book_review(request, book_id):
    # WITHOUT select_related (bad - N+1 queries)
    # book = Book.objects.get(id=book_id)
    # reviews = book.reviews.all()  # hits DB again
    
    # WITH select_related (good - single query)
    # But note: select_related doesn't work backward (FK to book is automatic)
    book = Book.objects.get(id=book_id)
    review = book.review.select_related('book').all()  # book is already loaded
    
    # Actually, simpler - just get reviews with book prefetched
    review = Review.objects.filter(book_id=book_id).select_related('book')
    
    context = {
        'review': review,
        'book': book,
    }
    return render(request, 'library/reviews.html', context)