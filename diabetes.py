import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\Anton\Downloads\diabetes.csv")
    df = df.rename(columns={"Diabetes_012": "Diabetes"})
    return df

df = load_data()
st.sidebar.header("Filter Options")
gender = st.sidebar.selectbox("Select Gender", options=['All', 'Male', 'Female'])

age_labels = {
    1: "18-24", 2: "25-29", 3: "30-34", 4: "35-39", 5: "40-44",
    6: "45-49", 7: "50-54", 8: "55-59", 9: "60-64", 10: "65-69",
    11: "70-74", 12: "75-79", 13: "80+"
}
df['AgeGroup'] = df['Age'].map(age_labels)

selected_groups = st.sidebar.multiselect(
    "Select Age Group(s)",
    options=list(age_labels.values()),
    default=list(age_labels.values())
)

if gender != 'All':
    gender_val = 1.0 if gender == 'Male' else 0.0
    df = df[df['Sex'] == gender_val]
df = df[df['AgeGroup'].isin(selected_groups)]

st.title("Interactive Diabetes Risk Factors Dashboard")
st.markdown("Explore health indicators by gender and age group. Use the filters to adjust the view.")
st.subheader("Diabetes Status Distribution")
diabetes_counts = df['Diabetes'].value_counts().rename({0.0: "No Diabetes", 1.0: "Diabetes", 2.0: "Prediabetes"})
fig1 = px.pie(values=diabetes_counts.values, names=diabetes_counts.index,
              title="Proportion of Diabetes Status", hole=0.4)
st.plotly_chart(fig1)

st.subheader("Income Levels (in %)")
income_dist = df.groupby(['Diabetes', 'Income']).size().reset_index(name='Count')
total_per_class = income_dist.groupby('Diabetes')['Count'].transform('sum')
income_dist['Percentage'] = (income_dist['Count'] / total_per_class * 100).round(2)
income_dist['Diabetes'] = income_dist['Diabetes'].map({0.0: "No", 1.0: "Yes", 2.0: "Prediabetes"})
fig2 = px.bar(
    income_dist,
    x="Income",
    y="Percentage",
    color="Diabetes",
    barmode="group",
    text_auto=True,
    labels={"Income": "Income Group (1 = lowest, 8 = highest)"},
    title="Normalized Income Distribution by Diabetes Status"
)
st.plotly_chart(fig2)
st.caption("Income: 1 = <10k, 2 = 10k–15k, ..., 8 = >75k (in $)")

st.subheader("Unhealthy Habits")
st.markdown("This chart shows the percentage of people in each diabetes group who answered 'Yes' to smoking or heavy alcohol use.")
habit_df = df.groupby('Diabetes')[['Smoker', 'HvyAlcoholConsump']].mean().reset_index()
habit_df['Diabetes'] = habit_df['Diabetes'].map({0.0: "No", 1.0: "Yes", 2.0: "Prediabetes"})
habit_df = habit_df.melt(id_vars='Diabetes', var_name='Habit', value_name='Percentage')
habit_df['Percentage'] = (habit_df['Percentage'] * 100).round(2)
fig3 = px.bar(
    habit_df,
    x='Habit',
    y='Percentage',
    color='Diabetes',
    barmode='group',
    text_auto=True,
    labels={'Habit': 'Habit Type', 'Percentage': '% of Group'},
    title="Smoking and Alcohol Use by Diabetes Status"
)
st.plotly_chart(fig3)

st.subheader("Health Metrics")
health_df = df.groupby('Diabetes')[['PhysActivity', 'Stroke', 'HeartDiseaseorAttack']].mean().reset_index()
health_df['Diabetes'] = health_df['Diabetes'].map({0.0: "No", 1.0: "Yes", 2.0: "Prediabetes"})
health_df = health_df.melt(id_vars='Diabetes', var_name='Condition', value_name='Percentage')
health_df['Percentage'] = (health_df['Percentage'] * 100).round(2)
fig4 = px.bar(
    health_df,
    x='Condition',
    y='Percentage',
    color='Diabetes',
    barmode='group',
    text_auto=True,
    labels={'Condition': 'Health Indicator'},
    title="Health Metrics by Diabetes Status"
)
st.plotly_chart(fig4)

st.subheader("Dietary Habits")
diet_df = df.groupby('Diabetes')[['Fruits', 'Veggies']].mean().reset_index()
diet_df['Diabetes'] = diet_df['Diabetes'].map({0.0: "No", 1.0: "Yes", 2.0: "Prediabetes"})
diet_df = diet_df.melt(id_vars='Diabetes', var_name='Food', value_name='Percentage')
diet_df['Percentage'] = (diet_df['Percentage'] * 100).round(2)
fig5 = px.bar(
    diet_df,
    x='Food',
    y='Percentage',
    color='Diabetes',
    barmode='group',
    text_auto=True,
    labels={'Food': 'Food Type'},
    title="Fruit & Vegetable Consumption by Diabetes Status"
)
st.plotly_chart(fig5)

st.subheader("BMI Distribution")
df['Diabetes_Label'] = df['Diabetes'].map({0.0: "No", 1.0: "Yes", 2.0: "Prediabetes"})
fig6 = px.box(
    df,
    x='Diabetes_Label',
    y='BMI',
    color='Diabetes_Label',
    labels={'Diabetes_Label': 'Diabetes', 'BMI': 'Body Mass Index'},
    title="BMI by Diabetes Status"
)
st.plotly_chart(fig6)
st.markdown("---")