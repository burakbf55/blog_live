from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls.base import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import CommentForm
from blogapp.models import Blog, Comment
from django.views.generic import ListView
# Create your views here.

class BlogList(ListView):
    model = Blog
    template_name = 'home.html'



class BlogDetail(LoginRequiredMixin,DetailView):
    model = Blog
    template_name = 'post_detail.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        
        form = CommentForm()
        post = get_object_or_404(Blog, pk=pk,)
        comments = post.comment_set.all()

        context['post'] = post
        context['comments'] = comments
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        post = Blog.objects.filter(id = self.kwargs['pk'])[0]
        comments = post.comment_set.all()

        context['post'] = post
        context['comments'] = comments
        context['form'] = form

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            content = form.cleaned_data['content']

            comment = Comment.objects.create(
                name=name, email=email, content= content, post=post
            )
            form = CommentForm()
            context['form'] = form
            return self.render_to_response(context=context)
        
        return self.render_to_response(context=context)

class BlogCreate(LoginRequiredMixin,CreateView):
    model = Blog
    template_name = 'post_yeni.html'
    fields = '__all__'

class BlogUpdate(LoginRequiredMixin,UpdateView):
    model = Blog
    template_name = 'post_edit.html'
    fields = ['title', 'body']
    login_url = 'login'

    def dispatch(self, request,*args,**kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request,*args,**kwargs)


class BlogDelete(LoginRequiredMixin,DeleteView):
    model = Blog
    template_name = 'post_silme.html'
    success_url = reverse_lazy("home")
    login_url = 'login'

    def dispatch(self, request,*args,**kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request,*args,**kwargs)