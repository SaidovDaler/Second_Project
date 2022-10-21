from django.shortcuts import render, redirect
from crud_app.models import Article, Comment
from .forms import ArticleForm 
from .forms import CommentForm
from django.db.models import Q
# Create your views here.

def article_func(request):
    search = request.GET.get('search')
    articles = Article.objects.all().order_by('date')
    articles = articles.filter(Q(title__icontains=search) | Q(text__icontains=search)) if search else articles
    return render (request, 'articles_list.html', {'articles': articles})



def article_create(request):
    form = ArticleForm(request.POST or None, request.FILES)
    if request.method == 'POST' and form.is_valid():
        inctance = form.save(commit=False)
        inctance.author = request.user
        inctance.save()
        return redirect('article_func')
    form = ArticleForm()
    return render(request, 'article_create.html', {'form': form})

def article_edit(request, slug):
    article=Article.objects.get(slug=slug)
    form=ArticleForm(request.POST or None, request.FILES or None, instance=article)
    if form.is_valid():
        form.save()
        return redirect('article_detail', slug=slug)
    return render(request, 'edit_aricle.html', {"form": form, 'article': article})

def article_delete(request,slug):
    article = Article.objects.get(slug=slug)
    if request.method == 'POST':
        article.delete()
        return redirect('article_func')
    return render(request, 'article_delete.html', {'article': article})   


def like_article(request, slug):
    article=Article.objects.get(slug=slug)

    if request.user not in article.likes.all():
        article.likes.add(request.user)
        article.dislikes.remove(request.user)
    elif request.user in article.likes.all():
        article.likes.remove(request.user)
    return redirect('article_detail', slug=slug)

        

def dislike_article(request, slug):
    article=Article.objects.get(slug=slug)

    if request.user not in article.dislikes.all():
        article.dislikes.add(request.user)
        article.likes.remove(request.user)
    elif request.user in article.dislikes.all():
        article.dislikes.remove(request.user)
    return redirect('article_detail', slug=slug)


def article_detail(request, slug):
    article = Article.objects.get(slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
           instance = form.save(commit=False)
           instance.user = request.user
           instance.article = article
           instance.save()
           return redirect('article_detail', slug=slug)
    form = CommentForm()
    return render(request, 'article_detail.html', {'article': article, 'form':form})       


def delete_comment(request, slug, pk):
    comment = Comment.objects.get(pk=pk)
    if request.method == 'POST':
        comment.delete()
        return redirect('article_detail', slug=slug)
    return render(request, 'comment_delete.html', {"comment": comment})


def edit_comment(request, slug, pk):
    comment =  Comment.objects.get(pk=pk)
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect('article_detail', slug=slug)
    return render(request, "comment_edit.html", {"form": form,
    'article': comment.article})    
   

