from flask import Blueprint

# 创建一个蓝图的对象，蓝图就是一个小模块的抽象概念
app_orders = Blueprint("app_orders", __name__)

@app_orders.route("/get_orders")
def get_orders():
    return "get orders page"