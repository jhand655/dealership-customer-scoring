import streamlit as st

def normalize(value, min_val, max_val):
    return max(0, min(100, (value - min_val) / (max_val - min_val) * 100))

def score_customer(
    credit_score, income, time_at_job, time_at_residence,
    prev_repossession, num_repos, time_at_prev_job,
    has_checking_account, down_payment
):
    # New normalization to match "average" with 60-70+
    credit_score_norm = normalize(credit_score, 300, 850)
    income_norm = normalize(income, 19200, 60000)  # Narrowed top to $60K
    residence_time_norm = normalize(time_at_residence, 0, 10)  # Average residence ~2-5 years
    prev_job_time_norm = normalize(time_at_prev_job, 0, 10)
    down_payment_norm = normalize(down_payment, 1000, 5000)  # Most avg down payments in $1K–$5K

    # Job time logic
    if time_at_job >= 2:
        job_time_score = 100
    elif time_at_job < 1 and time_at_prev_job >= 2:
        job_time_score = 85
    else:
        job_time_score = normalize(time_at_job, 0, 2) * 0.5 + prev_job_time_norm * 0.5

    income_job_score = (income_norm * 0.5 + job_time_score * 0.5)

    # Original repo penalty retained
    if prev_repossession == "Yes":
        repo_penalty = 10 if num_repos == 1 else 25
    else:
        repo_penalty = 0

    checking_bonus = 10 if has_checking_account == "Yes" else 0

    # Weighted scoring
    final_score = (
        credit_score_norm * 0.30 +
        income_job_score * 0.30 +
        residence_time_norm * 0.15 +
        down_payment_norm * 0.15 +
        prev_job_time_norm * 0.05 +
        checking_bonus +
        (-repo_penalty) * 0.05
    )

    return round(max(0, min(final_score, 100)), 2)
