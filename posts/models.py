import markdown
from bs4 import BeautifulSoup
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe

from users.models import User


class Post(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', args=[self.slug])

    def body_as_markdown(self):
        return mark_safe(markdown.markdown(self.body))

    def body_preview(self):
        plain_text = ''.join(BeautifulSoup(self.body_as_markdown(), 'html.parser').findAll(text=True))[:150]
        formatted_text = "\n".join(plain_text.split("\n")[:5])[:100] + '...'
        return formatted_text

    def get_first_image_src(self):
        img_tag = BeautifulSoup(self.body_as_markdown(), 'html.parser').find('img')
        if img_tag is None:
            img_src = 'https://www.landuse-ca.org/wp-content/uploads/2019/04/no-photo-available.png'
        else:
            img_src = img_tag['src']
        return img_src
