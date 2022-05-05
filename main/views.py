from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.forms.models import model_to_dict
from django.http import JsonResponse
import json



from .models import Book
from .serializers import BookSerializer



# Create your views here.

# Google API key
key = 'AIzaSyD-n3AbS3Srdj78foTxL66ePpG9Jnrma_g'


@api_view(['GET']) #GET, PATCH, DELETE
def books(request):

    authors_q = request.GET.get('author')
    title_q = request.GET.get('title')
    acquired_q = request.GET.get('acquired')
    from_q = request.GET.get('from')
    to_q = request.GET.get('to')


    if authors_q == None:
        authors_q = ''
    if title_q == None:
        title_q = ''
    if from_q == None:
        from_q = '0'
    if to_q == None:
        to_q = '9999'

    # filtered view
    if acquired_q == None:
        b = Book.objects.filter(
                authors__icontains=authors_q).filter(
                title__icontains=title_q).filter(
                published_year__gte=from_q).filter(
                published_year__lte=to_q)
    else:
        b = Book.objects.filter(
                authors__icontains=authors_q).filter(
                title__icontains=title_q).filter(
                published_year__gte=from_q).filter(
                published_year__lte=to_q).filter(
                acquired=acquired_q)

    serializer = BookSerializer(b, many=True)    
    return Response(serializer.data)    


@api_view(['GET', 'PATCH', 'DELETE'])
    # view single book
def index(request, id):
    if request.method == 'GET':
        b = Book.objects.get(id=id)
        return JsonResponse(model_to_dict(b))
    elif request.method == 'PATCH':
        b = Book.objects.get(id=id)
        body = request.body.decode('utf=8')
        body_dict = eval(body)
        
        
        if 'title' in body_dict:
            print('wszedl title')
            b.title = body_dict['title']
            b.save()
            
        if 'author' in body_dict:
            print('wszedl author')
            b.authors = body_dict['author']
            b.save()
        
        if 'published_year' in body_dict:
            print('wszedl published_year')
            b.published_year = body_dict['published_year']
            b.save()
        
        if 'external_id' in body_dict:
            print('wszedl external_id')
            b.external_id = body_dict['external_id']
            b.save()
        
        if 'acquired' in body_dict:
            print('wszedl acquired')
            b.acquired = body_dict['acquired']
            b.save()
        
        if 'thumbnail' in body_dict:
            print('wszedl thumbnail')
            b.thumbnail = body_dict['thumbnail']
            b.save()
        
        b = Book.objects.get(id=id)
        return JsonResponse(model_to_dict(b))
    
    
    elif request.method == 'DELETE':
        b = Book.objects.get(id=id)
        b.delete()
        return HttpResponse()




@api_view(['POST'])
def book_import(request):  
    body = request.body.decode('utf=8')
    body_dict = eval(body)
    q = 'inauthor:' + body_dict['author']
    
    queries = {'q': q, 'key': key, 'maxResults':40}
    r = requests.get('https://www.googleapis.com/books/v1/volumes', params=queries)
    print(r)
    if r.status_code != 200:
        return HttpResponse(('Sorry, we found problem with Google Books. Try again later.'))

    data = r.json()
    
    if not 'items' in data:
        return HttpResponse('Sorry, no books match that search term.')

    fetched_books = data['items']
    books = []
    for book in fetched_books:
        book_dict = {
            'title': book['volumeInfo']['title'],
            'external_id': book['id'] if 'id' in book else "",           
            'thumbnail': book['volumeInfo']['imageLinks']['thumbnail'] if 'imageLinks' in book['volumeInfo'] else "",
            'authors': ", ".join(book['volumeInfo']['authors']) if 'authors' in book['volumeInfo'] else "",
            'published_year': book['volumeInfo']['publishedDate'] if 'publishedDate' in book['volumeInfo'] else "",
            'popularity': book['volumeInfo']['ratingsCount'] if 'ratingsCount' in book['volumeInfo'] else 0
        }
        book_dict['published_year'] = book_dict['published_year'][:4]
        books.append(book_dict)
        
    number_of_imported_books = 0
    
    for b in books:
        if not Book.objects.filter(external_id=b['external_id']).exists():
            book = Book(title=b['title'],
                        authors=b['authors'],
                        published_year=b['published_year'],
                        external_id=b['external_id'],
                        acquired=False,
                        thumbnail=b['thumbnail'],
                    )
            book.save()
            number_of_imported_books += 1
                        
    response_data = {
        "imported": number_of_imported_books
    }            
    return JsonResponse(response_data)

    



