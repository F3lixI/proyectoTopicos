from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('login', views.iniciarSesion, name='login'),
    path('listProducts', views.filtrar_productos, name='listProducts'),
    path('detalles/<int:pk>/', views.singleProduct, name='singleProduct'),
    path('logout', views.cerrarSesion, name='logout'),
    path('buscar', views.search, name='search'),
    path('listProducts/<str:category>/', views.listProductsCategory, name='listProductsCategory'),
    path('shoppingCart', views.seeShoppingCart, name='shoppingCart'),
    path('addShoppingCart/<int:pk>/', views.addShoppingCart, name='addShoppingCart'),
    path('removeShoppingCart/<int:pk>/', views.removeShoppingCart, name='removeShoppingCart'),
    path('updateShoppingCart/<int:pk>/', views.updateShoppingCart, name='updateShoppingCart'),
    path('dismuirCantidad/<int:pk>/', views.disminuirCantidad, name='disminuirCantidad'),
]

