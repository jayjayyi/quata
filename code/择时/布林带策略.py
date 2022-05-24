# 三条线 
# middle = 20日均线
# up线 = 20日均线 + n * std（20日的close）
# down线 = 20日均线 - n * std（20日的close） ！ n是参数可调 也可不一样

import jqdata

def initialize(context):
    set_benchmark('000300.XSHG')
    set_option('use_real_price', True)
    set_order_cost(OrderCost(open_tax=0, close_tax=0.001, open_commission=0.0003, close_commission=0.0003, close_today_commission=0, min_commission=5), type='stock')
    
    g.security = '600036.XSHG'
    g.M = 20
    g.k = 2
    
def handle_data(context, data):
    sr = attribute_history(g.security, g.M)['close']
    # print(sr)
    
    ma = sr.mean()
    up = ma + g.k * sr.std()
    down = ma - g.k * sr.std()
    p = get_current_data()[g.security].day_open
    cash = context.portfolio.available_cash
    
    if p < down and g.security not in context.portfolio.positions:
        order_value(g.security, cash)
    elif p > up and g.security in context.portfolio.positions:
        order_target(g.security, 0)