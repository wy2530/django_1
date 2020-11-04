from django.urls import path
from cart import views
urlpatterns =[
    # 首页
    # path('index/', index)
    # 添加到购物车
    path('add_cart/', views.add_cart),
    # 展示购物车页面
    path('show_cart/', views.show_cart),
    # 删除商品
    path('remove_cart/', views.remove_cart),
    # 减少商品
    path('reduce_cart/', views.reduce_cart),
    # 提交订单
    path('place_order/', views.place_order),
    # 订单提交功能
    path('submit_order/', views.submit_order),
    # 提交订单成功的页面
    path('submit_success/', views.submit_success)
]