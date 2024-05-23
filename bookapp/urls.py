from django.urls import path
from .import views


urlpatterns = [

    path('register/', views.userRegistraion, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/',views.logOut,name='logout'),

    path("create-book/",views.createBook,name='createbook'),

    path("author",views.Create_AuthorForm,name="author"),

    path("", views.listBook,name='booklist'),

    path("detailsview/<int:book_id>/", views.detailsView, name='details'),

    path("updateview/<int:book_id>/",views.updateBook, name='update'),

    path("deleteview/<int:book_id>/",views.deleteView, name='delete'),

    path("index",views.index),

    path('search/',views.Search_Book,name='search'),

    # path('register/',views.userRegistraion,name='register'),
    # path('login/',views.loginPage,name='login'),
    path('admin_view/',views.admin_view,name='admin_view'),
    path('user_view/',views.user_view,name='user_view'),


]