# 选股策略 偏离度最高的m支股票
# 价格围绕均线，跌下去的一定会涨起来
# 偏离程度： （ma - p）/ ma

## 初始化函数，设定要操作的股票、基准等等
def initialize(context):
    # 设定沪深300作为基准
    set_benchmark('000300.XSHG')
    # True为开启动态复权模式，使用真实价格交易
    set_option('use_real_price', True) 
    # 股票类交易手续费是：买入时佣金万分之三，卖出时佣金万分之三加千分之一印花税, 每笔交易佣金最低扣5块钱
    set_order_cost(OrderCost(open_tax=0, close_tax=0.001, \
                             open_commission=0.0003, close_commission=0.0003,\
                             close_today_commission=0, min_commission=5), type='stock')

    g.security = get_index_stocks('000300.XSHG')
    
    # 获得市值
    g.ma_days = 30
    g.stock_num = 10    
    
    run_monthly(handle, 1) # run f per month

def handle(context):
    
    sr = pd.Series(index = g.security)
    for stock in sr.index:
        ma = attribute_history(stock, g.ma_days)['close'].mean()
        p = get_current_data()[stock].day_open
        ratio = (ma - p)/ma
        
        sr[stock] = ratio
    
    to_hold = sr.nlargest(g.stock_num).index.values

    # 不在要买里面，先卖出
    for stock in context.portfolio.positions:
        if stock not in to_hold:
            order_target(stock, 0)
            
    # 本月要买的
    to_buy = [stock for stock in to_hold if stock not in context.portfolio.positions]
    
    # 买
    if to_buy:
        cash_per_stock = context.portfolio.available_cash / len(to_buy)
        for stock in to_buy:
            order_value(stock, cash_per_stock)