"""
Data analysis program for Decision Science 101 research project - Group 9

Author: Radu Vasilescu
Date:   2018-11-07
"""

import pandas as pd
import numpy as np

from scipy import stats

# For 2-way ANOVA
import statsmodels
import statsmodels.api as sm
from statsmodels.formula.api import ols

import matplotlib.pyplot as plt

# ===== Data Ingest ===== #

# Read the data from the data file
data = pd.read_csv('data.csv')

# Split into confidence values for each type of question
meal_short = data['meal_short'].dropna()
meal_long = data['meal_long'].dropna()

class_short = data['class_short'].dropna()
class_long = data['class_long'].dropna()


# ===== Statistical Tests ===== #

# Run T test for meals
# meals_t, meals_p = stats.ttest_ind(meal_short, meal_long)

# Run T test for classes
# class_t, class_p = stats.ttest_ind(class_short, class_long)

# Run T test across groups:
# First, combine classes and combine meals
# class_all = pd.concat([class_short, class_long], ignore_index=True)
# meal_all = pd.concat([meal_short, meal_long], ignore_index=True)

# Then, run the test
# combined_t, combined_p = stats.ttest_ind(class_all, meal_all)

# Run T test across all shorts and all longs:
# First, combine shorts and combine longs
short_all = pd.concat([class_short, meal_short], ignore_index=True)
long_all = pd.concat([class_long, meal_long], ignore_index=True)

# Then, run the test
# comb_2_t, comb_2_p = stats.ttest_ind(short_all, long_all)

# 2-way ANOVA

# Make a new, aggregate DataFrame with all satisfaction values, question 
# type, and answer choice count
aggregate_arr = data.to_dict()

# print(aggregate_arr)

satisfactions = None
types = []
lengths = []

satisfactions = pd.concat([short_all, long_all], ignore_index=True).values.tolist()
# print(satisfactions)

# Classes: 0 | Meal Plans: 1
# Short: 0  | Long: 1

for _ in range(class_short.size):
    types.append(0)
    lengths.append(0)

for _ in range(meal_short.size):
    types.append(1)
    lengths.append(0)

for _ in range(class_long.size):
    types.append(0)
    lengths.append(1)

for _ in range(meal_long.size):
    types.append(1)
    lengths.append(1)

aggregate = pd.DataFrame({
    'Satisfaction': satisfactions,
    'Type': types,
    'Length': lengths
})

print(aggregate.head())

formula = 'Satisfaction ~ C(Type) + C(Length) + C(Type):C(Length)'
model = ols(formula, aggregate).fit()
aov_table = statsmodels.stats.anova.anova_lm(model, typ=1)


# ===== Report Results ===== #

# Display statistical test results
# print('Meals:     T = ' + str(meals_t) + ', P = ' + str(meals_p))
# print('Classes:   T = ' + str(class_p) + ', P = ' + str(class_p))
# print('Combined:  T = ' + str(combined_t) + ', P = ' + str(combined_p))
# print('Combined2: T = ' + str(comb_2_t) + ', P = ' + str(comb_2_p))

print(aov_table)    # ANOVA results

# --- Plot results graphically ---

# Meals

# plt.subplot(4, 2, 1)    # 1st plot
# plt.title('Meals (short)')
# plt.xlabel('Satisfaction Level')
# plt.ylabel('Responses')
# plt.hist(
#     meal_short,
#     bins=range(1, 11), # 1, 2, ..., 10
#     rwidth=0.75,
#     label='Meals (short)'
# )

# plt.subplot(4, 2, 2)    # Go to the 2nd subplot
# plt.title('Meals (long)')
# plt.xlabel('Satisfaction Level')
# plt.ylabel('Responses')
# plt.hist(
#     meal_long,
#     bins=range(1, 11),
#     rwidth=0.75,
#     label='Meals (long)'
# )

# # Classes

# plt.subplot(4, 2, 3)
# plt.title('Classes (short)')
# plt.xlabel('Satisfaction Level')
# plt.ylabel('Responses')
# plt.hist(
#     class_short,
#     bins=range(1, 11),
#     rwidth=0.75,
#     label='Classes (short)'
# )

# plt.subplot(4, 2, 4)
# plt.title('Classes (long)')
# plt.xlabel('Satisfaction Level')
# plt.ylabel('Responses')
# plt.hist(
#     class_long,
#     bins=range(1, 11),
#     rwidth=0.75,
#     label='Classes (long)'
# )

# # Combined

# plt.subplot(4, 2, 5)
# plt.title('Classes (all)')
# plt.xlabel('Satisfaction Level')
# plt.ylabel('Responses')
# plt.hist(
#     class_all,
#     bins=range(1, 11),
#     rwidth=0.75,
#     label='Classes (all)'
# )

# plt.subplot(4, 2, 6)
# plt.title('Meals (all)')
# plt.xlabel('Satisfaction Level')
# plt.ylabel('Responses')
# plt.hist(
#     meal_all,
#     bins=range(1, 11),
#     rwidth=0.75,
#     label='Meals (all)'
# )

# # Combined 2

# plt.subplot(4, 2, 7)
# plt.title('Short (all)')
# plt.xlabel('Satisfaction Level')
# plt.ylabel('Responses')
# plt.hist(
#     short_all,
#     bins=range(1, 11),
#     rwidth=0.75,
#     label='Short (all)'
# )

# plt.subplot(4, 2, 8)
# plt.title('Long (all)')
# plt.xlabel('Satisfaction Level')
# plt.ylabel('Responses')
# plt.hist(
#     long_all,
#     bins=range(1, 11),
#     rwidth=0.75,
#     label='Longs (all)'
# )

# # Fix overlapping in layout, and then display the plots
# plt.tight_layout()
# plt.gcf().canvas.set_window_title('Results')    # Window title
# plt.show()
