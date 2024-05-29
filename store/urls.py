from django.urls import path
from . import views

urlpatterns=[
    path('',views.home, name='home'),
    path('about/',views.about, name='about'),
    path('login/',views.login_user, name='login'),
    # we are going to create logout url but not page.
    path('logout/',views.logout_user, name='logout'),
    path('register/',views.register_user, name='register'),
    path('update_password/',views.update_password, name='update_password'),
    path('update_user/',views.update_user, name='update_user'),
    path('update_info/',views.update_info, name='update_info'),
    # In this product url we are going to pass the primary key of the product.(for example we will see that product/10 or product/20 etc the number is the primary key of the product.)
    path('product/<int:pk>',views.product,name='product'),
    path('category/<str:foo>', views.category, name='category'),
    path('category_summary/', views.category_summary, name='category_summary'),
    path('search/',views.search,name='search')
]