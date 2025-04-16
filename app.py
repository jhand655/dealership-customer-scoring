import streamlit as st

def normalize(value, min_val, max_val):
    return max(0, min(100, (value - min_val) / (max_val - min_val) * 100))

def score_customer(credit_score, income, time_at_job_years, time_at_residence_years):
    credit_score_norm = normalize(credit_score, 300, 850)
    income_norm = normalize(income, 15000, 200000)
    job_time_norm = normalize(time_at_job_years, 0, 30)
    residence_time_norm = normalize(time_at_residence_years, 0, 30)

    income_job_score = (income_norm + job_time_norm) / 2

    final_score = (
        credit_score_norm * 0.3 +
        income_job_score * 0.5 +
        residence_time_norm * 0.2
    )

    return round(final_score, 2)


# --- Streamlit App ---
st.set_page_config(page_title="Customer Scoring App", layout="centered")

st.title("🏁 Dealership Customer Scoring")

st.markdown("Enter customer details to calculate a score (0–100):")

credit_score = st.number_input("Credit Score", min_value=300, max_value=850, value=680)
income = st.number_input("Annual Income ($)", min_value=15000, max_value=200000, value=55000)
time_at_job = st.number_input("Time at Job (years)", min_value=0.0, max_value=50.0, value=5.0)
time_at_residence = st.number_input("Time at Residence (years)", min_value=0.0, max_value=50.0, value=3.0)

if st.button("Calculate Score"):
    score = score_customer(credit_score, income, time_at_job, time_at_residence)
    
    st.subheader(f"Customer Score: **{score}/100**")

    if score >= 80:
        st.success("High Quality Lead ✅")
    elif score >= 60:
        st.info("Moderate Quality Lead ⚠️")
    else:
        st.warning("Low Quality Lead ❌")
