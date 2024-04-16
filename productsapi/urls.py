from django.urls import path
from . import views
urlpatterns = [
    path('simpleapi',views.simpleapi,name='simple_api'),
    path('signup',views.signup,name='signup_api'),
    path('login', views.login, name='login_api'),
    path('logout', views.logout, name='logout_api'),
    path('create_product', views.create_product, name='createproductapi'),
    path('list_products', views.list_products, name='retrieveproductapi'),
    path('<int:pk>/update_product', views.update_product, name='updateproductapi'),
    path('<int:pk>/delete_product', views.delete_product, name='deleteproductapi'),
    path('<str:mitem>/apisearch', views.apisearch, name='seachproductapi'),

]
    
# "token": "e1eb8a219658b3fd13389ce784be5b351e52ebce"