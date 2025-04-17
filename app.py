import streamlit as st

def normalize(value, min_val, max_val):
    return max(0, min(100, (value - min_val) / (max_val - min_val) * 100))

def score_customer(
    credit_score, income, time_at_job, time_at_residence,
    prev_repossession, num_repos, time_at_prev_job,
    has_checking_account, down_payment
):
    credit_score_norm = normalize(credit_score, 400, 700)
    income_norm = normalize(income, 19200, 100000)
    residence_time_norm = normalize(time_at_residence, 0, 3)
    prev_job_time_norm = normalize(time_at_prev_job, 0, 3)
    down_payment_norm = normalize(down_payment, 1500, 10000)

    # Stronger job stability logic
    if time_at_job >= 2:
        job_time_score = 100
    elif time_at_job < 1 and time_at_prev_job >= 2:
        job_time_score = 100
    else:
        job_time_score = normalize(time_at_job, 0, 2) * 0.3 + prev_job_time_norm * 0.7

    income_job_score = (income_norm * 0.35 + job_time_score * 0.65)

    # Repossession penalty
    if prev_repossession == "Yes":
        repo_penalty = 10 if num_repos == 1 else 25
    else:
        repo_penalty = 0

    checking_bonus = 10 if has_checking_account == "Yes" else 0

    # Adjusted scoring formula
    final_score = (
        credit_score_norm * 0.20 +
        income_job_score * 0.35 +
        residence_time_norm * 0.10 +
        down_payment_norm * 0.20 +
        prev_job_time_norm * 0.05 +
        checking_bonus +
        (-repo_penalty) * 0.8
    )

    return round(max(0, min(final_score, 100)), 2)

# Streamlit App UI
st.set_page_config(page_title="Customer Scoring App", layout="centered")
st.title("🏁 Dealership Customer Scoring")

credit_score = st.number_input("Credit Score", 400, 700, value=560)
income = st.number_input("Annual Income ($)", 19200, 200000, value=36000)
time_at_job = st.number_input("Time at Current Job (years)", 0.0, 50.0, value=1.0)
time_at_residence = st.number_input("Time at Residence (years)", 0.0, 50.0, value=1.0)
prev_job_time = st.number_input("Time at Previous Job (years)", 0.0, 50.0, value=2.0)
down_payment = st.number_input("Down Payment Amount ($)", 1500, 10000, value=1500)

prev_repossession = st.radio("Previous Repossessions?", ("No", "Yes"))
num_repos = st.slider("How many repossessions?", 1, 3, 1) if prev_repossession == "Yes" else 0
has_checking_account = st.radio("Do you have a checking account?", ("Yes", "No"))

if st.button("Calculate Score"):
    score = score_customer(
        credit_score, income, time_at_job, time_at_residence,
        prev_repossession, num_repos, prev_job_time,
        has_checking_account, down_payment
    )

    st.subheader(f"Customer Score: **{score}/100**")
    if score >= 85:
        st.success("Excellent Lead ✅")
    elif score >= 75:
        st.info("Good Lead 👍")
    elif score >= 60:
        st.warning("Moderate Lead ⚠️")
    else:
        st.error("Low Quality Lead ❌")
