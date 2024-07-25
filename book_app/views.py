from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .models import *
from django.contrib import messages
from django.http import HttpResponseBadRequest,HttpResponseNotAllowed
from . import models


# Create your views here.
#render the main page
def index(request):
    
    return render(request,'Index.html')

#check if the user not in session can't tgo to success page
def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': get_user(request.session)
        }
        return render(request,'success.html',context)

#handel request post to registration, and pass data to the method to it there are an error shown a msg and redirect to registration page, else create the data and go to the success
def registration(request):
    if request.method == 'POST':
        errors = User.objects.basic_register(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():   
                messages.error(request, value)    
            return redirect('/')
        else:
            user = create_user(request.POST)
            request.session['user_id'] = user.id
            messages.success(request, "Successfully Registered")
            return redirect('/success')
    return redirect('/')

#handel request post to login by user email, and pass data to the method if there are an error display a msg and redirect to main page, else create the data and go to the success page
def login(request):
    if request.method == 'POST':
        errors = User.objects.basic_login(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        user = User.objects.filter(email=request.POST['email']) 
        if user: 
            logged_user = user[0] 
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/books')
        messages.success(request, "Successfully logged in")
        return redirect('/books')
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        return redirect('/')


def books (request): #get data to fill what we need after

    if 'user_id' not in request.session:
        return redirect('/')
    else:
        Books= Book.objects.all() #gets all the records in the table
        context ={ 
            'Books':Books,
            'user': get_user(request.session)}
    
        return render (request,'book.html',context)

#add book
def add_book(request):
    if request.method == 'POST':
        errors = Book.objects.basic_validatebook(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/books')
        # Validate form data and handle errors
        title = request.POST['title']
        description = request.POST['description']
        uploaded_by = get_user(request.session) # Assuming you have a function to get user from session
        # Create new Book object
        book = models.addBook(
            title=title,
            description=description,
            uploaded_by=uploaded_by
        )
        messages.success(request, 'Book added successfully')
    return redirect('/books')

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)    
  
    context = {
        'book': book,
        'liked_users': book.users_who_like.all()
,
        'users': get_user(request.session)  # Assuming this function returns the logged-in user
    }
    return render(request, 'details_book.html', context)
# clear the session of user to logout
def logout(request):
    if request.method=='POST':
        request.session.clear()
        return redirect('/')


#if you upload book you can edit
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        if title and description:
            book.title = title
            book.description = description
            book.save()
            messages.success(request, 'Book updated successfully')
            return redirect('/books')
        else:
            messages.error(request, 'Title and Description are required')
    
    context = {
        'book': book
    }
    return render(request, 'edit_book.html', context)

#confirm delete 
def confirmdelete(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully')
        return redirect('/book')
    
    context = {
        'book': book
    }
    return render(request, 'delete.html', context)
#after confirm delete 
def book_delete(request):
    if request.method == 'POST':
        id = request.POST.get("cid")
        Book=get_object_or_404(models.Book,id=id)
        Book.delete()
    return redirect('/books') 



# def favorite_book(request):
#     if request.method == 'POST':
#         book_id = request.POST.get("cid")
#         book = get_object_or_404(Book, id=book_id)
#         # Check if the user ID is in the session
#         user_id = request.session.get('user_id')
#         print(wholike(book_id))
#         if user_id:
#             # Logic to favorite or unfavorite the book
#             if user_id in book.users_who_like.values_list('id', flat=True):
#                 book.users_who_like.add(user_id)
#                 messages.success(request, f"You have favorited '{book.title}'.")
            
#             return redirect('/books')

    
    # Handle other HTTP methods with a specific response (optional)
    return HttpResponseNotAllowed(['POST'])
#favourite
def favorite_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        user_id = request.session.get('user_id')  # Get user_id from session
        user = get_object_or_404(User, id=user_id)  # Get the user
        
        # Add or remove the user from the book's list of likers
        if user not in book.users_who_like.all():
            book.users_who_like.add(user)  # Add to favorites
        
        return redirect('book_detail', book_id=book_id)  # Redirect to the book detail page

    return redirect('book_detail', book_id=book_id)  # If not POST, redirect anyway

#unfavourite
def unfavorite_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        user_id = request.session.get('user_id')  # Get user_id from session
        user = get_object_or_404(User, id=user_id)  # Get the user
        
        # Remove the user from the book's list of likers
        if user in book.users_who_like.all():
            book.users_who_like.remove(user)
        
        return redirect('book_detail', book_id=book_id)  # Redirect to the book detail page

    return redirect('book_detail', book_id=book_id)