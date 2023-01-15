from hummingbot.client.config.global_config_map import global_config_map
from hummingbot.client.config.config_helpers import get_strategy_config_map, get_strategy_config_value
from hummingbot.strategy.market_making.market_making_strategy import MarketMakingStrategy
from typing import List
import time

# Define the trading pair and the order types
trading_pair = "BTCUSDT"
spot_order_types = ["limit"]
perp_order_types = ["limit", "market"]

# Define the target positions
target_positions = [-0.5, 0, 0.5]

# Define the percentage for the perpetual market
perp_percentage = 0.5

# Define the leverage amount for the perpetual market
leverage_amount = 3

# Define the time interval for Bollinger bands
time_interval = "1m"

class DynamicBollingerDirectionMarketMakingStrategy(MarketMakingStrategy):
    def __init__(self, trading_pair: str, spot_order_types: List[str], perp_order_types: List[str], target_positions: List[float], perp_percentage: float, leverage_amount: int):
        self._trading_pair = trading_pair
        self._spot_order_types = spot_order_types
        self._perp_order_types = perp_order_types
        self._target_positions = target_positions
        self._perp_percentage = perp_percentage
        self._leverage_amount = leverage_amount
        self._direction = None
        self._last_price = None
        self._last_time_interval = None
        self._last_upper_band = None
        self._last_lower_band = None
        self._current_price = None
        self._upper_band = None
        self._lower_band = None
        super().__init__()

    async def on_tick(self):
        self._current_price = await self.data_source.quote_currency_price()
        if self._direction == "buy":
            if self._current_position < self._target_positions[0]:
                await self.buy_all_levels(self._trading_pair, self._spot_order_types
                self._upper_band, self._lower_band = self.get_bollinger_bands()
                if self._last_upper_band is None or self._last_lower_band is None:
                    self._last_upper_band = self._upper_band
                    self._last_lower_band = self._lower_band
                    self._last_price = self._current_price
                elif self._current_price > self._last_price and self._current_price > self._last_upper_band:
                    await self.cancel_all_orders(self._trading_pair, "limit", "buy")
                    await self.place_limit_orders(self._trading_pair, self._lower_band, "buy")
                    self._last_upper_band = self._upper_band
                    self._last_lower_band = self._lower_band
                    self._last_price = self._current_price
        elif self._direction == "sell":
            if self._current_position > self._target_positions[-1]:
                await self.sell_all_levels(self._trading_pair, self._spot_order_types)
                await self.perp_sell_all_levels(self._trading_pair, self._perp_order_types)
                self._upper_band, self._lower_band = self.get_bollinger_bands()
                if self._last_upper_band is None or self._last_lower_band is None:
                    self._last_upper_band = self._upper_band
                    self._last_lower_band = self._lower_band
                    self._last_price = self._current_price
                elif self._current_price < self._last_price and self._current_price < self._last_lower_band:
                    await self.cancel_all_orders(self._trading_pair, "limit", "sell")
                    await self.place_limit_orders(self._trading_pair, self._upper_band, "sell")
                    self._last_upper_band = self._upper_band
                    self._last_lower_band = self._lower_band
                    self._last_price = self._current_price

    def get_bollinger_bands(self):
        """
        Returns the upper and lower Bollinger
        bands based on the current market price and the time interval
        """
try:
current_time = time.time()
time_diff = current_time - self._last_time_interval
if time_diff > 60:
prices = self.data_source.get_historical_price(time_interval)
upper_band, middle_band, lower_band = talib.BBANDS(prices, timeperiod=20)
self._last_time_interval = current_time
return upper_band[-1], lower_band[-1]
else:
return self._last_upper_band, self._last_lower_band
except Exception as e:
self.logger().error(f"Error getting Bollinger bands: {e}")
return None, None

def set_direction(self, direction: str):
    """
    Sets the direction of the strategy (buy or sell)
    """
    self._direction = direction


Instantiate the strategy and set the direction
dynamic_bollinger_strategy = DynamicBollingerDirectionMarketMakingStrategy(trading_pair, spot_order_types, perp_order_types, target_positions, perp_percentage, leverage_amount)
dynamic_bollinger_strategy.set_direction("buy")

Connect the strategy to the exchange and start the strategy
dynamic_bollinger_strategy.connect()
dynamic_bollinger_strategy.start()

Wait for the strategy to finish
dynamic_bollinger_strategy.wait()

Disconnect the strategy from the exchange
dynamic_bollinger_strategy.disconnect()