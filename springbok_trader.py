from datamodel import OrderDepth, UserId, TradingState, Order
import string
import json
import numpy as np
from typing import Dict, List

import json
import numpy as np
from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order

class Trader:
    def run(self, state: TradingState) -> tuple[Dict[str, List[Order]], int, str]:
        """Main trading logic executed each iteration."""
        # Load or initialize traderData
        if state.traderData:
            data = json.loads(state.traderData)
        else:
            data = {
                'RAINFOREST_RESIN': {'prices': []},
                'KELP': {'prices': []},
                'SQUID_INK': {'prices': []}
            }

        result = {}
        for product in state.order_depths:
            order_depth = state.order_depths[product]
            mid_price = self.get_mid_price(order_depth)
            data[product]['prices'].append(mid_price)
            
            # Limit price history to relevant window sizes
            if product == 'RAINFOREST_RESIN' and len(data[product]['prices']) > 100:
                data[product]['prices'] = data[product]['prices'][-100:]
            elif product == 'KELP' and len(data[product]['prices']) > 20:
                data[product]['prices'] = data[product]['prices'][-20:]
            elif product == 'SQUID_INK' and len(data[product]['prices']) > 10:
                data[product]['prices'] = data[product]['prices'][-10:]

            # Apply strategy per product
            if product == 'RAINFOREST_RESIN':
                result[product] = self.trade_rainforest_resin(state, data)
            elif product == 'KELP':
                result[product] = self.trade_kelp(state, data)
            elif product == 'SQUID_INK':
                result[product] = self.trade_squid_ink(state, data)
            else:
                result[product] = []

        traderData = json.dumps(data)
        conversions = 0  # No conversions in Round 1
        return result, conversions, traderData

    def get_mid_price(self, order_depth: OrderDepth) -> float:
        """Calculate mid-price from best bid and ask."""
        best_bid = max(order_depth.buy_orders.keys())
        best_ask = min(order_depth.sell_orders.keys())
        return (best_bid + best_ask) / 2

    def trade_rainforest_resin(self, state: TradingState, data: Dict) -> List[Order]:
        """Market-making strategy for Rainforest Resin."""
        product = 'RAINFOREST_RESIN'
        if len(data[product]['prices']) < 100:
            return []
        
        ma = np.mean(data[product]['prices'])
        buy_price = int(round(ma - 2))
        sell_price = int(round(ma + 2))
        current_position = state.position.get(product, 0)
        max_buy = 50 - current_position
        max_sell = 50 + current_position

        orders = []
        if max_buy > 0:
            orders.append(Order(product, buy_price, min(10, max_buy)))
        if max_sell > 0:
            orders.append(Order(product, sell_price, -min(10, max_sell)))
        return orders

    def trade_kelp(self, state: TradingState, data: Dict) -> List[Order]:
        """Trend-following strategy for Kelp."""
        product = 'KELP'
        if len(data[product]['prices']) < 20:
            return []
        
        prices = data[product]['prices']
        short_ma = np.mean(prices[-5:])
        long_ma = np.mean(prices)
        current_position = state.position.get(product, 0)
        order_depth = state.order_depths[product]
        best_bid = max(order_depth.buy_orders.keys())
        best_ask = min(order_depth.sell_orders.keys())

        orders = []
        if short_ma < long_ma and current_position > -50:
            sell_qty = min(10, 50 + current_position)
            if sell_qty > 0:
                orders.append(Order(product, best_bid, -sell_qty))
        elif short_ma > long_ma and current_position < 50:
            buy_qty = min(10, 50 - current_position)
            if buy_qty > 0:
                orders.append(Order(product, best_ask, buy_qty))
        return orders

    def trade_squid_ink(self, state: TradingState, data: Dict) -> List[Order]:
        """Mean-reversion strategy for Squid Ink."""
        product = 'SQUID_INK'
        if len(data[product]['prices']) < 10:
            return []
        
        prices = data[product]['prices']
        ma = np.mean(prices)
        std = np.std(prices) if np.std(prices) > 0 else 1e-6  # Avoid division by zero
        z_score = (prices[-1] - ma) / std
        current_position = state.position.get(product, 0)
        order_depth = state.order_depths[product]
        best_bid = max(order_depth.buy_orders.keys())
        best_ask = min(order_depth.sell_orders.keys())

        orders = []
        if z_score < -1 and current_position < 50:
            buy_qty = min(5, 50 - current_position)
            if buy_qty > 0:
                orders.append(Order(product, best_ask, buy_qty))
        elif z_score > 1 and current_position > -50:
            sell_qty = min(5, 50 + current_position)
            if sell_qty > 0:
                orders.append(Order(product, best_bid, -sell_qty))
        return orders