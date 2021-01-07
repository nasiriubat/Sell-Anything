from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import ProductCreateForm
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Product, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.mail import send_mail
import email


class ProductListView(ListView):
    queryset = Product.objects.filter(is_published=True)
    paginate_by = 6
    template_name = 'products/product_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        cat = self.request.GET.get('cat')
        seller = self.request.GET.get('seller')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(categories__icontains=q) |
                Q(user__username__icontains=q) |
                Q(condition__icontains=q) |
                Q(details__icontains=q)
            ).distinct()
        if cat:
            queryset = queryset.filter(categories__icontains=cat)

        if seller:
            queryset = queryset.filter(user__username=seller)

        return queryset

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        post_id = request.POST.get('unlike')
        post_id2 = request.POST.get('like')
        if post_id is not None:
            post = get_object_or_404(Product, id=post_id)
            post.likes.remove(request.user)
        if post_id2 is not None:
            post_id2 = request.POST.get('like')
            post = get_object_or_404(Product, id=post_id2)
            post.likes.add(request.user)
        return redirect('home')






class ProductDetailView(DetailView):
    queryset = Product.objects.all()

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        comment = request.POST.get('comment')
        c_slug = request.POST.get('slug')
        if comment:
            if c_slug:
                post = get_object_or_404(Product, slug=c_slug)
                comment = Comment.objects.create(
                    user=request.user, post=post, text=comment)
                comment.save()
                return redirect('detail', c_slug)
        return redirect('detail', c_slug)


class ProductCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'products/product_form.html'
    form_class = ProductCreateForm
    email='shuvo131662@gmail.com'
    success_url = reverse_lazy('my_products')
    success_message = "Post Created Successfully"
    send_mail(
                            'New product Posted',
                            'Hello, you have a new product request!',
                            'shuvo131662@gmail.com',
                            [email],
                            fail_silently=False
                        )

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = ProductCreateForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('my_products')
    success_message = "Post Updated Successfully"

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)


class ProductDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy('my_products')
    success_message = "Post Deleted Successfully"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)


class MyProductView(LoginRequiredMixin, ListView):
    template_name = 'products/my_products.html'

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)
