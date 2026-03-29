import streamlit as st
import datetime
import math

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GGC Billable Hours",
    page_icon="🚛",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Mono', monospace;
}

h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
}

/* Dark industrial background */
.stApp {
    background-color: #0f0f0f;
    color: #e8e8e8;
}

/* Metric cards */
[data-testid="metric-container"] {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    transition: border-color 0.3s ease;
}
[data-testid="metric-container"]:hover {
    border-color: #f5c242;
}
[data-testid="metric-container"] label {
    color: #888 !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 2.4rem !important;
    font-weight: 800 !important;
    color: #f5c242 !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    color: #aaa !important;
    font-size: 0.8rem !important;
}

/* Input boxes */
input[type="text"], input[type="password"] {
    background: #1a1a1a !important;
    border: 1px solid #333 !important;
    border-radius: 8px !important;
    color: #e8e8e8 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 1.1rem !important;
    transition: border-color 0.2s ease !important;
}
input[type="text"]:focus, input[type="password"]:focus {
    border-color: #f5c242 !important;
    box-shadow: 0 0 0 2px rgba(245,194,66,0.15) !important;
}

/* Primary button */
.stButton > button[kind="primary"] {
    background: #f5c242 !important;
    color: #0f0f0f !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 8px !important;
    height: 3rem !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.05em;
}
.stButton > button[kind="primary"]:hover {
    background: #ffd966 !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(245,194,66,0.3) !important;
}

/* Secondary button */
.stButton > button[kind="secondary"] {
    background: #1a1a1a !important;
    color: #e8e8e8 !important;
    font-family: 'DM Mono', monospace !important;
    border: 1px solid #333 !important;
    border-radius: 8px !important;
    height: 3rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: #f5c242 !important;
    color: #f5c242 !important;
}

/* Container / card */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #141414 !important;
    border: 1px solid #222 !important;
    border-radius: 16px !important;
    padding: 0.5rem !important;
}

/* Divider */
hr {
    border-color: #222 !important;
}

/* Info / success / error boxes */
[data-testid="stAlert"] {
    background: #1a1a1a !important;
    border-radius: 10px !important;
    border-left: 3px solid #f5c242 !important;
    color: #e8e8e8 !important;
}

