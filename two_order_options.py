import numpy as np
import matplotlib.pyplot as plt
from plain_vanilla_options import PlainVanillaOptions

class TwoOptions():
    def __init__(self, option1, option2):
        
        self.S1, self.K1, self.P1, self.LorS1, self.option_type1 = option1
        self.S2, self.K2, self.P2, self.LorS2, self.option_type2 = option2

        self.plain_vanilla_options1 = PlainVanillaOptions(self.S1, self.K1, self.P1, self.LorS1, self.option_type1)
        self.plain_vanilla_options2 = PlainVanillaOptions(self.S2, self.K2, self.P2, self.LorS2, self.option_type2)

    # long call and short call
    def call_spread(self):
        option_price = self.plain_vanilla_options1.calculate_price() + self.plain_vanilla_options2.calculate_price()
        return option_price

if __name__ == '__main__':
    
    option1 = (7000, 5100, 200, 'long', 'call')
    option2 = (7000, 5300, 90,'short', 'call')
    two_options = TwoOptions(option1, option2)

    print(two_options.call_spread()*50)