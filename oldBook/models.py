from django.db import models
import hashlib
import json
from .hasher import make_password, verify
WEB_URL = "http://oldBook.heyblack.top/"


class User(models.Model):
    # openID = models.CharField("用户ID", max_length=100)
    username = models.CharField("用户名", max_length=25, unique=True)
    avatar = models.URLField("用户头像URL", blank=True)
    password = models.CharField("名称", max_length=128)

    @classmethod
    def create_user(cls, username, password, avatar=''):
        if not username or not password:
            raise ValueError('The given username and password must be set')

        user = cls(username=username,
                   password=make_password(password),
                   avatar=avatar)
        user.save()
        return user

    def verify(self, raw_password):
        return verify(raw_password, self.password)

    def obj_dic(self):
        return {
            "id": self.id,
            "username": self.username,
            "avatar": self.avatar
        }


class Book(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
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

    def dic_data(self):
        image_set = []
        for i in range(0, self.image_set.count()):
            image_model = self.image_set.all()[i]
            image_set.append(WEB_URL + image_model.image.url)

        json_dic = {
            "id": self.id,
            "page_view": self.page_view,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "title": self.title,
            "author": self.author,
            "publisher": self.publisher,
            "description": self.description,
            "expires": self.expires.strftime("%Y-%m-%d %H:%M:%S"),
            "wear_degree": self.wear_degree,
            "contact": self.contact,
            "contact_type": self.contact_type,
            "image_set": image_set,
            "username": self.user.username,
            "avatar": self.user.avatar

        }
        return json_dic

    def json_data(self):
        return json.dumps(self.dic_data())


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

