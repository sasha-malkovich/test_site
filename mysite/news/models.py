from django.db import models
from django.urls import reverse_lazy


class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    content = models.TextField(blank=True, verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменено')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    views = models.IntegerField(default=0)

    # Формирование обратной связи: т.е.получение всех новостей, связанных с определенной категорией
    # формат: первичная_модель. < имя_связанной(вторичной)_модели > _set.all()
    # cat4 = Category.objects.get(pk=4)
    # cat4.news_set.all()  # получить данные из этого сета можно циклом
    # ФОРМАТ МОЖНО ИЗМЕНИТЬ в модели атрибут foreighkey related_name ='get_news' или другое

    # null True in category потому что уже создана модель была частично и сейчас допустить иначе нельзя
    # в уже созданных новостях "нарушение целостности данных" при попытке

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at', 'title']

    def get_absolute_url(self):
        # return reverse_lazy('view_news', kwargs={'news_id': self.pk})
        return reverse_lazy('view_news', kwargs={'pk': self.pk})


class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name='Наименование категории')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

    # в этом случае можно было использовать reverse но reverse_lazy можно использовать всегда
    # как аргументы используются 1- имя маршрута (данное в urls) 2- словарь в необходимыми для
    # построения ссылки значениями (ключ как имя из urls)
    # работа функции крайне схожа с работой тега {% url... %}
    # в шаблонах {% url 'category' item.pk %} меняется на {{ item.get_absolute_url }}
    # метод с именно таким названием делает кнопку в админке "посмотреть на сайте"
    def get_absolute_url(self):
        return reverse_lazy('category', kwargs={'category_id': self.pk})
