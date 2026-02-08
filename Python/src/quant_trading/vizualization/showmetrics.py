import matplotlib.pyplot as plt

def show_CalcMaxdrawdur(cumreturns, max_drawdown, max_drawdown_duration, mdd_date, wealth_index, drawdowns):

    # Create a subplot: Top is Price, Bottom is Drawdown
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
    # Top Plot: Wealth Index
    ax1.plot(wealth_index.index, wealth_index, label='Wealth Index', color='blue', linewidth=1.5)
    ax1.set_title('Strategy Equity Curve')
    ax1.legend()

    # Bottom Plot: Drawdown Shading
    ax2.fill_between(drawdowns.index, drawdowns, 0, color='red', alpha=0.3, label='Drawdown Area')
    ax2.set_title('Drawdown Illustration (Underwater Periods)')
    ax2.set_ylabel('Drawdown %')


    # Add text box to the plot
    textstr = f'Max Drawdown: {max_drawdown:.2%}\nMax Duration: {max_drawdown_duration} periods'
    ax1.text(0.02, 0.98, textstr, transform=ax1.transAxes, fontsize=12,
            verticalalignment='top')

    ax1.annotate(f'Max Drawdown: {max_drawdown:.2%}', 
                xy=(mdd_date, wealth_index.loc[mdd_date]),
                xytext=(mdd_date, wealth_index.loc[mdd_date] * 0.9),
                arrowprops=dict(facecolor='black', shrink=0.05),
                fontsize=12, fontweight='bold', color='red')
