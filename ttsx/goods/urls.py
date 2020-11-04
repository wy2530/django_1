from django.urls import path
from goods import views
urlpatterns = [
    # 首页
    path('index/', views.index),
    # 商品详情页
    path('detail/', views.detail),
    # 商品分类页面
    path('goods/', views.goods),
]