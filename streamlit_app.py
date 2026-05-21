import streamlit as st

st.set_page_config(page_title="Onboarding Cost Calculator", page_icon="📊", layout="centered")

st.title("Onboarding Cost Calculator")
st.markdown(
    "Enter your onboarding assumptions below to compute the one-time onboarding cost plus monthly and annual running costs."
)

st.header("One-time onboarding cost")
setup_fee = st.number_input("Setup fee ($)", min_value=0.0, value=5000.0, step=100.0, format="%.2f")
training_hours = st.number_input("Training hours", min_value=0.0, value=20.0, step=1.0)
training_rate = st.number_input("Training hourly rate ($)", min_value=0.0, value=150.0, step=5.0, format="%.2f")
data_migration_cost = st.number_input("Data migration cost ($)", min_value=0.0, value=2000.0, step=100.0, format="%.2f")
consulting_cost = st.number_input("Consulting / implementation cost ($)", min_value=0.0, value=3000.0, step=100.0, format="%.2f")

st.header("Running costs")
monthly_license = st.number_input("Monthly license or subscription cost ($)", min_value=0.0, value=1200.0, step=50.0, format="%.2f")
monthly_support = st.number_input("Monthly support or maintenance cost ($)", min_value=0.0, value=800.0, step=50.0, format="%.2f")
monthly_cloud = st.number_input("Monthly infrastructure / cloud cost ($)", min_value=0.0, value=1000.0, step=50.0, format="%.2f")
additional_monthly = st.number_input("Additional monthly operating cost ($)", min_value=0.0, value=500.0, step=50.0, format="%.2f")

st.header("Optional onboarding scope")
user_count = st.number_input("Number of onboarded users", min_value=0, value=50, step=1)
st.write(
    "Optional: use this value for per-user estimates or to compare how onboarding scale impacts total cost. "
)

# calculations
training_cost = training_hours * training_rate
one_time_cost = setup_fee + training_cost + data_migration_cost + consulting_cost
monthly_running_cost = monthly_license + monthly_support + monthly_cloud + additional_monthly
yearly_running_cost = monthly_running_cost * 12
cost_per_user = one_time_cost / user_count if user_count > 0 else 0.0

st.divider()

st.subheader("Results")
col1, col2 = st.columns(2)
with col1:
    st.metric("One-time onboarding cost", f"${one_time_cost:,.2f}")
    st.metric("Monthly running cost", f"${monthly_running_cost:,.2f}")
with col2:
    st.metric("Annual running cost", f"${yearly_running_cost:,.2f}")
    st.metric("Onboarding cost per user", f"${cost_per_user:,.2f}")

st.markdown("---")

st.subheader("Cost breakdown")
st.write(
    f"- Setup fee: ${setup_fee:,.2f}\n"
    f"- Training cost: ${training_cost:,.2f} ({training_hours} hrs @ ${training_rate:,.2f}/hr)\n"
    f"- Data migration: ${data_migration_cost:,.2f}\n"
    f"- Consulting / implementation: ${consulting_cost:,.2f}\n"
    f"- Monthly license: ${monthly_license:,.2f}\n"
    f"- Monthly support: ${monthly_support:,.2f}\n"
    f"- Monthly cloud: ${monthly_cloud:,.2f}\n"
    f"- Additional monthly operating cost: ${additional_monthly:,.2f}"
)

st.caption("Use the input fields above to adjust assumptions and see how the one-time and recurring costs change.")
