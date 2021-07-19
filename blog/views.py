from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Post

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.

def home(request):
    context = {'posts': Post.objects.all()}
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

# Class based views.

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'                # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'                   # context: object_list
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'          # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'                   # context: object_list
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post                                    # context: object

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post                                    # <app>/<model>_form.html
    fields = ['title', 'content']                   # context: form

    def form_valid(self, form):                     # override form_valid to insert author of post
        form.instance.author = self.request.user
        return super().form_valid(form)
       
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post                                    # <app>/<model>_form.html
    fields = ['title', 'content']                   # context: form

    def form_valid(self, form):                     # override form_valid to insert author of post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post                                    # context: object
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
