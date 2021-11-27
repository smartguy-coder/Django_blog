from django.urls import path, include

from .views import index, by_category, PostCreateView, by_author, login, logout_user, RegisterUser, LoginUser, CategoryCreateView


urlpatterns = [
    path('', index, name='index'),
    path('<int:category_id>/', by_category, name='by_category'),
    path('add/', PostCreateView.as_view(), name='add'),
    path('add_category/', CategoryCreateView.as_view(), name='add_category'),
    path('author/<int:author_id>/', by_author, name='by_author'),
    path('registration/', RegisterUser.as_view(), name='registration'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
   
]

