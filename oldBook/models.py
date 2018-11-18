from django.db import models
import hashlib


class Book(models.Model):
    page_view = models.IntegerField("浏览量", default=0)
    author = models.CharField("作者", max_length=50)
    title = models.CharField("标题", max_length=50)
    publisher = models.CharField("出版社", max_length=25)
    created_at = models.DateTimeField("发布时间", auto_now_add=True)
    expires = models.DateTimeField("过期时间")
    description = models.TextField("其他描述", blank=True)
    WEAR_DEGREE_CHOICES = (
        (0, '较好'),
        (1, '一般'),
        (2, '严重'),
    )
    wear_degree = models.IntegerField("磨损程度", choices=WEAR_DEGREE_CHOICES)

    contact = models.CharField("联系方式", max_length=20)
    CONTACT_CHOICES = (
        (0, '手机'),
        (1, '微信'),
        (2, 'qq'),
        )
    contact_type = models.IntegerField("联系方式类型", choices=CONTACT_CHOICES)

    class Meta:
        ordering = ['-created_at']


def get_hash_filename(instance, filename):
    """

    :param instance: an instance of the model which file is sticked to
    :param filename: the original filename of the file
    :return: file path to "images/wechat_id/md5_32.file_type"
    """
    md5 = hashlib.md5()
    md5.update(filename.encode())
    hash_str = md5.hexdigest()
    return "images/%s/%s" % (str(instance.book.id), hash_str+"."
                             + (filename.split('.')[1]))


class Image(models.Model):
    book = models.ForeignKey(Book, default=None, on_delete=models.CASCADE)
    image = models.ImageField("图片", upload_to=get_hash_filename)


class User(models.Model):
    # openID = models.CharField("用户ID", max_length=100)
    nick = models.CharField("名称", max_length=20)
    avatar = models.URLField("用户头像URL")
