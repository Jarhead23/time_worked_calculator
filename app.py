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
        billable_units = math.ceil(total_minutes / 15)
        return billable_units * 0.25, total_minutes, None
    except ValueError:
        return None, None, "Use HH:MM format"

st.set_page_config(page_title="Stable Calculator", layout="centered")

st.title("⏱️ Billable Hours Calculator")
st.write("Enter times manually (e.g., 01:00 to 09:22).")

# 1. FIXED INPUT SECTION
with st.container(border=True):
    col1, col2 = st.columns(2)
    start_input = col1.text_input("Start Time", value="01:00")
    end_input = col2.text_input("End Time", value="09:22")
    submit = st.button("Calculate Billable Time", use_container_width=True)

st.divider()

# 2. RESERVED SPACE (This stops the jumping)
# We create the columns and placeholders FIRST
res_col1, res_col2 = st.columns(2)
billable_placeholder = res_col1.empty()
minutes_placeholder = res_col2.empty()
info_placeholder = st.empty()

# 3. FILL THE RESERVED SPACE
if submit:
    billable_total, raw_mins, error = calculate_hours(start_input, end_input)
    if error:
        st.error(error)
    else:
        # Instead of creating new elements, we "write" to the placeholders
        billable_placeholder.metric("Billable Hours", f"{billable_total:.2f}")
        minutes_placeholder.metric("Actual Minutes", f"{int(raw_mins)}m")
        info_placeholder.info(f"Rounding Up: {int(raw_mins)} minutes = {math.ceil(raw_mins/15)} quarter-hour blocks.")
else:
    # Optional: Put a dash or 0.00 so the user sees where the numbers will go
    billable_placeholder.metric("Billable Hours", "0.00")
    minutes_placeholder.metric("Actual Minutes", "0m")
