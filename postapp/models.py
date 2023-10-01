
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from jalali_date import date2jalali

class PIN_POST(models.Model):
    title = models.CharField(max_length=100, verbose_name='تیتر')
    img = models.ImageField(upload_to='images/', verbose_name='آدرس عکس', null=True)
    story = models.TextField(null=True, verbose_name='خلاصه')
    body = models.TextField(null=True, verbose_name='متن')
    published = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ')
    slug = models.SlugField(unique=True, max_length=100, null=True, blank=True)
    visited = models.IntegerField(verbose_name='بازدید ها')
    active = models.BooleanField(default=False, verbose_name='آیا این پست منتشر شود')
    objects = models.Manager()
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("pin-detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'پین'
        verbose_name_plural = 'پین ها'


class Askformovie(models.Model):
    email = models.EmailField(verbose_name='ایمیل')
    name = models.CharField(max_length=50, verbose_name='نام')
    body = models.TextField(verbose_name='دیدگاه')
    created = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(PIN_POST, on_delete=models.CASCADE, related_name="Comments", null=True, verbose_name='پین')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name='پاسخ ها')
    active = models.BooleanField(default=False)

    def get_jalali_created_date(self):
        return date2jalali(self.created)

    def get_jalali_created_time(self):
        return self.created.strftime("%H:%M")


    @property
    def children(self):
        return Askformovie.objects.filter(reply=self).order_by('created').all()

    @property
    def is_parent(self):
        if self.reply is None:
            return True

    def __str__(self):
        return f" {self.post} | {self.name} دگاهی از"

    class Meta:

        verbose_name = 'درخواست فیلم و سریال'
        verbose_name_plural = ' درخواست ها'




class Genre(models.Model):
    name = models.CharField(max_length=250, verbose_name='ژانر')
    slug = models.SlugField(unique=True, verbose_name='آدرس ژانر')


    class Meta:
        verbose_name = 'ژانر'
        verbose_name_plural = 'ژانر ها'

    def __str__(self):

        return self.name


class Country(models.Model):
    country = models.CharField(max_length=80)

    def __str__(self):
        return self.country

    class Meta:
        verbose_name = ' کشور'
        verbose_name_plural = 'کشور ها'


class Language(models.Model):
    language = models.CharField(max_length=80)

    def __str__(self):
        return self.language

    class Meta:
        verbose_name = 'زیان'
        verbose_name_plural = 'زیان ها'


class Year(models.Model):
    year = models.CharField(max_length=25)

    def __str__(self):
        return self.year

    class Meta:
        verbose_name = 'سال'
        verbose_name_plural = 'سال ها'


class State(models.Model):
    state = models.CharField(max_length=40)

    def __str__(self):
        return self.state

    class Meta:
        verbose_name = 'وضعیت'
        verbose_name_plural = 'وضعیت ها'


class Type(models.Model):
    type = models.CharField(max_length=40)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'نوع'
        verbose_name_plural = 'انواع'


class Days(models.Model):
    day = models.CharField(max_length=40)

    def __str__(self):
        return self.day

    class Meta:
        verbose_name = 'روز'
        verbose_name_plural = 'روز ها'




class Post(models.Model):

    title = models.CharField(max_length=100, verbose_name='تیتر')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده')
    name = models.CharField(max_length=100, verbose_name='نام')
    type_film = models.ForeignKey(Type, null=True, on_delete=models.PROTECT, verbose_name='نوع')
    category = models.ManyToManyField(Genre, verbose_name='ژانر')
    product = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name='محصول')
    language = models.ForeignKey(Language, on_delete=models.PROTECT, verbose_name='زبان')
    year = models.ForeignKey(Year, on_delete=models.PROTECT, verbose_name='سال تولید', null=True)
    state = models.ForeignKey(State, on_delete=models.PROTECT, verbose_name='وضعیت', null=True)
    episode = models.CharField(max_length=100, verbose_name='تعداد قسمت ها', null=True)
    time = models.CharField(max_length=100, verbose_name='زمان')
    visited = models.IntegerField(null=True, verbose_name='بازدید ها')
    director = models.CharField(null=True, max_length=80, verbose_name='کارگردان')
    actors = models.CharField(max_length=100, null=True, verbose_name='بازیگران')
    day = models.ManyToManyField(Days, verbose_name='روز های پخش')
    release = models.CharField(max_length=200, verbose_name='تاریخ پخش', null=True)
    story = models.TextField(null=True,  verbose_name='خلاصه')
    img = models.ImageField(upload_to='images/', verbose_name='آدرس عکس', null=True)
    published = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ')
    slug = models.SlugField(unique=True, max_length=100, null=True, blank=True)
    active = models.BooleanField(default=False,verbose_name='آیا این پست منتشر شود')

    def get_jalali_created_date(self):
        return date2jalali(self.published)

    def get_jalali_created_time(self):
        return self.published.strftime("%H:%M")

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Post, self).save(*args, **kwargs)


class Comment(models.Model):

    email = models.EmailField(verbose_name='ایمیل')
    name = models.CharField(max_length=50, verbose_name='نام')
    body = models.TextField(verbose_name='دیدگاه')
    created = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="Comments", null=True, verbose_name='پست')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name='پاسخ ها')
    active = models.BooleanField(default=False,verbose_name='آیا این دیدگاه منتشر شود')

    def get_jalali_created_date(self):
        return date2jalali(self.created)

    def get_jalali_created_time(self):
        return self.created.strftime("%H:%M")


    @property
    def children(self):
        return Comment.objects.filter(reply=self).order_by('created').all()

    @property
    def is_parent(self):
        if self.reply is None:
            return True

    def __str__(self):
        return f" {self.post} | {self.name} دگاهی از"

    class Meta:

        verbose_name = 'دیدگاه'
        verbose_name_plural = 'دیدگاه ها'




# class Numeposide(models.Model):
#     episode = models.CharField(max_length=80)
#
#     def __str__(self):
#         return self.episode
#
#     class Meta:
#         verbose_name = 'لینک قسمت'
#         verbose_name_plural = 'قسمت ها'


# class Subtitle(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, verbose_name='پست')
#     episode = models.CharField(max_length=80, verbose_name='اسم لینک')
#     frame = models.CharField(max_length=20, verbose_name='کیفیت')
#     url = models.URLField(max_length=2000, verbose_name='آدرس')
#
#     def __str__(self):
#         return f"{self.frame} | {self.episode} | {self.post}"
#
#     class Meta:
#         verbose_name = 'لینک زیرنویس'
#         verbose_name_plural = 'لینک های دانلود زیرنویس'
#


class Frame(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, verbose_name='پست')
    episode = models.CharField(max_length=80, verbose_name='اسم لینک')
    frame = models.CharField(max_length=20, verbose_name='کیفیت')
    url = models.URLField(max_length=2000, verbose_name='آدرس')


    def __str__(self):
        return f"{self.frame} | {self.episode} | {self.post}"

    class Meta:
        verbose_name = 'لینک های ایجاد شده'
        verbose_name_plural = 'تمام لینک های ایجاد شده'


class Download(models.Model):
    name = models.CharField(max_length=80, verbose_name='لینک')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, verbose_name='پست')
    frame = models.ManyToManyField(Frame, related_name="Frame", verbose_name='کیفیت')
    active = models.BooleanField(verbose_name='لینک فیلم و سریال')
    order = models.IntegerField()

    def __str__(self):
        return f" {self.name} | {self.post}"

    class Meta:
        verbose_name = 'لینک دانلود'
        verbose_name_plural = 'لینک های دانلود'

