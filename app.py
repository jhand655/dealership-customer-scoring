import streamlit as st

def normalize(value, min_val, max_val):
    return max(0, min(100, (value - min_val) / (max_val - min_val) * 100))

def score_customer(
    credit_score, income, time_at_job, time_at_residence,
    prev_repossession, num_repos, time_at_prev_job,
    has_checking_account, down_payment
):
    # Adjusted normalization to reflect average credit score of 580
    credit_score_norm = normalize(credit_score, 400, 800)  # Shifted range slightly lower
    income_norm = normalize(income, 19200, 200000)  # Adjusted minimum to 19200
    residence_time_norm = normalize(time_at_residence, 0, 30)
    prev_job_time_norm = normalize(time_at_prev_job, 0, 30)
    down_payment_norm = normalize(down_payment, 1000, 10000)

    # Job time logic
    if time_at_job >= 2:
        job_time_score = 100
    elif time_at_job < 1 and time_at_prev_job >= 2:
        job_time_score = 80
    else:
        job_time_score = normalize(time_at_job, 0, 2) * 0.7 + prev_job_time_norm * 0.3

    # Income check and job weighting
    if income < 19200:
        income_job_score = 0
    else:
        income_job_score = (income_norm * 0.5 + job_time_score * 0.5)

    # Repossession penalty
    if prev_repossession == "Yes":
        if num_repos == 1:
            repo_penalty = 10
        else:
            repo_penalty = 25
    else:
        repo_penalty = 0

    # Checking account bonus
    checking_bonus = 10 if has_checking_account == "Yes" else 0

    # Final score calculation
    final_score = (
        credit_score_norm * 0.25 +
        income_job_score * 0.30 +
        residence_time_norm * 0.10 +
        prev_job_time_norm * 0.10 +
        down_payment_norm * 0.10 +
        checking_bonus +
        (-repo_penalty) * 0.15
    )

    return round(max(0, min(final_score, 100)), 2)

# Streamlit App UI
st.set_page_config(page_title="Customer Scoring App", layout="centered")
st.title("🏁 Dealership Customer Scoring")
st.markdown("Enter customer details to calculate a score (0–100):")

# Inputs
credit_score = st.number_input("Credit Score", min_value=300, max_value=850, value=680)
income = st.number_input("Annual Income ($)", min_value=19200, max_value=200000, value=55000)
time_at_job = st.number_input("Time at Current Job (years)", min_value=0.0, max_value=50.0, value=1.0)
time_at_residence = st.number_input("Time at Residence (years)", min_value=0.0, max_value=50.0, value=3.0)
prev_job_time = st.number_input("Time at Previous Job (years)", min_value=0.0, max_value=50.0, value=3.0)
down_payment = st.number_input("Down Payment Amount ($)", min_value=1000, max_value=10000, value=2000)

prev_repossession = st.radio("Previous Repossessions?", ("No", "Yes"))
if prev_repossession == "Yes":
    num_repos = st.slider("How many repossessions?", 1, 5, 1)
else:
    num_repos = 0

has_checking_account = st.radio("Do you have a checking account?", ("Yes", "No"))

# Scoring
if st.button("Calculate Score"):
    score = score_customer(
        credit_score, income, time_at_job, time_at_residence,
        prev_repossession, num_repos, prev_job_time,
        has_checking_account, down_payment
    )

    st.subheader(f"Customer Score: **{score}/100**")
    if score >= 80:
        st.success("High Quality Lead ✅")
    elif score >= 60:
        st.info("Moderate Quality Lead ⚠️")
    else:
        st.warning("Low Quality Lead ❌")
