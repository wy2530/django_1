from django.contrib import admin
from goods.models import GoodsInfo
# Register your models here.

class GoodsInfoAdmin(admin.ModelAdmin):
    # 自定义展示哪些字段(数据库中的名字)
    list_display = ['id', 'goods_name', 'goods_price', 'goods_desc']
    # 使数据分页显示
    list_per_page = 10
    # 操作按钮
    actions_on_top = True
    actions_on_bottom = True
    # 搜索框和搜索依赖字段
    search_fields = ['id', 'goods_name']


# 模型类+定义的类都需要注册的
admin.site.register(GoodsInfo, GoodsInfoAdmin)
