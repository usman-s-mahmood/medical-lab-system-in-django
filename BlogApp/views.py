from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . import forms
from . import models
from AuthApp import forms as auth_forms
from django.contrib.auth import authenticate
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    services = models.Service.objects.all().order_by('-pk')
    return render(
        request,
        'BlogApp/index.html',
        {
            'services': services,
            'home': True
        }
    )
    
@login_required(login_url='/auth/login')
def add_category(request):
    form = forms.AddCategoryForm(request.POST)
    if not request.user.is_superuser and not request.user.is_staff:
        messages.warning(
            request,
            message=f'Invalid Operation! You are not allowed to visit this page',
            extra_tags='danger'
        )
        return redirect('/auth/dashboard')
    if request.method == 'POST':
        if form.is_valid():
            form.instance.added_by = request.user
            category_name = form.cleaned_data['name']
            category_name = category_name.lower()
            form.instance.name = category_name
            print(form.instance.name)
            form.save()
            messages.success(
                request,
                message=f'Your category is now added to the system!',
                extra_tags='success'
            )
            return redirect('/add-category')
        else:
            messages.warning(
                request,
                message=f'Your form has errors!\n{form.errors}',
                extra_tags='danger'
            )
            return render(
                request,
                'BlogApp/add-category.html',
                {
                    'form': form
                }
            )
    return render(
        request,
        'BlogApp/add-category.html',
        {
            'form': form,
            'add_category': True
        }
    )
    
@login_required(login_url='/auth/login')
def add_post(request):
    if not request.user.is_superuser and not request.user.is_staff:
        messages.warning(
            request,
            message=f'You are not allowed to visit this area!',
            extra_tags='danger'
        )
        return redirect('/auth/dashboard')
    form = forms.AddPostForm(
        request.POST,
        request.FILES
    )
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = request.user
            form.instance.category = request.POST.get('category')
            title = form.instance.title
            title = title.lower()
            form.instance.title = title
            form.save()
            messages.success(
                request,
                message=f'Your post has been added to the system!',
                extra_tags='success'
            )
            title_slug = title.replace(' ', '-')
            return redirect(f'/posts/{title_slug}') 
        else:
            messages.warning(
                request,
                message=f'Your form has errors!\n{form.errors}',
                extra_tags='danger'
            )
            return render(
                request,
                'BlogApp/add-post.html',
                {
                    'form': form,
                    'categories': models.Category.objects.all()
                }        
            )
    return render(
        request,
        'BlogApp/add-post.html',
        {
            'form': form,
            'categories': models.Category.objects.all(),
            'add_post': True
        }
    )
    
@login_required(login_url='/auth/login')
def edit_post(request, id):
    if not request.user.is_superuser and not request.user.is_staff:
        messages.warning(
            request,
            message=f'You are not allowed to visit this area!',
            extra_tags='danger'
        )
        return redirect('/auth/dashboard')
    post_query = models.BlogPosts.objects.filter(id=id).first()
    if post_query is None:
        messages.warning(
            request,
            message=f'Invalid Post ID! No post exists with this ID',
            extra_tags='danger'
        )
        return redirect('/auth/dashboard')
    elif post_query.author.id != request.user.id or not request.user.is_superuser:
        messages.warning(
            request,
            message=f'Invalid Operation! You can not the post of another user',
            extra_tags='danger'
        )
        return redirect('/auth/dashboard')
    form = forms.AddPostForm(
        request.POST or None,
        request.FILES,
        instance=post_query
    )
    if request.method == 'POST':
        if form.is_valid():
            form.instance.category = request.POST.get('category')
            title = form.instance.title
            form.instance.title = title.lower()
            form.save()
            messages.success(
                request,
                message=f'You post has now been edited!',
                extra_tags='success'
            )
            title_slug = form.instance.title
            title_slug = title_slug.replace(' ', '-')
            return redirect(f'/posts/{title_slug}') # -- /post/{title_slug}
        else:
            messages.warning(
                request,
                message=f'Your form has errors!\n{form.errors}',
                extra_tags='danger'
            )
    else:
        form = forms.AddPostForm(
            instance=post_query
        )
        return render(
            request,
            'BlogApp/edit-post.html',
            {
                'form': form,
                'categories': models.Category.objects.all(),
                'edit_post': True
            }
        )
        
