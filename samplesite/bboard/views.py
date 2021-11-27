from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from django.core.paginator import Paginator
from django.contrib import messages

from .models import Post, Category
from .forms import PostForm, RegisterUserForm, LoginUserForm, LoginUserForm, CategoryForm


def index(request):
    posts = Post.objects.all()

    paginator = Paginator(posts, 3) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    context = {'posts': posts, 'categories': categories, 'page_obj': page_obj}
    return render(request, 'bboard/index.html', context)


def by_category(request, category_id):
    posts = Post.objects.filter(category=category_id)

    paginator = Paginator(posts, 3) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    current_category = Category.objects.get(pk=category_id)
    context = {'posts': posts, 'categories': categories, 'current_category': current_category, 'page_obj': page_obj}
    return render(request, 'bboard/by_category.html', context)


def by_author(request, author_id):
    posts = Post.objects.filter(author=author_id)

    paginator = Paginator(posts, 3) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    authors = User.objects.all()
    current_author = User.objects.get(pk=author_id)
    categories = Category.objects.all()
    context = {'posts': posts, 'authors': authors, 'current_author': current_author, 'categories': categories, 'page_obj': page_obj}
    return render(request, 'bboard/by_author.html', context)


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'bboard/create.html'
    form_class = PostForm
    success_url = reverse_lazy('index')

    # redirecting for LoginRequiredMixin
    login_url = '/login'
    redirect_field_name = 'next'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)

    def get_context_data(self, **kwards):
        context = super().get_context_data(**kwards)
        context['categories'] = Category.objects.all()
        return context


class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('../')
        
    template_name = 'bboard/create_category.html'
    form_class = CategoryForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwards):
        context = super().get_context_data(**kwards)
        context['categories'] = Category.objects.all()
        return context



class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'bboard/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')

    def get_context_data(self, **kwards):
        context = super().get_context_data(**kwards)
        context['categories'] = Category.objects.all()
        return context

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'bboard/login.html'


    def get_success_url(self):
        return reverse_lazy('index')

    def get_context_data(self, **kwards):
        context = super().get_context_data(**kwards)
        context['categories'] = Category.objects.all()
        return context    

    

def logout_user(request):
    logout(request)
    return redirect('index')




