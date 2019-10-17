"""
Tyson Reimer
University of Manitoba
October 2nd, 2019
"""

import os
import matplotlib.pyplot as plt

from modules import get_proj_path, verify_path

###############################################################################

# Define the output directory, used to save the figures
__OUTPUT_DIR = os.path.join(get_proj_path(), 'output/figs/')
verify_path(__OUTPUT_DIR)

###############################################################################

# Define the mean and stdev values for each metric, obtained from
# logistic regression performance on test set
acc = (85, 4)
roc = (94.4, 0.5)
sens = (95, 6)
spec = (80, 10)

# Define the reported value and its uncertainty for each metric from
# EuCAP 2019 paper, using simulations
simu_roc = (94, 1)
simu_acc = (87, 1)
simu_sens = (83, 2)
simu_spec = (91, 2)

# Define your favourite color for the novel results
blue_color = [178, 224, 240]
blue_color = [ii / 255 for ii in blue_color]

# Define color for the past simulated results
grey_color = [99, 99, 99]
grey_color = [ii / 255 for ii in grey_color]

###############################################################################


if __name__ == '__main__':

    # Make the fig, define its size, set the font and tick label size
    plt.figure(figsize=(12, 6))
    plt.rc('font', family='Times New Roman')
    plt.tick_params(labelsize=28)

    new_xs = [1, 3.5, 6, 8.5]
    simu_xs = [2, 4.5, 7, 9.5]

    # Make the bars for the new results
    plt.bar(new_xs,
            height=[roc[0], acc[0], sens[0], spec[0]],
            yerr=[roc[1], acc[1], sens[1], spec[1]],
            width=0.75,
            color=blue_color,
            capsize=10,
            linewidth=1,
            edgecolor='k',
            label='Logistic Regression on UM-BMID')

    # Make the bars for the old simulated results
    plt.bar(simu_xs,
            height=[simu_roc[0], simu_acc[0], simu_sens[0], simu_spec[0]],
            yerr=[simu_roc[1], simu_acc[1], simu_sens[1], simu_spec[1]],
            width=0.75,
            color=grey_color,
            capsize=10,
            linewidth=1,
            edgecolor='k',
            label='SVM RBF on Simulated Data [28]')

    plt.legend(fontsize=24,
               loc='lower left',
               framealpha=0.95)

    # Label each bar
    plt.xticks([1.5, 4, 6.5, 9],
               ['ROC AUC',
                'Accuracy',
                'Sensitivity',
                'Specificity'],
               size=28)

    # Label the y-axis and give a title to the plot
    plt.ylabel('Metric Value (%)', fontsize=28)
    plt.title('Logistic Regression Performance on Test Set\n'
              'Compared to Simulated Results from [28]',
              fontsize=35)

    # Put text for each value onto the figure itself, for the
    # NEW results (experimental)
    plt.text(new_xs[0], 88.5,
             '(%s ' % roc[0] + r'$\mathdefault{\pm}$ ' + '%s)%%' % roc[1],
             size=24,
             color='k',
             horizontalalignment='center',
             verticalalignment='center',
             bbox={'facecolor': 'w',
                   'alpha': 0.9})
    plt.text(new_xs[1], 73,
             '(%s ' % acc[0] + r'$\mathdefault{\pm}$ ' + '%s)%%' % acc[1],
             size=24,
             color='k',
             horizontalalignment='center',
             verticalalignment='center',
             bbox={'facecolor': 'w',
                   'alpha': 0.9})
    plt.text(new_xs[2], 85,
             '(%s ' % sens[0] + r'$\mathdefault{\pm}$ ' + '%s)%%' % sens[1],
             size=24,
             color='k',
             horizontalalignment='center',
             verticalalignment='center',
             bbox={'facecolor': 'w',
                   'alpha': 0.9})
    plt.text(new_xs[3], 65,
             '(%s ' % spec[0] + r'$\mathdefault{\pm}$ ' + '%s)%%' % spec[1],
             size=24,
             color='k',
             horizontalalignment='center',
             verticalalignment='center',
             bbox={'facecolor': 'w',
                   'alpha': 0.9})

    # Put text for each value onto the figure itself, for the
    # OLD results (simulated)
    plt.text(simu_xs[0], 82.5,
             '(%s ' % simu_roc[0] + r'$\mathdefault{\pm}$ ' + '%s)%%'
             % simu_roc[1],
             size=24,
             color='k',
             horizontalalignment='center',
             verticalalignment='center',
             bbox={'facecolor': 'w',
                   'alpha': 0.9})
    plt.text(simu_xs[1], 80,
             '(%s ' % simu_acc[0] + r'$\mathdefault{\pm}$ ' + '%s)%%'
             % simu_acc[1],
             size=24,
             color='k',
             horizontalalignment='center',
             verticalalignment='center',
             bbox={'facecolor': 'w',
                   'alpha': 0.9})
    plt.text(simu_xs[2], 75,
             '(%s ' % simu_sens[0] + r'$\mathdefault{\pm}$ ' + '%s)%%'
             % simu_sens[1],
             size=24,
             color='k',
             horizontalalignment='center',
             verticalalignment='center',
             bbox={'facecolor': 'w',
                   'alpha': 0.9})
    plt.text(simu_xs[3], 85,
             '(%s ' % simu_spec[0] + r'$\mathdefault{\pm}$ ' + '%s)%%'
             % simu_spec[1],
             size=24,
             color='k',
             horizontalalignment='center',
             verticalalignment='center',
             bbox={'facecolor': 'w',
                   'alpha': 0.9})

    # Set appropriate y-limit
    plt.ylim([50, 100])
    plt.tight_layout()  # Make everything fit nicely
    plt.show()  # Display the plot

    # Save the figure
    plt.savefig(os.path.join(__OUTPUT_DIR, 'test-bars.png'),
                transparent=True,  # Set transparent background
                dpi=600  # Set DPI to make fig with good resolution
                )
