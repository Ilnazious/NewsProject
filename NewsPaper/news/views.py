from django.contrib.auth.models import Group
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.http import urlencode
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Post, Author
from .filters import PostFilter
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib import messages

class PostsList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['all_posts'] = Post.objects.all()
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

#Функции создания, обновления и удаления

class NewsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'

    def get_success_url(self):
        base_url = reverse_lazy('news_list')  # Используем новое имя URL
        query_params = urlencode({'page': 1})
        return f"{base_url}?{query_params}"

    def form_valid(self, form):
        # Получаем или создаем автора для пользователя
        author, created = Author.objects.get_or_create(authorUser=self.request.user)
        form.instance.author = author
        form.instance.categoryType = Post.NEWS
        return super().form_valid(form)

class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'

    def get_success_url(self):
        base_url = reverse_lazy('news_list')
        query_params = urlencode({'page': 1})
        return f"{base_url}?{query_params}"

    def get_queryset(self):
        return super().get_queryset().filter(categoryType=Post.NEWS)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author.authorUser != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_confirm_delete.html'

    def get_success_url(self):
        base_url = reverse_lazy('news_list')
        query_params = urlencode({'page': 1})
        return f"{base_url}?{query_params}"

    def get_queryset(self):
        return super().get_queryset().filter(categoryType=Post.NEWS)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author.authorUser != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class ArticleCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'

    def get_success_url(self):
        base_url = reverse_lazy('news_list')
        query_params = urlencode({'page': 1})
        return f"{base_url}?{query_params}"

    def form_valid(self, form):
        author, created = Author.objects.get_or_create(authorUser=self.request.user)
        form.instance.author = author
        form.instance.categoryType = Post.ARTICLE
        return super().form_valid(form)

class ArticleUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'

    def get_success_url(self):
        base_url = reverse_lazy('news_list')
        query_params = urlencode({'page': 1})
        return f"{base_url}?{query_params}"

    def get_queryset(self):
        return super().get_queryset().filter(categoryType=Post.ARTICLE)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author.authorUser != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class ArticleDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_confirm_delete.html'

    def get_success_url(self):
        base_url = reverse_lazy('news_list')
        query_params = urlencode({'page': 1})
        return f"{base_url}?{query_params}"

    def get_queryset(self):
        return super().get_queryset().filter(categoryType=Post.ARTICLE)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author.authorUser != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

@login_required
def become_author(request):
    authors_group = Group.objects.get(name='authors')
    request.user.groups.add(authors_group)
    return redirect('/accounts/email')