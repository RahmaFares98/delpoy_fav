from django.urls import path
from . import views


handler404 = 'book_app.views.error_404'
handler500 = 'book_app.views.error_500'

urlpatterns = [
    path('', views.index ),
    path('registration',views.registration),
    path('login',views.login),
    path('logout',views.logout),
    path('success',views.success),
    path('books', views.books),
    path('addbook',views.add_book),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('favorite/<int:book_id>', views.favorite_book, name='favorite_book'),
    path('unfavorite/<int:book_id>', views.unfavorite_book, name='unfavorite_book'),
    path('book/<int:book_id>/edit/', views.edit_book, name='edit_book'),
    path('book/<int:book_id>/delete/', views.confirmdelete, name='confirmdelete'),
    path('book_delete', views.book_delete ,name='book_delete'),

]