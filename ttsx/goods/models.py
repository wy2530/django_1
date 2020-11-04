from django.db import models


# Create your models here.

# 1、商品分类表
class GoodsCategory(models.Model):
    # 分类的名称
    cag_name = models.CharField(max_length=32)
    # 分类的样式
    cag_css = models.CharField(max_length=20)
    # 分类的图片 (当前图片存到了cag文件夹下)
    cag_img = models.ImageField(upload_to='cag')


# 2、商品信息表
class GoodsInfo(models.Model):
    # 商品名字(verbose_name只会显示在 admin 页面)
    goods_name = models.CharField(max_length=2000, verbose_name='商品名字')
    # 商品价格
    goods_price = models.IntegerField(default=0, verbose_name='商品价格')
    # 商品图片
    goods_img = models.ImageField(upload_to='goods')
    # 商品描述
    goods_desc = models.CharField(max_length=2000, verbose_name='商品描述')
    # 商品分类(此时是外键了)
    '''
    分析一下该外键，商品分类与商品信息是1：多，因此外键建在多的一方
    外键对应的是商品分类表
    '''
    goods_cag = models.ForeignKey(to='GoodsCategory', on_delete=models.CASCADE)

    def __str__(self):
        return self.goods_name