/* Table */
[data-testid="stDataFrame"] {
    background: #141414 !important;
    border-radius: 12px !important;
    overflow: hidden;
}
thead tr th {
    background: #1f1f1f !important;
    color: #f5c242 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
tbody tr:hover td {
    background: #1f1f1f !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #111 !important;
    border-right: 1px solid #222 !important;
}

/* Number input */
input[type="number"] {
    background: #1a1a1a !important;
    border: 1px solid #333 !important;
    color: #e8e8e8 !important;
    border-radius: 8px !important;
}

/* Select box */
[data-baseweb="select"] > div {
    background: #1a1a1a !important;
    border-color: #333 !important;
    border-radius: 8px !important;
    color: #e8e8e8 !important;
}

/* Labels */
label[data-testid="stWidgetLabel"] p {
    color: #888 !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* Progress bar */
[data-testid="stProgress"] > div > div {
    background: #f5c242 !important;
}

/* Accent tag */
.tag {
    display: inline-block;
    background: rgba(245,194,66,0.12);
    color: #f5c242;
    border: 1px solid rgba(245,194,66,0.3);
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 0.72rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.big-result {
    font-family: 'Syne', sans-serif;
    font-size: 3.5rem;
    font-weight: 800;
    color: #f5c242;
    line-height: 1;
}

.sub-label {
    font-size: 0.7rem;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 4px;
}

.breakdown-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #1e1e1e;
    font-size: 0.85rem;
}
.breakdown-row:last-child { border-bottom: none; }
.breakdown-label { color: #666; }
.breakdown-value { color: #e8e8e8; font-weight: 500; }

.bar-bg {
    background: #1e1e1e;
    border-radius: 4px;
    height: 6px;
    margin-top: 8px;
}
.bar-fill {
    background: #f5c242;
    border-radius: 4px;
    height: 6px;
    transition: width 0.6s ease;
}
</style>
""", unsafe_allow_html=True)


# ── 1. SESSION STATE ──────────────────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "history" not in st.session_state:
    st.session_state["history"] = []

# ── 2. LOGIN ──────────────────────────────────────────────────────────────────

def check_password():
    def password_entered():
        if st.session_state["password_input"] == st.secrets["MY_APP_PASSWORD"]:
            st.session_state["authenticated"] = True
            del st.session_state["password_input"]
        else:
            st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.markdown("<div style='margin-top: 6rem;'></div>", unsafe_allow_html=True)
        col = st.columns([1, 2, 1])[1]
        with col:
            st.markdown("<p class='tag'>🚛 GGC Internal</p>", unsafe_allow_html=True)
            st.markdown("### Billable Hours Calculator")
            st.text_input(
                "Access Code",
                type="password",
                on_change=password_entered,
                key="password_input",
            )
        return False
    return True

if not check_password():
    st.stop()
    
# ── 3. CORE LOGIC ─────────────────────────────────────────────────────────────
def calculate_hours(start_str, end_str):
    try:
        fmt = '%H:%M'
        start_time = datetime.datetime.strptime(start_str.strip(), fmt)
        end_time   = datetime.datetime.strptime(end_str.strip(), fmt)
        if end_time <= start_time:
            end_time += datetime.timedelta(days=1)
        duration       = end_time - start_time
        total_minutes  = duration.total_seconds() / 60
        billable_units = math.ceil(total_minutes / 15)
        return billable_units * 0.25, total_minutes, None
    except ValueError:
        return None, None, "Use HH:MM format (e.g. 09:00)"

# ── 4. SIDEBAR — HISTORY ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📋 Session History")
    if st.session_state["history"]:
        total_billable = sum(e["billable"] for e in st.session_state["history"])
        total_raw      = sum(e["minutes"] for e in st.session_state["history"])
        st.markdown(f"""
        <div style='background:#1a1a1a;border:1px solid #2a2a2a;border-radius:10px;padding:14px;margin-bottom:16px;'>
            <div class='sub-label'>Session Total</div>
            <div style='font-family:Syne,sans-serif;font-size:2rem;font-weight:800;color:#f5c242;'>{total_billable:.2f}h</div>
            <div class='sub-label'>{int(total_raw)} raw minutes across {len(st.session_state["history"])} entries</div>
        </div>
        """, unsafe_allow_html=True)

        for i, entry in enumerate(reversed(st.session_state["history"])):
            rounding_loss = entry["billable"] * 60 - entry["minutes"]
            st.markdown(f"""
            <div class='breakdown-row'>
                <span class='breakdown-label'>{entry['start']} → {entry['end']}</span>
                <span class='breakdown-value'>{entry['billable']:.2f}h</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state["history"] = []
            st.rerun()
    else:
        st.markdown("<p style='color:#444;font-size:0.85rem;'>No entries yet. Calculate a shift to start tracking.</p>", unsafe_allow_html=True)

# ── 5. MAIN UI ────────────────────────────────────────────────────────────────
st.markdown("<p class='tag'>🚛 GGC Time Tracker</p>", unsafe_allow_html=True)
st.markdown("# ⏱️ Billable Hours")
st.markdown("<p style='color:#555;font-size:0.9rem;margin-top:-10px;'>15-minute block rounding · overnight shift support</p>", unsafe_allow_html=True)

st.divider()

# Input section
with st.container(border=True):
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        start_input = st.text_input("▶ Start Time", value="01:00", placeholder="HH:MM")
    with col2:
        end_input = st.text_input("⏹ End Time", value="09:22", placeholder="HH:MM")
    with col3:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        submit = st.button("Calculate →", type="primary", use_container_width=True)

    # Live preview while typing (no button needed)
    live_billable, live_mins, live_err = calculate_hours(start_input, end_input)
    if live_billable is not None and not submit:
        overnight = "🌙 Overnight shift detected" if live_mins > (
            (datetime.datetime.strptime(end_input.strip(), '%H:%M') -
             datetime.datetime.strptime(start_input.strip(), '%H:%M')).total_seconds() / 60
            if end_input > start_input else -1
        ) else ""
        st.markdown(f"""
        <div style='margin-top:8px;padding:10px 14px;background:#111;border-radius:8px;border:1px solid #1e1e1e;display:flex;gap:32px;align-items:center;'>
            <div>
                <div class='sub-label'>Live Preview</div>
                <span style='font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;color:#f5c242;'>{live_billable:.2f}h</span>
            </div>
            <div>
                <div class='sub-label'>Raw Minutes</div>
                <span style='color:#aaa;font-size:1rem;'>{int(live_mins)}m</span>
            </div>
            <div>
                <div class='sub-label'>Blocks (×15 min)</div>
                <span style='color:#aaa;font-size:1rem;'>{math.ceil(live_mins/15)}</span>
            </div>
            {"<div style='color:#f5c242;font-size:0.8rem;'>"+overnight+"</div>" if overnight else ""}
        </div>
        """, unsafe_allow_html=True)

st.divider()

# Results section
res_col1, res_col2 = st.columns(2)
billable_ph = res_col1.empty()
minutes_ph  = res_col2.empty()
info_ph     = st.empty()

if submit:
    billable_total, raw_mins, error = calculate_hours(start_input, end_input)
    if error:
        st.error(f"⚠️ {error}")
    else:
        # Check overnight
        is_overnight = raw_mins > 720  # more than 12h suggests overnight

        billable_ph.metric(
            "Billable Hours",
            f"{billable_total:.2f}",
            delta=f"{'🌙 Overnight' if is_overnight else '☀️ Same day'}",
        )
        minutes_ph.metric(
            "Actual Minutes",
            f"{int(raw_mins)}m",
            delta=f"+{int(billable_total*60 - raw_mins)}m rounded up",
        )

        blocks      = math.ceil(raw_mins / 15)
        pct_used    = (raw_mins / (blocks * 15)) * 100
        bar_width   = int(pct_used)

        info_ph.markdown(f"""
        <div style='background:#141414;border:1px solid #222;border-radius:14px;padding:20px 24px;margin-top:8px;'>
            <div style='margin-bottom:16px;'>
                <div class='sub-label' style='margin-bottom:6px;'>Billing breakdown</div>
                <div class='breakdown-row'>
                    <span class='breakdown-label'>Raw duration</span>
                    <span class='breakdown-value'>{int(raw_mins)} min</span>
                </div>
                <div class='breakdown-row'>
                    <span class='breakdown-label'>15-min blocks used</span>
                    <span class='breakdown-value'>{blocks} × 0.25h</span>
                </div>
                <div class='breakdown-row'>
                    <span class='breakdown-label'>Billed duration</span>
                    <span class='breakdown-value'>{blocks * 15} min</span>
                </div>
                <div class='breakdown-row'>
                    <span class='breakdown-label'>Rounding buffer</span>
                    <span class='breakdown-value'>+{int(blocks*15 - raw_mins)} min</span>
                </div>
                <div class='breakdown-row'>
                    <span class='breakdown-label'>Block utilization</span>
                    <span class='breakdown-value'>{pct_used:.1f}%</span>
                </div>
            </div>
            <div class='bar-bg'>
                <div class='bar-fill' style='width:{bar_width}%;'></div>
            </div>
            <div style='color:#444;font-size:0.7rem;margin-top:6px;'>{bar_width}% of last block used</div>
        </div>
        """, unsafe_allow_html=True)

        # Save to history
        st.session_state["history"].append({
            "start":   start_input,
            "end":     end_input,
            "billable": billable_total,
            "minutes":  raw_mins,
        })
else:
    billable_ph.metric("Billable Hours", "—")
    minutes_ph.metric("Actual Minutes", "—")

