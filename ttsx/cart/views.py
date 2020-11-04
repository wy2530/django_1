import datetime

from django.shortcuts import render, redirect
from goods.models import *
from cart.models import *


# Create your views here.

# 添加到购物车 cookie  goods_id:count"""
def add_cart(request):
    # 1、获取传过来的商品id
    goods_id = request.GET.get('id', '')
    # 2、把商品添加到cookie里
    """
            把商品id存到cookies里：
            1、如果购物车里没用该商品，就直接添加1
            2、如果购物车原本就有该商品，只需要数量加1
     """
    if goods_id:
        # 获取详情页地址(也就是上一页的数据)
        prev_url = request.META['HTTP_REFERER']
        # 需要返回整个页面，但是有部分数据修改的时候用重定向
        response = redirect(prev_url)
        goods_count = request.COOKIES.get(goods_id)
        if goods_count:
            goods_count = int(goods_count) + 1
        else:
            goods_count = 1
        # 把商品id和数量保存到cookie
        response.set_cookie(goods_id, goods_count)

    return response


# 展示购物车内容 """
def show_cart(request):
    # 1、获取购物车商品列表
    cart_goods_list = []
    # 2、获取购物车商品总数量
    cart_goods_count = 0
    # 3、购物车总价格
    cart_goods_money = 0

    """
    从cookie中获取数据，遍历cookie
    """
    for goods_id, goods_num in request.COOKIES.items():
        if not goods_id.isdigit():
            continue
        # 根据id查询商品
        cart_goods = GoodsInfo.objects.get(id=goods_id)
        cart_goods.goods_num = goods_num
        # 当前商品的价格小计
        cart_goods.total_money = int(goods_num) * cart_goods.goods_price

        cart_goods_list.append(cart_goods)
        cart_goods_count += int(goods_num)

        # 购物车商品总价
        cart_goods_money += int(goods_num) * cart_goods.goods_price

    return render(request, 'cart.html', {'cart_goods_list': cart_goods_list,
                                         'cart_goods_count': cart_goods_count,
                                         'cart_goods_money': cart_goods_money,
                                         })


# 减少购物车中的该商品"""
def reduce_cart(request):
    goods_id = request.GET.get('id', '')
    if goods_id:
        # 获取详情页地址(也就是上一页的数据)
        prev_url = request.META['HTTP_REFERER']
        # 需要返回整个页面，但是有部分数据修改的时候用重定向
        response = redirect(prev_url)
        goods_count = request.COOKIES.get(goods_id)
        if int(goods_count) == 0:
            response.delete_cookie(goods_id)
        elif goods_count:
            goods_count = int(goods_count) - 1
            response.set_cookie(goods_id, goods_count)
        # 把商品id和数量保存到cookie
    return response


# 删除购物车中的该商品
def remove_cart(request):
    # 获取要删除商品的ip
    goods_id = request.GET.get('id', '')
    # 如果得到了id
    if goods_id:
        # 获取上一个页面的url地址
        prev_url = request.META['HTTP_REFERER']
        # 获取要返回的response对象
        response = redirect(prev_url)
        # 判断商品是否存在在购物车
        # 先获取当前商品的数量
        goods_count = request.COOKIES.get(goods_id, '')
        # 如果存在，那么一定有数量
        if goods_count:
            response.delete_cookie(goods_id)
    return response


# 提交订单页面
def place_order(request):
    # 1、获取购物车商品列表
    cart_goods_list = []
    # 2、获取购物车商品总数量
    cart_goods_count = 0
    # 3、购物车总价格
    cart_goods_money = 0

    """
    从cookie中获取数据，遍历cookie
    """
    for goods_id, goods_num in request.COOKIES.items():
        if not goods_id.isdigit():
            continue
        # 根据id查询商品
        cart_goods = GoodsInfo.objects.get(id=goods_id)
        cart_goods.goods_num = goods_num
        # 当前商品的价格小计
        cart_goods.total_money = int(goods_num) * cart_goods.goods_price

        cart_goods_list.append(cart_goods)
        cart_goods_count += int(goods_num)

        # 购物车商品总价
        cart_goods_money += int(goods_num) * cart_goods.goods_price

    return render(request, 'place_order.html', {'cart_goods_list': cart_goods_list,
                                                'cart_goods_count': cart_goods_count,
                                                'cart_goods_money': cart_goods_money,
                                                })


# 提交订单的功能
def submit_order(request):
    # 会提交到订单信息数据库中
    addr = request.POST.get('addr', '河北省唐山市')
    recv = request.POST.get('recv', 'Jocelyn')
    tele = request.POST.get('tele', '13899902312')
    extra = request.POST.get('extra', '无')
    print(addr,recv,tele,extra)
    # 实例化订单对象
    order_info = OrderInfo()
    # 给订单赋值
    order_info.order_addr = addr
    order_info.order_recv = recv
    order_info.order_tele = tele
    order_info.order_extra = extra
    # 订单编号的生成(简化为日期)
    order_info.order_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    # 保存
    order_info.save()

    # 提交成功的页面  (重定向不加/是拼接吗？？？)
    response = redirect('/cart/submit_success/?id=%s' % order_info.order_id)

    # 遍历购物车的数据，生成orderGoods对象
    for goods_id, goods_num in request.COOKIES.items():
        if not goods_id.isdigit():
            continue
        # 获取商品对象
        cart_goods = GoodsInfo.objects.get(id=goods_id)
        order_goods = OrderGoods()
        # 商品信息
        # order_goods.goods_info_id = goods_id
        order_goods.goods_info = cart_goods
        order_goods.goods_num = goods_num
        order_goods.goods_order = order_info
        order_goods.save()

        # 把数据从数据库中删除
        response.delete_cookie(goods_id)
    return response


# 提交成功的
def submit_success(request):
    # 获取传过来的订单号
    order_id = request.GET.get('id')
    # 获取订单对象
    order_info = OrderInfo.objects.get(order_id=order_id)
    order_goods_list = OrderGoods.objects.filter(goods_order=order_info)

    total_money = 0
    total_num = 0
    for goods in order_goods_list:
        goods.total_money = goods.goods_info.goods_price * goods.goods_num
        total_money += goods.total_money
        total_num += goods.goods_num
    return render(request, 'success.html', {'order_info': order_info,
                                            'order_goods_list': order_goods_list,
                                            'total_money': total_money,
                                            'total_num': total_num,
                                            })
