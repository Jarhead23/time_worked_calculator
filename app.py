import streamlit as st
import datetime
import math

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GGC Billable Hours",
    page_icon="🚛",
    layout="wide",
)
# ── 1. INITIALIZE SESSION STATE ───────────────────────────────────────────────
# Ensures the key exists the moment the app starts, preventing KeyError
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# ── 2. LOGIN FUNCTION ─────────────────────────────────────────────────────────
def check_password():
    """Returns True if the user entered the correct password."""
    def password_entered():
        if st.session_state["password_input"] == st.secrets["MY_APP_PASSWORD"]:
            st.session_state["authenticated"] = True
            del st.session_state["password_input"]  # remove password from state for security
        else:
            st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.markdown("<div style='margin-top: 6rem;'></div>", unsafe_allow_html=True)
        st.text_input(
            "Enter Password to access the GGC Billable Hours Calculator",
            type="password",
            on_change=password_entered,
            key="password_input",
        )
        return False
    return True

if not check_password():
    st.stop()
    
def calculate_hours(start_str, end_str):
    try:
        # Define the format we expect (HH:MM in 24-hour or 12-hour format)
        # We try 24-hour format first for simplicity
        fmt = '%H:%M'
        start_time = datetime.datetime.strptime(start_str.strip(), fmt)
        end_time = datetime.datetime.strptime(end_str.strip(), fmt)
        
        # Handle overnight shifts
        if end_time <= start_time:
            end_time += datetime.timedelta(days=1)
            
        duration = end_time - start_time
        total_minutes = duration.total_seconds() / 60
        
        # ALWAYS ROUND UP LOGIC
        # 1-15 min = 0.25, 16-30 = 0.50, etc.
        billable_units = math.ceil(total_minutes / 15)
        billable_hours = billable_units * 0.25
        
        return billable_hours, total_minutes, None
    except ValueError:
        return None, None, "Please enter time in HH:MM format (e.g., 02:08 or 14:15)"

# --- Streamlit UI ---
st.set_page_config(page_title="Manual Time Entry", layout="centered")

st.title("⏱️ HUNKS Billable Hours ")
st.write("Type your start and end times below in **HH:MM** format.")

# Manual Text Inputs
col1, col2 = st.columns(2)
with col1:
    start_input = st.text_input("Start Time (HH:MM)", value="02:00")
with col2:
    end_input = st.text_input("End Time (HH:MM)", value="02:08")

if start_input and end_input:
    billable_total, raw_mins, error = calculate_hours(start_input, end_input)
    
    if error:
        st.error(error)
    else:
        st.divider()
        st.header(f"Total Billable: {billable_total:.2f} Hours")
        
        # Breakdown
        st.write(f"**Calculated from:** {start_input} to {end_input}")
        st.write(f"**Total Minutes:** {int(raw_mins)}")
        
        # Logic display to match your chart
        st.info(f"Logic: {int(raw_mins)} minutes is {math.ceil(raw_mins/15)} 15-minute blocks.")

# Quick Reference
with st.expander("Rounding Reference Chart"):
    st.markdown("""
    | Minutes | Result |
    | :--- | :--- |
    | 1 – 15 | +0.25 |
    | 16 – 30 | +0.50 |
    | 31 – 45 | +0.75 |
    | 46 – 60 | +1.00 |
    """)
