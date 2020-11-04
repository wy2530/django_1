from typing import List

from django.core.paginator import Paginator
from django.shortcuts import render,reverse
from django.http import HttpResponse
from goods.models import *

# Create your views here.
from goods.models import GoodsInfo


"""用户登录注册页"""
def home(request):
    return render(request, 'login.html')

"""首页展示"""
def index(request):
    # 1、查询商品的分类
    categories = GoodsCategory.objects.all()
    # 2、从每个分类中 获取4个商品(每一类的最后4个商品)
    for cag in categories:
        # -id 可以反向排序
        cag.goods_list = cag.goodsinfo_set.order_by('-id')[:4]

    # 3、获取购物车里所有的商品
    '''
      cookie(因为需要保存数据了)
      key:value  商品id:数量
    '''
    # 1、定义购物车商品列表
    cart_goods_list = []
    # 2、购物车中的商品总数量
    cart_goods_count = 0
    for goods_id, goods_num in request.COOKIES.items():
        if not goods_id.isdigit():
            continue
        # 根据id来获取商品对象
        cart_goods = GoodsInfo.objects.get(id=goods_id)
        cart_goods.goods_num = goods_num  # goods_num没用在数据库里怎么回事？？？

        cart_goods_list.append(cart_goods)
        cart_goods_count = cart_goods_count + int(goods_num)
    # 4、购物车中商品的数量
    return render(request, 'index.html', {'categories': categories,
                                          'cart_goods_list': cart_goods_list,
                                          'cart_goods_count': cart_goods_count
                                          })


"""商品详情页"""
def detail(request):
    # 1、商品的数据
    categories = GoodsCategory.objects.all()
    # 2、购物车数据
    cart_goods_list = []
    cart_goods_count = 0
    for goods_id, goods_num in request.COOKIES.items():
        if not goods_id.isdigit():
            continue
        # 根据id查询商品
        cart_goods = GoodsInfo.objects.get(id=goods_id)
        cart_goods.goods_num = goods_num
        cart_goods_list.append(cart_goods)
        cart_goods_count = cart_goods_count + int(goods_num)
    # 3、当前要显示的商品的数据
    goods_id = request.GET.get('id', 1)  # 最后的1是默认的
    goods_data = GoodsInfo.objects.get(id=goods_id)
    return render(request, 'detail.html', {'categories': categories,
                                           'cart_goods_list': cart_goods_list,
                                           'cart_goods_count': cart_goods_count,
                                           'goods_data': goods_data,
                                           # 'cart_goods': cart_goods,
                                           })


"""商品分类页面"""


def goods(request):
    # 1、获取传过来的分类id
    cag_id = request.GET.get('cag', 1)
    # 1-2.得到当前page的页码
    page_id = request.GET.get('page', 1)
    # 2、获取当前分类
    current_cag = GoodsCategory.objects.get(id=cag_id)
    # 3、当前分类下的所有数据
    goods_data = GoodsInfo.objects.filter(goods_cag_id=cag_id)
    # 1-1.分页,实例化分页对象
    paginator = Paginator(goods_data, 18)
    # 1-3.显示该页码
    page_data = paginator.page(page_id)
    # 4、所有分类
    categories = GoodsCategory.objects.all()
    # 5、购物车所有商品
    cart_goods_list = []
    cart_goods_count = 0
    for goods_id, goods_num in request.COOKIES.items():
        if not goods_id.isdigit():
            continue
        # 根据id查询商品
        cart_goods = GoodsInfo.objects.get(id=goods_id)
        cart_goods.goods_num = goods_num
        cart_goods_list.append(cart_goods)
        cart_goods_count = cart_goods_count + int(goods_num)
    return render(request, 'goods.html', {'current_cag': current_cag,
                                          # 1-2：改一下传过去的数据
                                          'page_data': page_data,
                                          'cart_goods_list': cart_goods_list,
                                          'cart_goods_count': cart_goods_count,
                                          'categories': categories,
                                          # 1-4: 分页器中包含了关于分页的所有信息
                                          'paginator': paginator,
                                          'cag_id': cag_id,
                                          })
