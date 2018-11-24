# Decision Science 101 Final Project - Group 9

Analysis of the effect of pre-existing preferences on the choice overload effect.

This repository contains the code used to analyze data collected from a Qualtrics survey.

## Data Processing

The data were exported from Qualtrics as a CSV format and then processed in Excel in order to remove irrelevant information such as IP address, date/time, and so on.

Then, the records were split into four different groups based on which columns were non-null:

```python
# Split into confidence values for each type of question
meal_short = data['meal_short'].dropna()
meal_long = data['meal_long'].dropna()

class_short = data['class_short'].dropna()
class_long = data['class_long'].dropna()
```

## Statistical Analysis

### T-Tests

Four T-tests were performed on the data using the `stats` package from `scipy`.

Two of these tests were aggregate/combined tests, and so the relevant data were combined into aggregate `DataFrame` objects and then the T-tests were run on those aggregate objects.

```python
# Run T test for meals
meals_t, meals_p = stats.ttest_ind(meal_short, meal_long)

# Run T test for classes
class_t, class_p = stats.ttest_ind(class_short, class_long)

# Run T test across groups:
# First, combine classes and combine meals
class_all = pd.concat([class_short, class_long], ignore_index=True)
meal_all = pd.concat([meal_short, meal_long], ignore_index=True)

# Then, run the test
combined_t, combined_p = stats.ttest_ind(class_all, meal_all)

# Run T test across all shorts and all longs:
# First, combine shorts and combine longs
short_all = pd.concat([class_short, meal_short], ignore_index=True)
long_all = pd.concat([class_long, meal_long], ignore_index=True)

# Then, run the test
comb_2_t, comb_2_p = stats.ttest_ind(short_all, long_all)
```

The results of these T-tests were:

```
Meals:     T = 1.7696545138428823,  P = 0.07938985600664483
Classes:   T = 0.24361622467144387, P = 0.24361622467144387
Combined:  T = -0.9312622018447003, P = 0.3526736589969208
Combined2: T = 2.0697634338884923,  P = 0.03956754951327441
```

### 2x2 ANOVA

In addition, the `statsmodels` package was used to perform a 2-way ANOVA. After the satisfaction values
were aggregated into lists by category, the following code was used for the ANOVA:

```python
formula = 'Satisfaction ~ C(Type) + C(Length) + C(Type):C(Length)'
model = ols(formula, aggregate).fit()
aov_table = statsmodels.stats.anova.anova_lm(model, typ=1)
```

The results of the ANOVA were:

```
                      df      sum_sq    mean_sq         F    PR(>F)
C(Type)              1.0    3.582745   3.582745  0.875582  0.350383
C(Length)            1.0   17.122664  17.122664  4.184584  0.041916
C(Type):C(Length)    1.0    0.300051   0.300051  0.073329  0.786790
Residual           233.0  953.399603   4.091844       NaN       NaN
```

## Results Visualization

The `pyplot` package from `matplotlib` was used to create a full visualization of the data consisting of a series of histograms outlining the preference reported by users for each category of question.

Graphs were creates as follows:

```python
plt.subplot(4, 2, 1)    # 1st plot
plt.title('Meals (short)')
plt.xlabel('Satisfaction Level')
plt.ylabel('Responses')
plt.hist(
    meal_short,
    bins=range(1, 11), # 1, 2, ..., 10
    rwidth=0.75,
    label='Meals (short)'
)

...

# Fix overlapping in layout, and then display the plots
plt.tight_layout()
plt.gcf().canvas.set_window_title('Results')    # Window title
plt.show()
```

This resulted in the following visualization:

![results-all](https://user-images.githubusercontent.com/10100323/48680965-7879a200-eb6d-11e8-83e7-04011268514a.png)


## Website

A website view of this readme is hosted at [decsci.raduvasilescu.com](http://decsci.raduvasilescu.com).

This host is specified in the `CNAME` file in this repository, and the main HTML page template has been adjusted
from the default Jekyll theme and can be found in `_layouts/default.html`.

## Project Contributors

- Radu Vasilescu
- Zoe Tang
- Claire Hutchinson
- Prateek Khandelwal
