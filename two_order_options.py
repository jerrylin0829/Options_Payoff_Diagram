import numpy as np
import matplotlib.pyplot as plt
from plain_vanilla_options import PlainVanillaOptions
from call_spread import CallSpread
from debit_spread import DebitSpread

class TwoOptions():
    def __init__(self, option1, option2):
        self.call_spread = CallSpread(option1, option2)
        self.debit_spread = DebitSpread(option1, option2)
if __name__ == '__main__':
    
    option1 = (4000, 4200, 90, 'short', 'call')
    option2 = (4000, 3800, 120,'long', 'call')
    two_options = TwoOptions(option1, option2)
    plot_call_spread = two_options.call_spread.plot()
    # plot_debit_spread = two_options.debit_spread.plot()
    # price_debit_spread = two_options.debit_spread.calculate_price()
    # print(price_put_spread)
    # print(plot_call_spread)