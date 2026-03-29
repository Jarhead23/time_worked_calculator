import streamlit as st
import datetime
import math

def get_billable_hours(start, end):
    # Convert times to datetime objects to find the difference
    today = datetime.date.today()
    start_dt = datetime.datetime.combine(today, start)
    end_dt = datetime.datetime.combine(today, end)
    
    # Handle overnight shifts (e.g., 10 PM to 2 AM)
    if end_dt < start_dt:
        end_dt += datetime.timedelta(days=1)
        
    diff = end_dt - start_dt
    total_minutes = diff.total_seconds() / 60
    
    # CORE LOGIC: Always round UP to the nearest 15-minute block
    # 1. Divide total minutes by 15 to get number of quarters
    # 2. Use math.ceil to force any fraction (like 1.1) up to the next integer (2)
    # 3. Multiply by 0.25 to get the decimal hour
    quarters = math.ceil(total_minutes / 15)
    billable_hours = quarters * 0.25
    
    return billable_hours, total_minutes

# --- Streamlit UI ---
st.set_page_config(page_title="Billing Calculator", layout="centered")

st.title("⚖️ Billable Hours Calculator")
st.markdown("Enter your times below to calculate total hours rounded **UP** to the nearest 15 minutes.")

# Input Section
with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        start_time = st.time_input("Start Time", value=datetime.time(2, 0))
    with col2:
        end_time = st.time_input("End Time", value=datetime.time(2, 8))

# Calculation Logic
billable_total, raw_mins = get_billable_hours(start_time, end_time)

# Results Display
st.subheader("Results")
st.metric(label="Total Billable Hours", value=f"{billable_total:.2f} hrs")

# Breakdown for transparency
with st.expander("See Calculation Breakdown"):
    st.write(f"**Actual Time:** {int(raw_mins // 60)}h {int(raw_mins % 60)}m ({raw_mins} total minutes)")
    st.write(f"**Rounding Rule:** Every 1-15 minute block is counted as 0.25.")
    
    # Validation against your examples
    st.info(f"Example Check: Your entry of {start_time.strftime('%I:%M')} to {end_time.strftime('%I:%M')} "
            f"results in **{billable_total:.2f}** billable hours.")
