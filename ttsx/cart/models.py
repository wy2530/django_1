from django.db import models


# Create your models here.
# 订单基本信息
class OrderInfo(models.Model):
    """
    订单信息模型
    知识点：choices参数，可列举完全
    """
    status = (
        (1, '待付款'),
        (2, '待发货'),
        (3, '待收货'),
        (4, '已完成'),
    )
    # 订单编号
    order_id = models.CharField(max_length=100)
    # 收获地址
    order_addr = models.CharField(max_length=100)
    # 收货人
    order_recv = models.CharField(max_length=20)
    # 联系电话
    order_tele = models.CharField(max_length=11)
    # 运费
    order_fee = models.IntegerField(default=10)
    # 订单备注
    order_extra = models.CharField(max_length=200)
    # 订单状态
    order_status = models.IntegerField(default=1, choices=status)


# 商品信息
class OrderGoods(models.Model):
    # 所属商品
    goods_info = models.ForeignKey(to='goods.GoodsInfo', on_delete=models.CASCADE)
    # 商品数量
    goods_num = models.IntegerField()
    # 商品所属订单
    goods_order = models.ForeignKey(to='OrderInfo', on_delete=models.CASCADE)
