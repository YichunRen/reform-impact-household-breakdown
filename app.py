import streamlit as st
import pandas as pd
import random
from policyengine_us import Simulation
from policyengine_us import Microsimulation
from policyengine_core.reforms import Reform
from policyengine_core.periods import instant
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
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
st.header("Raw Data", divider="rainbow")
st.dataframe(
    difference_person_df,
    hide_index=True,
)

# Penalty
penalty_df = (
    difference_person_df.groupby(by="household_id", as_index=False)
    .agg(
        {
            "household_net_income_diff": "mean",
            "relative_change": "mean",
            "person_id": "count",
            "household_net_income_base": "mean",
            "household_income_decile": "mean",
        }
    )
    .sort_values(by="relative_change", ascending=True)
    .rename(
        columns={
            "relative_change": "household_net_income_relative_diff",
            "person_id": "family_size",
            "household_net_income_base": "household_net_income",
        }
    )
)

st.header("Household net income changes", divider="rainbow")

# Add histogram data
x1 = np.random.randn(200)
x2 = np.random.randn(200) + 2
# Group data together
hist_data = [x1, x2]
group_labels = ["Before reform", "After reform"]
fig = ff.create_distplot(hist_data, group_labels, bin_size=[0.1, 0.25, 0.5])
st.plotly_chart(fig, use_container_width=True)

st.divider()

# histogram
fig1, ax1 = plt.subplots()
ax1.hist(penalty_df["household_net_income_relative_diff"], rwidth=0.85)
ax1.set_title("Distribution of household net income relative differences")
ax1.set_xlabel("Frequency")
ax1.set_ylabel("Ralative difference")
st.pyplot(fig1)

st.divider()

# penalties section
st.subheader("Top 10 :red[Penalties] :arrow_down:")
st.dataframe(
    penalty_df.head(10)
    .reset_index(drop=True)
    .set_axis(range(1, 11))
)

st.divider()

# Bonus section
st.subheader("Top 10 :green[Bonuses] :arrow_up:")
st.dataframe(
    penalty_df
    .sort_values(by="household_net_income_relative_diff", ascending=False)
    .head(10)
    .reset_index(drop=True)
    .set_axis(range(1, 11))
)
bonus_income_tab, bonus_family_tab = st.tabs(
    ["Income Status", "Family Status"]
)
with bonus_income_tab:
    temp = (
        penalty_df.sort_values(
            by="household_net_income_relative_diff", ascending=False
        )[
            [
                "household_id",
                "household_net_income",
                "household_income_decile",
                "family_size",
            ]
        ]
        .head(10)
        .reset_index(drop=True)
    )
    average_household_income = temp["household_net_income"].mean()
    average_family_size = temp["family_size"].mean()
    # Average of household income (metric)
    st.metric(
        label="Average Household income",
        value="$" + str(int(average_household_income)),
    )
    with st.expander("Household income decile distribution"):
        # Household income decile distribution (pie chart)
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=temp["household_income_decile"]
                    .value_counts()
                    .index,
                    values=temp["household_income_decile"]
                    .value_counts()
                    .values,
                )
            ]
        )
        fig.update_traces(
            hoverinfo="label+percent",
            textinfo="value",
            textfont_size=20,
            marker=dict(line=dict(color="#000000", width=2)),
        )
        st.plotly_chart(fig, use_container_width=True)
    with st.expander("Household income data table"):
        # Total Household income (Table)
        st.dataframe(
            temp[["household_id", "household_net_income"]],
            hide_index=True,
        )
with bonus_family_tab:
    st.metric(
        label="Average family size",
        value=str(int(average_family_size)),
    )


st.header("Data Analysis", divider="rainbow")

# scatterplot
st.subheader("Relationship between :blue[change] and :orange[age]")
st.scatter_chart(data=difference_person_df, x="age", y="relative_change")
st.subheader("Relationship between :blue[change] and :orange[poverty]")
st.scatter_chart(
    data=difference_person_df,
    x="in_poverty",
    y="relative_change",
    color="#ffaa00",
)

# Number of dependent (data table) / distribution (pie chart)
# Average number of dependent (metric)
# Dataframe styling
