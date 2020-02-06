from flask import Blueprint

# 创建了一个蓝图
app_cart = Blueprint("app_cart", __name__,template_folder="templates")

# 在__init__文件被执行的时候，把视图加载进来，让蓝图与应用程序知道有蓝图的存在
from .views import get_cart