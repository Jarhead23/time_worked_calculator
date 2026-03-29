import streamlit as st
import datetime
import math

def calculate_billable_hours(start, end):
    # Convert times to a datetime object for calculation
    # Using a dummy date (today) to handle time arithmetic
    today = datetime.date.today()
    start_dt = datetime.datetime.combine(today, start)
    end_dt = datetime.datetime.combine(today, end)
    
    # Logic for overnight shifts (e.g., 11:00 PM to 1:00 AM)
    if end_dt <= start_dt:
        end_dt += datetime.timedelta(days=1)
        
    # Calculate the total difference in minutes
    duration = end_dt - start_dt
    total_minutes = duration.total_seconds() / 60
    
    # --- CORE ROUNDING LOGIC ---
    # Divide minutes by 15. If there is ANY remainder (e.g., 16/15 = 1.06), 
    # math.ceil() pushes it to the next whole number (2).
    fifteen_min_blocks = math.ceil(total_minutes / 15)
    billable_hours = fifteen_min_blocks * 0.25
    
    return billable_hours, total_minutes

# --- STREAMLIT UI ---
st.set_page_config(page_title="Billable Hours Tracker", layout="centered")

st.title("⏱️ Billable Hours Calculator")
st.write("Enter any start and end time. The system **always rounds up** to the nearest 15 minutes.")

# User Inputs
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        user_start = st.time_input("Enter Start Time", value=datetime.time(9, 0))
    with col2:
        user_end = st.time_input("Enter End Time", value=datetime.time(11, 8))

# Perform Calculation
billable_total, raw_mins = calculate_billable_hours(user_start, user_end)

# Display Results
st.divider()
st.header(f"Total Billable: {billable_total:.2f} Hours")

# Verification Table
st.subheader("Calculation Details")
data = {
    "Actual Minutes Worked": f"{int(raw_mins)} mins",
    "15-Minute Blocks (Rounded Up)": math.ceil(raw_mins / 15),
    "Final Decimal Value": f"{billable_total:.2f}"
}
st.table(data)

# Quick Reference for Logic
with st.expander("Show Rounding Chart"):
    st.markdown("""
    | Minutes Over | Billable Increase |
    | :--- | :--- |
    | 1–15 mins | +0.25 |
    | 16–30 mins | +0.50 |
    | 31–45 mins | +0.75 |
    | 46–60 mins | +1.00 |
    """)
