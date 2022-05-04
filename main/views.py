from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.forms.models import model_to_dict
from django.http import JsonResponse


from .models import Book
from .serializers import BookSerializer



# Create your views here.

# Google API key
key = 'AIzaSyD-n3AbS3Srdj78foTxL66ePpG9Jnrma_g'


@api_view(['GET'])
def books(request):

    authors_q = request.GET.get('authors')
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

    print(b)
    serializer = BookSerializer(b, many=True)    
    return Response(serializer.data)    

    # view single book
def index(request, id): 
    b = Book.objects.get(id=id)
    print(b)
    return JsonResponse(model_to_dict(b))

    
    
    



