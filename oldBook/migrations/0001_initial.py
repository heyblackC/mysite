# Generated by Django 2.1.2 on 2018-11-20 05:18

from django.db import migrations, models
import django.db.models.deletion
import oldBook.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_view', models.IntegerField(default=0, verbose_name='浏览量')),
                ('author', models.CharField(max_length=50, verbose_name='作者')),
                ('title', models.CharField(max_length=50, verbose_name='标题')),
                ('publisher', models.CharField(max_length=25, verbose_name='出版社')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('expires', models.DateTimeField(verbose_name='过期时间')),
                ('description', models.TextField(blank=True, verbose_name='其他描述')),
                ('wear_degree', models.IntegerField(choices=[(0, '较好'), (1, '一般'), (2, '严重')], verbose_name='磨损程度')),
                ('contact', models.CharField(max_length=20, verbose_name='联系方式')),
                ('contact_type', models.IntegerField(choices=[(0, '手机'), (1, '微信'), (2, 'qq')], verbose_name='联系方式类型')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=oldBook.models.get_hash_filename, verbose_name='图片')),
                ('book', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='oldBook.Book')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nick', models.CharField(max_length=20, verbose_name='名称')),
                ('avatar', models.URLField(verbose_name='用户头像URL')),
            ],
        ),
    ]