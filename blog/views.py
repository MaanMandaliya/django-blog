from django.shortcuts import render, get_object_or_404
from .models import Post
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User

class PostListView(ListView):
    model = Post
    #by-default template_name = "<app>/<model>_<viewtype>.html"
    template_name = "blog/home.html"
    #by-default it calls List object
    context_object_name = "posts"
    #Orderby in selecting posts
    ordering = ['-date_posted']
    #pagination
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(date_posted__lte=timezone.now())

class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_posts.html"
    #by-default it calls List object
    context_object_name = "posts"
    #pagination
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user,date_posted__lte=timezone.now()).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(CreateView, LoginRequiredMixin):
    model = Post
    fields = ['title','content']
    #to set post author
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']
    #to set post author
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    # to check author
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    # to check author
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

def about(request):
    context = {
        'title' : "About"
    }
    return render(request,'about.html',context)