@login_required(login_url='/auth/login')
def delete_post(request, id):
    if not request.user.is_superuser and not request.user.is_staff:
        messages.warning(
            request,
            message=f'You are not allowed to visit this area!',
            extra_tags='danger'
        )
        return redirect('/auth/dashboard')
    post_query = models.BlogPosts.objects.filter(id=id).first()
    if post_query is None:
        messages.warning(
            request,
            message=f'Invalid Post ID! No post exists with this ID',
            extra_tags='danger'
        )
        return redirect('/auth/dashboard')
    elif post_query.author.id != request.user.id or not request.user.is_superuser:
        messages.warning(
            request,
            message=f'Invalid Operation! You can not the post of another user',
            extra_tags='danger'
        )
        return redirect('/auth/dashboard')
    form = auth_forms.DeleteConfirmation(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            username = request.user.username
            password = form.cleaned_data['password']
            attempt = authenticate(
                request,
                username=username,
                password=password
            )
            if attempt:
                post_query.delete()
                messages.success(
                    request,
                    message=f'Your post has been deleted!',
                    extra_tags='success'
                )
                return redirect('/auth/dashboard')
            else:
                messages.warning(
                    request,
                    message=f'Invalid Password! Try again',
                    extra_tags='danger'
                )
                return redirect(f'/delete-post/{id}')
        else:
            messages.warning(
                request,
                message=f'You form has errors!\n{form.errors}',
                extra_tags='danger'
            )
            return redirect(f'/delete-post/{id}')
    return render(
        request,
        'BlogApp/delete-post.html',
        {
            'form': form,
            'title': post_query.title,
            'author': post_query.author,
            'delete_post': True
        }
    )
    
def return_categories():
    category_query = models.Category.objects.all()
    return [category.name for category in category_query]
    
def blog_posts(request):
    posts = models.BlogPosts.objects.all().order_by('-pk')
    pagination = Paginator(posts, 2)
    page = request.GET.get('page')
    posts = pagination.get_page(page)
    return render(
        request,
        'BlogApp/blog-posts.html',
        {
            'posts': posts,
            'recents': models.BlogPosts.objects.all().order_by('-pk')[0:3],
            'categories': return_categories,
            'blog': True
        }
    )
    
def post_view(request, slug):
    slug = slug.replace('-', ' ')
    post_query = models.BlogPosts.objects.filter(title = slug).first()
    if post_query is None:
        messages.warning(
            request,
            message=f'Invalid Slug! No post exists with this slug',
            extra_tags='danger'
        )
        return redirect('/posts')
    return render(
        request,
        'BlogApp/post-view.html',
        {
            'post': post_query,
            'recents': models.BlogPosts.objects.all().order_by('-pk')[0:3],
            'categories': return_categories
        }
    )
    
def category_view(request, category):
    category = category.replace('-', ' ')
    category_query = models.Category.objects.filter(name=category).first()
    if category_query is None:
        messages.warning(
            request,
            message=f'Invalid Category provided!',
            extra_tags='danger'
        )
        return redirect('/posts')
    post_query = models.BlogPosts.objects.filter(category=category).all()
    postsNone = False
    if not post_query:
        postsNone = True
    pagination = Paginator(post_query, 2)
    page = request.GET.get('page')
    post_query = pagination.get_page(page)
    return render(
        request,
        'BlogApp/category-view.html',
        {
            'posts': post_query,
            'recents': models.BlogPosts.objects.all().order_by('-pk')[0:3],
            'categories': return_categories,
            'category': category,
            'postsNone': postsNone
        }
    )
    
def search_results(request, query):
    post_query = models.BlogPosts.objects.filter(content__contains = query).all().order_by('-pk')
    post_check = False
    if post_query:
        post_check = True
    pagination = Paginator(post_query, 2)
    page = request.GET.get('page')
    post_query = pagination.get_page(page)
    return render(
        request,
        'BlogApp/search-results.html',
        {
            'posts': post_query,
            'post_check': post_check,
            'recents': models.BlogPosts.objects.all().order_by('-pk')[0:3],
            'categories': return_categories,
            'query': query
        }
    )

def search(request):
    if request.method == 'POST':
        query = request.POST.get('search')
        return redirect(f'/search-results/{query}')
    messages.warning(
        request,
        message=f'You forgot to search!',
        extra_tags='danger'
    )
    return redirect('/')

def search_redirect(request):
    messages.warning(
        request,
        message=f'You forgot to search!',
        extra_tags='danger'
    )
    return redirect('/')

def about_view(request):
    return render(
        request,
        'BlogApp/about.html',
        {
            'about': True
        }
    )
    
def contact_view(request):
    form = forms.ContactForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            form.instance.name = name
            form.instance.email = email
            form.instance.subject = subject
            form.instance.message = message
            form.save()
            messages.success(
                request,
                message=f'Your contact query is submitted!',
                extra_tags='success'
            )
            return redirect('/contact')
        else:
            messages.warning(
                request,
                message=f'Your form has errors!\n{form.errors}',
                extra_tags='danger'
            )
            return render(
                request,
                'BlogApp/contact.html',
                {
                    
                }
            )
    return render(
        request,
        'BlogApp/contact.html',
        {
            'contact': True
        }
    )
    
def not_found(request, exception):
    return render(
        request,
        'BlogApp/404.html',
        status=404
    )
    
def server_error(request):
    return render(
        request,
        'BlogApp/500.html',
        status=500
    )
    
@login_required(login_url='/auth/login')
def add_service(request):
    form = forms.AddServiceForm(request.POST)
    if not request.user.is_superuser and not request.user.is_staff:
        messages.warning(
            request,
            message=f'Invalid Operation! You are not allowed to visit this page',
            extra_tags='danger'
        )
        return redirect('/auth/dashboard')
    if request.method == 'POST':
        if form.is_valid():
            form.instance.added_by = request.user
            service_name = form.cleaned_data['name']
            service_name = service_name.lower()
            form.instance.name = service_name
            form.save()
            messages.success(
                request,
                message=f'Your service is now added to the system!',
                extra_tags='success'
            )
            return redirect('/add-service')
        else:
            messages.warning(
                request,
                message=f'Your form has errors!\n{form.errors}',
                extra_tags='danger'
            )
            return render(
                request,
                'BlogApp/add-service.html',
                {
                    'form': form
                }
            )
    return render(
        request,
        'BlogApp/add-service.html',
        {
            'form': form,
            'add_service': True
        }
    )
    
def newsletter_view(request):
    form = forms.NewsletterForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            email = request.POST.get('email')
            email_query = models.Newsletter.objects.filter(email=email).first()
            if email_query:
                messages.warning(
                    request,
                    message=f'You have already subscribed to our newsletter',
                    extra_tags='danger'
                )
                return redirect('/')
            else:
                form.instance.email = email
                form.save()
                messages.success(
                    request,
                    message=f'Thank you for subscribing to our newsletter!',
                    extra_tags='success'
                )
                return redirect('/')
        else:
            messages.warning(
                request,
                message=f'Your form has errors!\n{form.errors}',
                extra_tags='danger'
            )
            return redirect('/')
    return redirect('/')

def quotation_view(request):
    form = forms.QuotationForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            name = request.POST.get('name')
            email = request.POST.get('email')
            service = request.POST.get('service')
            message = request.POST.get('message')
            form.instance.name = name
            form.instance.email = email
            form.instance.service = service
            form.instance.message = message
            form.save()
            messages.success(
                request,
                message=f'Thank you for submitting your query! We will contact you soon',
                extra_tags='success'
            )
            return redirect('/')
        else:
            messages.warning(
                request,
                message=f'Your form has errors!\n{form.errors}',
                extra_tags='danger'
            )
            return redirect('/')
    return redirect('/')

@login_required(login_url='/auth/login')
def like_post(request, post_id):
    post = models.BlogPosts.objects.filter(id=post_id).first()
    if post is None:
        messages.warning(
            request,
            message=f'Invalid URL! No post exists with this ID',
            extra_tags='danger'
        )
        return redirect('/posts')
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        messages.success(
            request,
            message=f'Post Unliked!',
            extra_tags='warning'
        )
        slug = post.title.replace(' ', '-')
        return redirect(f'/posts/{slug}')
    else:
        post.likes.add(request.user)
        messages.success(
            request,
            'Thank you for liking this post!',
            extra_tags='success'
        )
        slug = post.title.replace(' ', '-')
        return redirect(f'/posts/{slug}')
        
def not_found(request, exception):
    return render(
        request,
        'BlogApp/404.html',
        status=404
    )
    
def server_error(request):
    return render(
        request,
        'BlogApp/500.html',
        status=500
    )