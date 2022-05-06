from django.urls import path
from . import views


urlpatterns = [
    path('', views.books),
    path('books', views.books),
    path('books/<int:id>', views.index, name='index'),
    path('<int:id>', views.index, name='index'),
    path('import', views.book_import),
    path('add', views.add)
]
