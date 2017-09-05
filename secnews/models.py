from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
@python_2_unicode_compatible
class SecnewsItem(models.Model):
    pub_date = models.DateField('published date')
    tag = models.CharField(max_length=50)
    author = models.CharField(max_length=50, default='')
    en_text = models.TextField('original English text', default='')
    cn_text = models.TextField('Chinese summary')
    img_link = models.URLField('illustration link', default='')

    def __str__(self):
        return '#{}, {}'.format(self.id, self.pub_date)
