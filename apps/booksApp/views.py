from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..loginApp.models import User
from .models import Book
from django.contrib import messages

#CRUD

def addBookToDB(title, description, id_user):
    user = User.objects.get(id = id_user)
    book = Book.objects.create(
        title = title,
        description = description,
        added_by = user,
    )
    return book

def updateBookOnDB(id_book,title, description):
    book = Book.objects.get(id = id_book)
    book.title = title
    book.description = description
    book.save()
    return book
    

def addFavoriteBookToDB(id_book,id_user):
    user = User.objects.get(id = id_user)
    book = Book.objects.get(id = id_book)
    book.users_who_like.add(user)
    return True

def delFavoriteBookFromDB(id_book,id_user):
    user = User.objects.get(id = id_user)
    book = Book.objects.get(id = id_book)
    book.users_who_like.remove(user)
    return True

def delBookFromDB(id_book):
    book = Book.objects.get(id = id_book)
    book.delete()
    print(book.title)
    return book.title

#MISC
def isfavorite(id_book,id_user):
    if len(User.objects.filter(id = id_user, books_liked__id = id_book)) > 0:
        return True
    return False

def books_filtered(request):
    books = Book.objects.all()
    books_filtered = []
    for book in books:
        data = {
            'book_data' : book,
            'isfavorite': isfavorite(book.id,int(request.session['id'])),
        }
        books_filtered.append(data)
    return books_filtered

#ROUTES
def gotoBooks(request):

    if not "id" in request.session or request.session["id"] == 0:
        return redirect('signin')

    context = {
        'user' : User.objects.get(id = request.session["id"]),
        'books' : books_filtered(request),
        'tipo' : 'allbooks', 
    }
    return render(request,'books.html',context)

def viewEditBook(request, id_book):

    if not "id" in request.session or request.session["id"] == 0:
        return redirect('signin')

    book = Book.objects.get(id = id_book)
    if request.session["id"] == book.added_by.id:
        tipo = "edit"
    else:
        tipo = "view"

    context = {
        'tipo' : tipo,
        'book' : book,
        'username' : User.objects.get(id = request.session['id']).first_name,
    }

    return render(request,'vieweditbook.html',context)

def gotoMyBooks(request):

    if not "id" in request.session or request.session["id"] == 0:
        redirect('signin')

    context = {
        'user' : User.objects.get(id = request.session["id"]),
        'books' : User.objects.get(id = request.session["id"]).books_liked.all(),
        'tipo' : 'favorite', 
    }

    return render(request,'books.html',context)

def addNewBook(request):
    
    if not "id" in request.session or request.session["id"] == 0:
        return redirect('signin')

    errors = Book.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value) 

        context = {
            'title' : request.POST['title'],
            'description' : request.POST['description'],
            'books' : books_filtered(request),
            'user' : User.objects.get(id = request.session["id"]),
            'tipo' : request.POST['tipo'], #allbooks, favorite
        }
            
        return render(request,'books.html',context) #go back to "books/add" keeping data

    else:

        book = addBookToDB(
            title = request.POST['title'],
            description = request.POST['description'],
            id_user = request.session['id'],
        )

        addFavoriteBookToDB(
            id_book = book.id,
            id_user = request.session['id'],
        )

        messages.success(request, f"Book {request.POST['title']} successfully created and added to My Favorites!")

        return redirect('books')

def addFavorite(request, id_book):
    
    if not "id" in request.session or request.session["id"] == 0:
        return redirect('signin')

    addFavoriteBookToDB(
        id_book = id_book,
        id_user = request.session['id'],
    )

    messages.success(request, f"Book { Book.objects.get(id = id_book).title } has been added to My Favorites!")

    return redirect('books')

def unFavorite(request, id_book):
    if not "id" in request.session or request.session["id"] == 0:
        return redirect('signin')

    delFavoriteBookFromDB(
        id_book = id_book,
        id_user = request.session['id'],
    )

    messages.warning(request, f"Book { Book.objects.get(id = id_book).title } has been Un-Favorited!")

    return redirect('book', id_book=id_book)

def deleteBook(request, id_book):

    if not "id" in request.session or request.session["id"] == 0:
        return redirect('signin')   

    if request.session["id"] != Book.objects.get(id = id_book).added_by.id:
        return redirect('books')

    title = delBookFromDB(id_book)

    messages.warning(request, f"Book { title } has been removed!")

    return redirect('books')

def updateBook(request):

    if not "id" in request.session or request.session["id"] == 0:
        return redirect('signin')

    book_set = Book.objects.filter(id = int(request.POST['id_book']))
    if len(book_set) < 1:
        return redirect('books')

    book = book_set[0]

    if request.session["id"] != book.added_by.id:
        return redirect('books')

    errors = Book.objects.book_validator(request.POST,int(request.POST['id_book']))
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value) 

            book.title = request.POST['title']
            book.description = request.POST['description']

            context = {
                'tipo' : 'edit',
                'book' : book,
                'username' : User.objects.get(id = request.session['id']).first_name, 
            }
            
        return render(request,'vieweditbook.html',context)

    else:

        book = updateBookOnDB(
            int(request.POST['id_book']),
            request.POST['title'],
            request.POST['description'],
        )

        messages.success(request, f"Book {request.POST['title']} successfully updated!")

        return viewEditBook(request, int(request.POST['id_book']))


