

class VolatilitySqueezeStrategy(FlexibleDirectionMarketMakingStrategy):
    def __init__(self, trading_pair, spot_order_types, perp_order_types, target_positions, perp_percentage, leverage_amount, event_logger):
        super().__init__(trading_pair, spot_order_types, perp_order_types,
                         target_positions, perp_percentage, leverage_amount, event_logger)
        self._upper_band = None
        self._lower_band = None
        self._last_upper_band = None
        self._last_lower_band = None
        self._last_time_interval = None
        self._threshold = 0.05

    async def on_tick(self):
        self._upper_band, self._lower_band = self.get_bollinger_bands()
        if self._upper_band is not None and self._lower_band is not None:
            if self._direction == "buy":
                if self._current_price > self._last_upper_band + (self._last_upper_band * self._threshold):
                    await self.cancel_all_orders(self._trading_pair, "limit", "buy")
                    await self.place_limit_orders(self._trading_pair, self._last_upper_band, "buy")
                    self._last_upper_band = self._upper_band
                    self._last_lower_band = self._lower_band
            elif self._direction == "sell":
                if self._current_price < self._last_lower_band - (self._last_lower_band * self._threshold):
                    await self.cancel_all_orders(self._trading_pair, "limit", "sell")
             await self.place_limit_orders(self._trading_pair,
                                                                                              self._last_lower_band, "sell")
            self._last_upper_band=self._upper_band
            self._last_lower_band=self._lower_band

            class VolatilityBreakoutStrategy(FlexibleDirectionMarketMakingStrategy):
                def init(self, trading_pair, spot_order_types, perp_order_types, target_positions, perp_percentage, leverage_amount, event_logger):
                 super().init(trading_pair, spot_order_types, perp_order_types,
                 target_positions, perp_percentage, leverage_amount, event_logger)
                 self._upper_band=None
                 self._lower_band=None
                  self._last_upper_band=None
                  self._last_lower_band=None
                  self._last_time_interval=None
                  self._threshold=0.05

                                                
                                                  async def on_tick(self):
                                                  self._upper_band, self._lower_band=self.get_bollinger_bands()
                                                  if self._upper_band is not None and self._lower_band is not None:
                                                  if self._direction == "buy":
                                                  if self._current_price < self._last_lower_band - (self._last_lower_band * self._threshold):
                                                  await self.cancel_all_orders(self._trading_pair, "limit", "buy")
                                                  await self.place_limit_orders(self._trading_pair, self._last_lower_band - (self._last_lower_band * self._threshold), "buy")
                                                  self._last_upper_band=self._upper_band
                                                  self._last_lower_band=self._lower_band
                                                  elif self._direction == "sell":
                                                  if self._current_price > self._last_upper_band + (self._last_upper_band * self._threshold):
                                                  await self.cancel_all_orders(self._trading_pair, "limit", "sell")
                                                  
                                                  await self.place_limit_orders
                                                  (self._trading_pair, self._last_upper_band +
                                                      (self._last_upper_band * self._threshold), "sell")
                                                  self._last_upper_band=self._upper_band
                                                  self._last_lower_band=self._lower_band

                                                  class CombinedStrategy(FlexibleDirectionMarketMakingStrategy):
                                                  def init(self, trading_pair, spot_order_types, perp_order_types, target_positions, perp_percentage, leverage_amount, event_logger):
                                                  super().init(trading_pair, spot_order_types, perp_order_types,
                                                               target_positions, perp_percentage, leverage_amount, event_logger)
                                                  self.squeeze_strategy=VolatilitySqueezeStrategy(
                                                      trading_pair, spot_order_types, perp_order_types, target_positions, perp_percentage, leverage_amount, event_logger)
                                                  self.breakout_strategy=VolatilityBreakoutStrategy(
                                                      trading_pair, spot_order_types, perp_order_types, target_positions, perp_percentage, leverage_amount, event_logger)

                                                 
                                                  async def on_tick(self):
                                                  self.squeeze_strategy.on_tick()
                                                  self.breakout_strategy.on_tick()
                                                  combined_strategy=CombinedStrategy(
                                                      trading_pair, spot_order_types, perp_order_types, target_positions, perp_percentage, leverage_amount, event_logger)
                                                  combined_strategy.connect()
                                                  combined_strategy.start()

                                                  Wait for the strategy to finish
                                                  combined_strategy.wait()

                                                  Disconnect the strategy from the exchange
                                                  combined_strategy.disconnect()
