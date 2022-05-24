import jqdata

def initialize(context):
    set_benchmark
    # g.security = get_index_stocks('000300.XSHG')
    set_option('use_real_price', True)
    set_order_cost(OrderCost(open_tax=0, close_tax=0.001, open_commission=0.0003, close_commission=0.0003, close_today_commission=0, min_commission=5), type='stock')
    
    g.security = ['601318.XSHG']
    g.p1 = 5
    g.p2 = 30
    
def handle_data(context, data):
    for stock in g.security:
        # 金叉：5日均线大于10日均线且不持仓
        # 死叉：5日均线小于10日均线且持仓
        df = attribute_history(stock, g.p2)
        ma10 = df['close'].mean()
        ma5 = df['close'][-5:].mean()
        
        if ma5 < ma10 and stock in context.portfolio.positions:
            order_target(stock, 0)
            
        if ma5 > ma10 and stock not in context.portfolio.positions:
            order_value(stock, context.portfolio.available_cash * 0.8)
            
        