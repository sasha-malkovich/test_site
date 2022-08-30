from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout

# from django.contrib.auth.forms import UserCreationForm , было когда автоматически
# создавали форму и в register form=UserCreation form было

from django.contrib import messages
from django.core.paginator import Paginator

from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm
from .utils import MyMixin


def register(request):
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрированы')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


# def index стал:
class HomeNews(MyMixin, ListView):
    model = News
    # дефолтное имя шаблона имямодели_list и в нем дефолтное имя object_list
    # чтобы это изменить:
    template_name = 'news/index.html'
    context_object_name = 'news'
    # mixin_prop = 'hello'
    paginate_by = 4

    # queryset = News.objects.select_related('category') если не определен get_query_set()

    # для дополнительных СТАТИЧНЫХ данных строка -- extra_context = {'title': 'Главная'}

    # для дополнительных динамичных данных (в примере статика но поебать)
    # (все что в скобках добавляется по умолчанию значит заебись):
    def get_context_data(self, *, object_list=None, **kwargs):
        # мы переопределям по факту метод, поэтому в следующей строке сохраняем данные,
        # по умолчанию хранящиеся как контекст а лишь затем добавляем свои:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        # context['mixin_prop'] = self.get_prop() # {{ mixin_prop }} потом использовать в шаблоне выведет HELLO
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')

#
# def index(request):
#     news = News.objects.all()
#     # news = News.objects.order_by('-created_at') # did it in Meta class
#     # before i found out about rendering:
#     # res = '<h1> СПИСОК НОВОСТЕЙ </h1>'
#     # for item in news:
#     #     res += f'<div>\n<p>{item.title}</p>{item.content}</p>\n</div>\n<hr>\n'
#     # return HttpResponse(res)
#     # categories = Category.objects.all() changed by custom tag
#     context = {
#         'news': news,
#         'title': 'Список новостей',
#         # 'categories': categories, changed by custom tag
#     }
#     return render(request, 'news/index.html', context)


class NewsByCategory(ListView):
    model = News
    template_name = 'news/category.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 4

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context


# before i found out about rendering
# def test(request):
#     return HttpResponse('testovaya stranitsa')

def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    # categories = Category.objects.all() changed by custom tag
    # category = Category.objects.get(pk=category_id) заменено на след строку
    category = get_object_or_404(Category, pk=category_id)
    context = {
        'news': news,
        # 'categories': categories, changed by custom tag
        'category': category,
    }
    return render(request, 'news/category.html', context=context)


class ViewNews(DetailView):
    model = News
    # указываем что первичный ключ приходит от url в виде news_id -- pk_url_kwarg = 'news_id'
    context_object_name = 'news_item'  # default - object


def view_news(request, news_id):
    # news_item = News.objects.get(pk=news_id) заменено на след строку
    news_item = get_object_or_404(News, pk=news_id)
    return render(request, 'news/view_news.html', context={'news_item': news_item})


class AddNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # ВАЖНО что класс ожидает обязательно в наличии у модели метод get_absolute_url, ошибка при его отсутствии
    # поиск при автоматической постройке редиректа (смотри в функции контроллере add_news)
    # но
    # можно самостоятельно построить ссылку, и ошибка будет только если джанго пробует эту
    # построенную ссылку и она не работает ->
    # success_url = reverse_lazy('home')
    # raise_exception = True
    login_url = '/admin/'



# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)  # форма связная с данными
#         if form.is_valid():
#             # нужно для формы не связанной с моделью
#             # news = News.objects.create(**form.cleaned_data)
#             # для формы связанной с моделью:
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()  # форма не связная с данными, при ошибке валидации не нужно будет заново заполнять поля
#     return render(request, 'news/add_news.html', {'form': form})
