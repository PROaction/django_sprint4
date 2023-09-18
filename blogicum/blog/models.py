from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone

from blogicum.settings import MAX_LENGTH

User = get_user_model()


class BaseModel(models.Model):
    """Базовая модель с флагом публикуемости и временем создания."""

    is_published = models.BooleanField(default=True,
                                       verbose_name='Опубликовано',
                                       help_text='Снимите галочку, '
                                                 'чтобы скрыть публикацию.')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено',
                                      )

    class Meta:
        abstract = True


class Location(BaseModel):
    """Модель для описания местоположения автора поста."""

    name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Category(BaseModel):
    """Модель категорий постов."""

    title = models.CharField(max_length=MAX_LENGTH, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(unique=True,
                            verbose_name='Идентификатор',
                            help_text='Идентификатор страницы для URL; '
                                      'разрешены символы латиницы, цифры, '
                                      'дефис и подчёркивание.')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Post(BaseModel):
    """Модель постов."""

    title = models.CharField(max_length=MAX_LENGTH, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем — '
                  'можно делать отложенные публикации.')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор публикации')
    location = models.ForeignKey(Location,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 verbose_name='Местоположение')
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 verbose_name='Категория')
    image = models.ImageField(upload_to="image/%Y/%m/%d/",
                              verbose_name="Картинка",
                              null=True)

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        default_related_name = 'posts'
        ordering = ('-pub_date',)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'id': self.pk})


class Comment(models.Model):
    text = models.TextField('Текст комментария')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='пост',
    )
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено',
                                      )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('created_at',)
