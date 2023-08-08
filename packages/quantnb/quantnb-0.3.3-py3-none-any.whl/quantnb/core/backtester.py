from quantnb.core.data_module import DataModule
from quantnb.core.enums import OrderDirection, Trade, OrderType
from quantnb.core.data_module import DataModule
from quantnb.core.trade_module import TradeModule
from quantnb.core import print_bar
from quantnb.core.enums import DataType, Trade
from quantnb.core.specs_nb import backtester_specs
from numba.experimental import jitclass
import numpy as np

TRADE_ITEMS_COUNT = Trade.__len__()


# from quantnb.core.trade_module import DataModule


# pyright: reportGeneralTypeIssues=false
@jitclass(backtester_specs)
class Backtester_nb:
    data_module: DataModule.class_type.instance_type
    trade_module: TradeModule.class_type.instance_type

    def __init__(
        self,
        data_module: DataModule,
        trade_module: TradeModule,
    ) -> None:
        self.prev_percentage: int = 0
        self.data_module: DataModule = data_module
        self.trade_module: TradeModule = trade_module

    def was_trade_filled(self, i, date, last_trade, last_trade_index=None, debug=False):
        tick = date[i]
        next_tick = date[i + 1]

        if tick < last_trade <= next_tick:
            return True

        elif last_trade < tick:
            if debug:
                print("Skippped tick", last_trade_index, last_trade, tick, next_tick, i)
            return True
        else:
            return False

    def loop_updates(self, index):
        # UPDATE PNL OF TRADES
        self.trade_module.update_trades_pnl(self.data_module.close[index], 0, 0)

        # CLOSE TRADES
        data = self.data_module
        self.trade_module.check_trades_to_close(
            data.date[index], data.close[index], data.bid[index], data.ask[index]
        )

        # UPDATE EQUITY
        self.data_module.update_equity(
            index, self.trade_module.closed_pnl, self.trade_module.floating_pnl
        )

    def from_trades(self, trades):
        last_trade_index = 0
        close = self.data_module.close
        print("==========")

        for i in range(len(close)):
            self.prev_percentage = print_bar(i, len(close), self.prev_percentage)

            # ### ==============================================================================  ####

            curr_trade = trades[last_trade_index]
            direction = (
                OrderDirection.LONG.value
                if curr_trade[3] == 1
                else OrderDirection.SHORT.value
            )
            exit_time = curr_trade[1] if curr_trade[1] != -1 else np.inf
            volume = curr_trade[2]

            if self.was_trade_filled(
                i, self.data_module.date, curr_trade[0], debug=False
            ):
                entry_price = self.data_module.calculate_entry_price(i, direction)

                self.trade_module.add_trade(
                    i,
                    direction,
                    OrderType.MARKET.value,
                    self.data_module.date[i],
                    entry_price,
                    volume,
                    0,
                    0,
                    exit_time,
                    curr_trade[4],  # extra
                )
                last_trade_index += 1

            # Update PNL | Check trades to close | Update Equity
            self.loop_updates(i)

        self.trade_module.reconcile()
        return 0


class Backtester:
    def __init__(
        self,
        close,
        bid,
        ask,
        date,
        data_type=DataType.BID_ASK,
        multiplier=1,
        commission=0,
        slippage=0,
        initial_capital=10000,
        max_active_trades=100,
    ):
        self.trade_module = TradeModule(
            data_type=data_type,
            multiplier=multiplier,
            commission=commission,
            slippage=slippage,
            max_active_trades=max_active_trades,
        )
        self.data_module = DataModule(
            slippage=slippage,
            initial_capital=initial_capital,
            close=close,
            bid=bid,
            data_type=DataType.BID_ASK,
            ask=ask,
            date=date,
        )

        print("Compiling")
        print("Preparing")
        self.bt = Backtester_nb(
            self.data_module,
            self.trade_module,
        )

    def from_trades(self, trades):
        return self.bt.from_trades(trades)
