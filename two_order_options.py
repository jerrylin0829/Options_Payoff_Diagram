import numpy as np
import matplotlib.pyplot as plt
from plain_vanilla_options import PlainVanillaOptions

class CallSpread():
    def __init__(self, option1, option2):
        
        self.S1, self.K1, self.P1, self.LorS1, self.option_type1 = option1
        self.S2, self.K2, self.P2, self.LorS2, self.option_type2 = option2
        
        self.plain_vanilla_options1 = PlainVanillaOptions(self.S1, self.K1, self.P1, self.LorS1, self.option_type1)
        self.plain_vanilla_options2 = PlainVanillaOptions(self.S2, self.K2, self.P2, self.LorS2, self.option_type2)

    def calculate_price(self):
        option_price = self.plain_vanilla_options1.calculate_price() + self.plain_vanilla_options2.calculate_price()
        return option_price
    
    def plot_call_spread(self):
        underlying_range = np.linspace(0.8 * self.K1, 1.2 * self.K1, 100)

    def plot_payoff(self, LorS, option_type):
        underlying_range = np.linspace(0.8 * self.K, 1.2 * self.K, 100)
        payoffs = [self.calculate_payoff(underlying_price) for underlying_price in underlying_range]
        plt.plot(underlying_range, payoffs, label='Payoff')
        plt.axhline(y=0, color='black')
        plt.axvline(x=self.S, color='r', linestyle='--', label='Market Price')
        plt.text(self.K, -5, f'K: {self.K:.2f}', va='top', ha='center', color='green')
        plt.xlabel('Underlying Price')
        plt.ylabel('Payoff')
        plt.title(LorS + ' ' + option_type)
        plt.grid(True)

        # Calculate and plot breakeven point for call option
        if self.option_type == 'call':
            breakeven_point = self.K + self.P
            plt.scatter(breakeven_point, 0, color='blue', label='Breakeven Point')
            if LorS == 'long': 
                # Loss Area
                plt.fill_between(underlying_range, payoffs, where=(underlying_range <= breakeven_point), color='red', alpha=0.2, label='Profit Area')
                # Profit Area
                plt.fill_between(underlying_range, payoffs, where=(underlying_range > breakeven_point), color='green', alpha=0.3, label='Loss Area')
            elif LorS == 'short':
                # Loss Area
                plt.fill_between(underlying_range, payoffs, where=(underlying_range >= breakeven_point), color='red', alpha=0.3, label='Profit Area')
                # Profit Area
                plt.fill_between(underlying_range, payoffs, where=(underlying_range < breakeven_point), color='green', alpha=0.3, label='Loss Area')
            plt.text(breakeven_point, 0, f'BEP: {breakeven_point:.2f}', va='bottom', ha='right', color='blue')

        # Calculate and plot breakeven point for put option
        elif self.option_type == 'put':
            breakeven_point = self.K - self.P
            plt.scatter(breakeven_point, 0, color='blue', label='Breakeven Point')
            if LorS == 'long': 
                # Loss Area
                plt.fill_between(underlying_range, payoffs, where=(underlying_range >= breakeven_point), color='red', alpha=0.2, label='Profit Area')
                # Profit Area
                plt.fill_between(underlying_range, payoffs, where=(underlying_range < breakeven_point), color='green', alpha=0.3, label='Loss Area')
            elif LorS == 'short':
                # Loss Area
                plt.fill_between(underlying_range, payoffs, where=(underlying_range <= breakeven_point), color='red', alpha=0.3, label='Profit Area')
                # Profit Area
                plt.fill_between(underlying_range, payoffs, where=(underlying_range > breakeven_point), color='green', alpha=0.3, label='Loss Area')
            plt.text(breakeven_point, 0, f'BEP: {breakeven_point:.2f}', va='bottom', ha='right', color='blue')
        
        else:
            raise ValueError("Invalid option type. Please specify 'call' or 'put'.")
        
        plt.legend()
        plt.show()
    
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