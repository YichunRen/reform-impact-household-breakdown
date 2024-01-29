import streamlit as st
import pandas as pd
import random
from policyengine_us import Simulation
from policyengine_us import Microsimulation
from policyengine_core.reforms import Reform
from policyengine_core.periods import instant
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import numpy as np

# Create sample data
column_names = [
    "person_id",
    "household_id",
    "age",
    "household_net_income_diff",
    "household_income_decile",
    "in_poverty",
    "household_tax",
    "household_benefits",
    "household_net_income_base",
    "relative_change",
]
sample_value = []
for _ in range(100):
    random_numbers = [random.randint(-100, 100) for _ in range(10)]
    sample_value.append(random_numbers)
sample_data = [dict(zip(column_names, value)) for value in sample_value]

difference_person_df = pd.DataFrame(columns=column_names)
difference_person_df = difference_person_df._append(
    sample_data, ignore_index=True
)

st.title(":rainbow[_Output Demo_]")
# Create data display table
# Random Raw data
st.header('Raw Data', divider='rainbow')
st.dataframe(
    difference_person_df,
    hide_index=True,
)


# Penalty
penalty_df = (difference_person_df.groupby(by="household_id", as_index=False)
.agg({"household_net_income_diff": "mean", "relative_change": "mean"})
.sort_values(by="relative_change", ascending=True)
.rename(columns={"relative_change": "household_net_income_relative_diff"}))

st.header('Household net income changes', divider='rainbow')

# Add histogram data
x1 = np.random.randn(200) 
x2 = np.random.randn(200) + 2
# Group data together
hist_data = [x1, x2]
group_labels = ['Before reform', 'After reform']
fig = ff.create_distplot(
        hist_data, group_labels, bin_size=[.1, .25, .5])
st.plotly_chart(fig, use_container_width=True)

st.divider()

# histogram
fig1, ax1 = plt.subplots()
ax1.hist(penalty_df['household_net_income_relative_diff'], rwidth=0.85)
ax1.set_title('Distribution of household net income relative differences')
ax1.set_xlabel('Frequency')
ax1.set_ylabel('Ralative difference')
st.pyplot(fig1)

st.divider()

# penalties
st.subheader("Top 10 :red[Penalties] :arrow_down:")
st.dataframe(
    penalty_df.head(10)
    .reset_index()
    .set_axis(range(1, 11))
)

st.divider()

# Bonus
st.subheader("Top 10 :green[Bonuses] :arrow_up:")
st.dataframe(
    penalty_df
    .sort_values(by="household_net_income_relative_diff", ascending=False)
    .head(10)
    .reset_index()
    .set_axis(range(1, 11))
)

st.header('Data Analysis', divider='rainbow')

#scatterplot
st.subheader("Relationship between :blue[change] and :orange[age]")
st.scatter_chart(data = difference_person_df, x = 'age', y = 'relative_change')
st.subheader("Relationship between :blue[change] and :orange[poverty]")
st.scatter_chart(data = difference_person_df, x = 'in_poverty', y = 'relative_change', color='#ffaa00')

