from django.urls import path
from.import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register', views.register, name="register"),
    path('login', views.login_page, name="login"),
    path('logout', views.logout_page, name="logout"),
    path('cart', views.cart_page, name="cart"),
    path('favourite', views.favourite_page, name="favourite"),
    path('favviewpage', views.favviewpage, name="favviewpage"),
    path('delete_cart/<str:cid>', views.delete_cart, name="delete_cart"),
    path('delete_fav/<str:fid>', views.delete_fav, name="delete_fav"),
    path('collection', views.collection, name="collection"),
    path('collection/<str:name>', views.collectionview, name="collection"),
    path('collection/<str:cname>/<str:pname>', views.product_details, name="product_details"),
    path('addtocart', views.add_to_cart, name="addtocart"),
]    