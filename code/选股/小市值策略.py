# 针对多个因子
# 注意将不同数量级因子归一化再合成评价模型
# 常用归一化
# 1. min——max归一化 x‘ = （x - min）/ （max - min） 0～1
# 缺点：新的数据加入的时候，可能会有问题

# 2. z-score归一化 x‘ = （x - u）/ 标准差 均值为0，标准差为1
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
    g.q = query(valuation, indicator).filter(valuation.code.in_(g.security)) 
    g.N = 20
    
    run_monthly(handle, 1) # run f per month

def handle(context):

    df = get_fundamentals(g.q)[['code', 'market_cap', 'roe']]
    df['market_cap'] = (df['market_cap'] - df['market_cap'].min()) / (df['market_cap'].max() - df['market_cap'].min())
    df['roe'] = (df['roe'] - df['roe'].min()) / (df['roe'].max() - df['roe'].min())
    df['score'] = df['roe'] - df['market_cap']

    df = df.sort_values('score').iloc[-g.N:,: ]
    
    # 需要买的code
    to_hold = df['code'].values
    
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