
from django.urls import path
from . import views

urlpatterns = [
    path('books', views.gotoBooks, name='books'),
    path('books/<int:id_book>',views.viewEditBook, name='book'),
    path('books/myFavBooks',views.gotoMyBooks, name='mybooks'),
    path('books/new',views.addNewBook, name='newbook'),
    path('books/<int:id_book>/favorite',views.addFavorite, name='addfavorite'),
    path('books/<int:id_book>/unfavorite',views.unFavorite, name='unfavorite'),
    path('books/<int:id_book>/delete',views.deleteBook, name='deleteBook'),
    path('books/update',views.updateBook, name='updateBook'),
]