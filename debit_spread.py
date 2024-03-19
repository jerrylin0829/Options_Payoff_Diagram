import numpy as np
import matplotlib.pyplot as plt
from plain_vanilla_options import PlainVanillaOptions

class DebitSpread():
    def __init__(self, option1, option2):
        
        self.S1, self.K1, self.P1, self.LorS1, self.option_type1 = option1
        self.S2, self.K2, self.P2, self.LorS2, self.option_type2 = option2
        
        self.plain_vanilla_options1 = PlainVanillaOptions(self.S1, self.K1, self.P1, self.LorS1, self.option_type1)
        self.plain_vanilla_options2 = PlainVanillaOptions(self.S2, self.K2, self.P2, self.LorS2, self.option_type2)

    def calculate_price(self):
        option_price = self.plain_vanilla_options1.calculate_price() + self.plain_vanilla_options2.calculate_price()
        return option_price
    
    def plot(self):
        # Plot line of Payoff
        underlying_range = np.linspace(0.6 * min(self.K1, self.K2), 1.3 * max(self.K1, self.K2), 500)
        payoffs1 = [self.plain_vanilla_options1.calculate_payoff(underlying_price) for underlying_price in underlying_range]
        payoffs2 = [self.plain_vanilla_options2.calculate_payoff(underlying_price) for underlying_price in underlying_range]
        payoffs = [payoff1 + payoff2 for payoff1, payoff2 in zip(payoffs1, payoffs2)]

        # Convert payoffs to numpy array
        payoffs = np.array(payoffs)

        plt.plot(underlying_range, payoffs, label='Payoff', color = "r")
        plt.axhline(y=0, color='black')
        plt.axvline(x=self.S1, color='gray', linestyle='--', label='Market Price')
        plt.plot(self.K1, 0, 'go', label=f'K1: {self.K1:.2f}', alpha=0.3)
        plt.plot(self.K2, 0, 'go', label=f'K2: {self.K2:.2f}', alpha=0.3)
        plt.xlabel('Underlying Price')
        plt.ylabel('Payoff')
        plt.title('Put Spread')
        plt.grid(True)

        # Calculate and plot breakeven points
        breakeven_points = []
        for i in range(len(payoffs)-1):
            if payoffs[i] * payoffs[i+1] < 0:  # If the signs are different, it means there is a crossing between these two elements
                x1, x2 = underlying_range[i], underlying_range[i+1]
                y1, y2 = payoffs[i], payoffs[i+1]
                # Use linear interpolation to calculate the underlying_price at the crossing
                breakeven_point = x1 - y1 * (x2 - x1) / (y2 - y1)
                breakeven_points.append(breakeven_point)
                
        for breakeven_point in breakeven_points:
            plt.plot([breakeven_point], [0], 'bo', label=f'BEP: {breakeven_point:.2f}', alpha=0.3)
        
        # Loss Area
        plt.fill_between(underlying_range, payoffs, where=(payoffs <= 0), color='green', alpha=0.2, label='Profit Area')
        
        # Profit Area
        plt.fill_between(underlying_range, payoffs, where=(payoffs > 0), color='red', alpha=0.2, label='Loss Area')
        plt.legend()
        plt.show()     
    