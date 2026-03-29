import streamlit as st
import datetime
import math

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
            "Enter Password to access the Rounding Calculator",
            type="password",
            on_change=password_entered,
            key="password_input",
        )
        return False
    return True

if not check_password():
    st.stop()
    
def calculate_rounded_hours(start, end):
    # Calculate the difference in minutes
    delta = datetime.datetime.combine(datetime.date.min, end) - \
            datetime.datetime.combine(datetime.date.min, start)
    
    total_seconds = delta.total_seconds()
    
    # Handle cases where end time is before start time (overnight shifts)
    if total_seconds < 0:
        total_seconds += 24 * 3600
        
    total_minutes = total_seconds / 60
    
    # Logic: Always round UP to the nearest 15 minutes (0.25 hours)
    # We divide minutes by 15, ceil it, then multiply by 0.25
    rounded_quarters = math.ceil(total_minutes / 15)
    rounded_hours = rounded_quarters * 0.25
    
    return rounded_hours, total_minutes

# --- Streamlit UI ---
st.set_page_config(page_title="Work Hours Calculator", page_icon="⏰")

st.title("Time Rounding Calculator")
st.write("Enter your shift times below. This tool **always rounds up** to the nearest 15 minutes.")

col1, col2 = st.columns(2)

with col1:
    start_time = st.time_input("Start Time", datetime.time(9, 0))

with col2:
    end_time = st.time_input("End Time", datetime.time(11, 8)) # Default to your 2:08 example logic

if st.button("Calculate Total Hours"):
    rounded_total, raw_minutes = calculate_rounded_hours(start_time, end_time)
    
    # Calculations for the breakdown display
    raw_hours = raw_minutes / 60
    
    st.divider()
    
    # Metrics display
    m1, m2 = st.columns(2)
    m1.metric("Actual Time Worked", f"{int(raw_minutes // 60)}h {int(raw_minutes % 60)}m")
    m2.metric("Billable Hours (Rounded)", f"{rounded_total:.2f}")

    # Visual Table for Clarity
    st.info(f"Rounding Logic Applied: {raw_hours:.4f} hours rounded up to **{rounded_total:.2f}**")

# --- Quick Reference Chart ---
with st.expander("View Rounding Reference"):
    st.markdown("""
    | Minutes Worked | Added Value | Decimal |
    | :--- | :--- | :--- |
    | 1 – 15 | + 0.25 | .25 |
    | 16 – 30 | + 0.50 | .50 |
    | 31 – 45 | + 0.75 | .75 |
    | 46 – 60 | + 1.00 | 1.0 |
    """)
