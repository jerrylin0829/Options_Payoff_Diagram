import numpy as np
import matplotlib.pyplot as plt

class PlainVanillaOptions:
    def __init__(self, S, K, P, LorS, option_type):
        self.S = S  # 現價
        self.K = K  # 履約價
        self.P = P  # 權利金
        self.LorS = LorS  # 買or賣 ('Long' 或 'Short')
        self.option_type = option_type  # 選擇權類型 ('call' 或 'put')

    def calculate_price(self):
        if self.option_type == 'call':
            if self.LorS == 'long':
                option_price = max(0, self.S - self.K) - self.P
            elif self.LorS == 'short':
                option_price = min(0, self.K - self.S) + self.P
            else:
                raise ValueError("Invalid option direction. Please specify 'long' or 'short'.")
            
        elif self.option_type == 'put':
            if self.LorS == 'long':
                option_price = max(0, self.K - self.S) - self.P
            elif self.LorS == 'short':
                option_price = min(0, self.S - self.K) + self.P
            else:
                raise ValueError("Invalid option direction. Please specify 'long' or 'short'.")
        else:
            raise ValueError("Invalid option type. Please specify 'call' or 'put'.")
        
        return option_price
    
    def calculate_payoff(self, underlying_price):
        if self.option_type == 'call':
            if self.LorS == 'long':
                payoff = max(0, underlying_price - self.K) - self.P
            elif self.LorS == 'short':
                payoff = min(0, self.K - underlying_price) + self.P
            
        elif self.option_type == 'put':
            if self.LorS == 'long':
                payoff = max(0, self.K - underlying_price) - self.P
            elif self.LorS == 'short':
                payoff = min(0, underlying_price - self.K) + self.P

        return payoff

    def plot_payoff(self, LorS, option_type):
        underlying_range = np.linspace(0.5 * self.S, 1.1 * self.S, 100)
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

if __name__ == '__main__':

    # Example usage:
    S = 7000   # 現價
    K = 5300    # 履約價
    P = 90      # 權利金

    # For American options
    lot = 1     # 口數
    share = 100 # 一口股數
    LorS = input("long or short: ")  # 買or賣 ('Long' 或 'Short')
    option_type = input("call or put: ")  # 選擇權類型 ('call' 或 'put')

    option = PlainVanillaOptions(S, K, P, LorS, option_type)
    option_price = option.calculate_price()
    print("Taiwan Option Price:", option_price*50)
    print("American Option Price:", option_price*lot*share)
    option.plot_payoff(LorS, option_type)
