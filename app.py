import streamlit as st
import psutil
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
import time

# =====================================================
# AUTO REFRESH
# =====================================================
st_autorefresh(interval=5000, key="refresh")

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Workstation Digital Twin",
    page_icon="🖥️",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================
st.markdown("""
<style>

.stApp{
    background-color:#f5f7fb;
}

.block-container{
    padding-top:1rem;
    padding-left:1rem;
    padding-right:1rem;
}

div[data-testid="stMetric"]{
    background:white;
    border-radius:12px;
    padding:10px;
    border:1px solid #e5e7eb;
}

.sidebar-card{
    background:white;
    padding:15px;
    border-radius:12px;
    border:1px solid #e5e7eb;
    margin-top:20px;
}

.small-text{
    font-size:13px;
    color:#6b7280;
}

.main-card{
    background:white;
    border-radius:14px;
    padding:10px;
    border:1px solid #e5e7eb;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# LIVE DATA
# =====================================================
cpu_usage = psutil.cpu_percent(interval=1)

memory = psutil.virtual_memory()
memory_usage = memory.percent

disk = psutil.disk_usage('/')
disk_usage = disk.percent

net = psutil.net_io_counters()

download_mb = round(
    net.bytes_recv / (1024*1024),
    2
)

# =====================================================
# HISTORY
# =====================================================
if "cpu_history" not in st.session_state:
    st.session_state.cpu_history = []

if "memory_history" not in st.session_state:
    st.session_state.memory_history = []

current_time = datetime.now().strftime("%H:%M:%S")

st.session_state.cpu_history.append({
    "Time": current_time,
    "CPU": cpu_usage
})

st.session_state.memory_history.append({
    "Time": current_time,
    "Memory": memory_usage
})

st.session_state.cpu_history = st.session_state.cpu_history[-30:]
st.session_state.memory_history = st.session_state.memory_history[-30:]

cpu_df = pd.DataFrame(st.session_state.cpu_history)
mem_df = pd.DataFrame(st.session_state.memory_history)

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:

    st.markdown("## 🖥️ Digital Twin")

    st.markdown("---")

    page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Metrics",
        "History",
        "Settings"
    ]
)
    

    st.markdown("<br>", unsafe_allow_html=True)

    total_ram = round(
        memory.total/(1024**3),
        1
    )

    uptime_hours = int(
        (time.time()-psutil.boot_time())/3600
    )

    st.markdown("""
    <div class='sidebar-card'>
    <h4>System Info</h4>
    </div>
    """, unsafe_allow_html=True)

    st.write("OS: Windows")
    st.write(f"RAM: {total_ram} GB")
    st.write(f"Threads: {psutil.cpu_count(logical=True)}")
    st.write(f"Uptime: {uptime_hours} hrs")

   # =====================================================
# PAGE SELECTION
# =====================================================

if page == "Metrics":
    st.title("📈 Metrics")
    st.write("Detailed Metrics Page")
    st.stop()

elif page == "History":
    st.title("🕒 History")
    st.write("History Page")
    st.stop()

elif page == "Settings":
    st.title("⚙️ Settings")
    st.write("Settings Page")
    st.stop()
   
# =====================================================
# HEADER
# =====================================================
header_left, header_right = st.columns([4,1])

with header_left:

    st.markdown(
        "## Workstation Digital Twin"
    )

    st.caption(
        "Real-time monitoring of CPU and Memory Utilization"
    )

with header_right:

    st.caption(
        f"Last Updated: {current_time}"
    )

    st.success("🟢 Live")

# =====================================================
# TOP ROW
# =====================================================
c1,c2,c3 = st.columns([2,2,1])

# CPU GAUGE
with c1:

    fig_cpu = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=cpu_usage,
            title={"text":"CPU Usage"},
            gauge={
                "axis":{"range":[0,100]},
                "bar":{"color":"#2563eb"},
                "bgcolor":"white"
            }
        )
    )

    fig_cpu.update_layout(
        height=250,
        template="plotly_white",
        margin=dict(l=10,r=10,t=40,b=10)
    )

    st.plotly_chart(
        fig_cpu,
        use_container_width=True
    )

# MEMORY GAUGE
with c2:

    fig_mem = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=memory_usage,
            title={"text":"Memory Usage"},
            gauge={
                "axis":{"range":[0,100]},
                "bar":{"color":"#22c55e"}
            }
        )
    )

    fig_mem.update_layout(
        height=250,
        template="plotly_white",
        margin=dict(l=10,r=10,t=40,b=10)
    )

    st.plotly_chart(
        fig_mem,
        use_container_width=True
    )

# STATUS CARD
with c3:

    st.markdown("### System Status")

    if cpu_usage < 70 and memory_usage < 80:

        st.success("✔ Healthy")
        st.write("All systems normal")

    elif cpu_usage < 90 and memory_usage < 90:

        st.warning("⚠ Moderate")

    else:

        st.error("✖ Critical")

# =====================================================
# CHART ROW
# =====================================================
g1,g2 = st.columns(2)

with g1:

    cpu_fig = px.line(
        cpu_df,
        x="Time",
        y="CPU"
    )

    cpu_fig.update_traces(
        line_color="#2563eb"
    )

    cpu_fig.update_layout(
        title="CPU Usage Over Time",
        height=300,
        template="plotly_white"
    )

    st.plotly_chart(
        cpu_fig,
        use_container_width=True
    )

with g2:

    mem_fig = px.line(
        mem_df,
        x="Time",
        y="Memory"
    )

    mem_fig.update_traces(
        line_color="#22c55e"
    )

    mem_fig.update_layout(
        title="Memory Usage Over Time",
        height=300,
        template="plotly_white"
    )

    st.plotly_chart(
        mem_fig,
        use_container_width=True
    )

# =====================================================
# CURRENT METRICS
# =====================================================
st.markdown("### Current Metrics")

m1,m2,m3,m4 = st.columns(4)

with m1:
    st.metric(
        "CPU Usage",
        f"{cpu_usage}%"
    )

with m2:
    st.metric(
        "Memory Usage",
        f"{memory_usage}%"
    )

with m3:
    st.metric(
        "Disk Usage (C:)",
        f"{disk_usage}%"
    )

with m4:
    st.metric(
        "Network Download",
        f"{download_mb} MB"
    )