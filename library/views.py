from django.shortcuts import render
from django.db.models import Avg, Count
from .models import Book, Author
# Create your views here.

def stats_dashboard(request):
    avg_yr = Book.objects.aggregate(avg_yr = Avg('pub_year'))['avg_yr']
    author_leaderboard = Author.objects.values('id','name').annotate(book_count =Count('books')).order_by('-book_count')
    context = {'avg_yr': round(avg_yr,2) if avg_yr else None,'author_leaderboard': author_leaderboard,}
    return render (request,'library/stats.html',context)