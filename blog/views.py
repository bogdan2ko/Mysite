from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm, SearchForm
from django.views.generic import ListView
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank




class PostListView(ListView):
    queryset = Post.objects.all().select_related("author")
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

    

# def post_list(request):
#     object_list=Post.published.all()
#     paginator=Paginator(object_list,3) #о 3 статьи на каждой странице.
#     page=request.GET.get("page")
#     try:
#         posts=paginator.page(page)
#     except PageNotAnInteger:
#         # Если страница не является целым числом, возвращаем первую страницу.
#         posts = paginator.page(1)
#     except EmptyPage:
#         # Если номер страницы больше, чем общее количество страниц, возвращаем последнюю.
#         posts = paginator.page(paginator.num_pages)
#     return render(request,'blog/post/list.html', {'page': page, 'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post.objects.select_related('author'), slug=post, status='published',publish__year=year,
                             publish__month=month,publish__day=day)
    # Список активных комментариев для этой статьи.
    comments = post.comments.filter(active=True)
    new_comment = None
    comment_form = CommentForm()  # Инициализировать переменную значением по умолчанию
    if request.method == 'POST':
        # Пользователь отправил комментарий.
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Создаем комментарий, но пока не сохраняем в базе данных.
            new_comment = comment_form.save(commit=False)
            # Привязываем комментарий к текущей статье.
            new_comment.post = post
            # Сохраняем комментарий в базе данных.
            new_comment.save()
    return render(request,'blog/post/detail.html',{'post': post,
                                                   'comments': comments,
                                                   'new_comment': new_comment,
                                                   'comment_form': comment_form})



def post_share(request, post_id):
    # Получение статьи по идентификатору.
    post = get_object_or_404(Post.published.select_related('author'), id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Форма была отправлена на сохранение.
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Все поля формы прошли валидацию.
            cd = form.cleaned_data
            # ... Отправка электронной почты.
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:\n{}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail=(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


from django.shortcuts import render
from django.contrib.postgres.search import SearchVector
from .forms import SearchForm
from .models import Post

def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.annotate(search=SearchVector('title', 'body'),).filter(search=query)
    return render(request, 'blog/post/search.html', {'form': form, 'query': query, 'results': results})