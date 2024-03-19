import numpy as np
import matplotlib.pyplot as plt
from plain_vanilla_options import PlainVanillaOptions

class OrderOptions():
    def __init__(self, *args, **kwargs):
        self.options = []
        for option_data in args:
            self.options.append(PlainVanillaOptions(*option_data))

    def calculate_prices(self):
        prices = []
        for option in self.options:
            prices.append(option.calculate_price())
        return prices
    
    def total_prices(self):
        total = 0
        for price in self.calculate_prices():
            total += price
        return total
    
    def plot(self):
        # Initialize a list to store all payoff curves
        all_payoffs = []

        # Extract all K values from options
        all_K_values = [option.K for option in self.options]

        # Find the minimum and maximum K values
        min_K = min(all_K_values)
        max_K = max(all_K_values)

        # Generate the underlying range based on the minimum and maximum K values
        underlying_range = np.linspace(0.6 * min_K, 1.3 * max_K, 500)

        # Calculate and plot payoff curve for each option
        for option in self.options:
            payoffs = [option.calculate_payoff(underlying_price) for underlying_price in underlying_range]
            all_payoffs.append(payoffs)

        # Calculate the total payoff curve by summing all individual payoffs
        total_payoff = np.array(np.sum(all_payoffs, axis=0))

        # Plot the total payoff curve
        plt.plot(underlying_range, total_payoff, label='Total Payoff', color='black', linewidth=2)

        plt.axhline(y=0, color='black')  # Plot horizontal line at y=0
        plt.axvline(x=self.options[0].S, color='gray', linestyle='--', label='Market Price')
        plt.xlabel('Underlying Price')
        plt.ylabel('Payoff')
        plt.title('Payoff Diagram')

        # Calculate and plot breakeven points
        breakeven_points = []
        for i in range(len(total_payoff)-1):
            if total_payoff[i] * total_payoff[i+1] < 0:  # If the signs are different, it means there is a crossing between these two elements
                x1, x2 = underlying_range[i], underlying_range[i+1]
                y1, y2 = total_payoff[i], total_payoff[i+1]
                # Use linear interpolation to calculate the underlying_price at the crossing
                breakeven_point = x1 - y1 * (x2 - x1) / (y2 - y1)
                breakeven_points.append(breakeven_point)

        for breakeven_point in breakeven_points:
            plt.plot([breakeven_point], [0], 'bo', label=f'BEP: {breakeven_point:.2f}', alpha=0.3)
        
        # Loss Area
        plt.fill_between(underlying_range, total_payoff, where=(total_payoff <= 0), color='red', alpha=0.2, label='Profit Area')
        
        # Profit Area
        plt.fill_between(underlying_range, total_payoff, where=(total_payoff >= 0), color='green', alpha=0.2, label='Loss Area')
        plt.legend()
        plt.grid(True)
        plt.show()     

if __name__ == '__main__':
    # Initialize an empty list to store options data
    options_data = []

    S = float(input("Enter the market price: "))
    # Prompt the user to input options data until they finish
    while True:
        K = float(input("Enter the strike price: "))
        P = float(input("Enter the premium: "))
        LorS = input("Enter the direction (long/short): ")
        option_type = input("Enter the option type (call/put): ")
        
        # Append the options data to the list
        options_data.append((S, K, P, LorS, option_type))
        
        # Check if the user wants to continue entering data
        cont = input("Do you want to continue entering options data? (y/n): ")
        if cont.lower() != 'y':
            break

    # Create an instance of OrderOptions and pass in the options data
    order_options = OrderOptions(*options_data)
    
    # Calculate prices, total price, and plot the graph
    price = order_options.calculate_prices()
    total = order_options.total_prices()
    plot = order_options.plot()

    # Output prices and total price
    print("Option Prices:", price)
    print("Total Price:", total)

    # options_data = [
    #     (4000, 3600, 150, 'long', 'put'),
    #     (4000, 3800, 120, 'long', 'call'),
    #     (4000, 3500, 120, 'long', 'call'),
    #     (4000, 3700, 120, 'long', 'put')
    # ]