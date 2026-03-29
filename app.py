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
        fmt = '%H:%M'
        start_time = datetime.datetime.strptime(start_str.strip(), fmt)
        end_time = datetime.datetime.strptime(end_str.strip(), fmt)
        
        if end_time <= start_time:
            end_time += datetime.timedelta(days=1)
            
        duration = end_time - start_time
        total_minutes = duration.total_seconds() / 60
        
        # logic: 1-15 = .25, 16-30 = .50, etc.
        billable_units = math.ceil(total_minutes / 15)
        billable_hours = billable_units * 0.25
        
        return billable_hours, total_minutes, None
    except ValueError:
        return None, None, "Use HH:MM format (e.g. 02:08)"

# --- UI Setup ---
st.set_page_config(page_title="GGC Time Tracker (TT)", layout="centered")

st.title("⏱️ Billable Hours Calculator")
st.write("Enter times manually. Use 24-hour format (e.g., 14:30 for 2:30 PM).")

# Create a fixed container for inputs so they don't move
input_container = st.container(border=True)
with input_container:
    col1, col2 = st.columns(2)
    start_input = col1.text_input("Start Time", value="02:00")
    end_input = col2.text_input("End Time", value="02:08")
    submit = st.button("Calculate Billable Time", use_container_width=True)

# Create a reserved space for the result so the page height stays consistent
result_area = st.container()

with result_area:
    if submit:
        billable_total, raw_mins, error = calculate_hours(start_input, end_input)
        
        if error:
            st.error(error)
        else:
            # Using columns inside the result area to keep it neat
            st.divider()
            res_col1, res_col2 = st.columns(2)
            res_col1.metric("Billable Hours", f"{billable_total:.2f}")
            res_col2.metric("Actual Minutes", f"{int(raw_mins)}m")
            
            # This info box confirms the rounding logic
            st.info(f"Rounding Up: {int(raw_mins)} minutes = {math.ceil(raw_mins/15)} quarter-hour blocks.")
    else:
        # Placeholder text so the screen doesn't look empty before hitting enter
        st.info("Enter times above and click calculate.")
