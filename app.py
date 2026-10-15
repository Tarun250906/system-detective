
import platform
import subprocess
import time

import psutil
import streamlit as st

st.set_page_config(
    page_title="System Detective",
    page_icon="🕵️",
    layout="wide",
)
if "cpu_initialized" not in st.session_state:
    psutil.cpu_percent(interval=None)
    st.session_state.cpu_initialized = True

st.title("🕵️ System Detective")
st.caption("Live system monitoring · Ubuntu on WSL2")

if st.button("🔄 Refresh Now", type="primary"):
    st.rerun()

st.caption(f"Last updated: {time.strftime('%H:%M:%S')}")

cpu_usage = psutil.cpu_percent(interval=0.5)
memory = psutil.virtual_memory()
disk = psutil.disk_usage("/")
cpu_count = psutil.cpu_count() or 1

c1, c2, c3, c4 = st.columns(4)

c1.metric("CPU Usage", f"{cpu_usage:.1f}%")
c2.metric("Memory Usage", f"{memory.percent:.1f}%")
c3.metric("Available Memory", f"{memory.available / (1024**3):.2f} GiB")
c4.metric("Disk Usage", f"{disk.percent:.1f}%")

st.divider()

st.subheader("💻 System Information")

left, right = st.columns(2)

with left:
    st.write("**Operating System:**", platform.system())
    st.write("**Kernel:**", platform.release())
    st.write("**Architecture:**", platform.machine())
    st.write("**Python Version:**", platform.python_version())

with right:
    st.write("**Logical CPUs:**", cpu_count)
    st.write("**Total Memory:**", f"{memory.total / (1024**3):.2f} GiB")
    st.write("**Disk Capacity:**", f"{disk.total / (1024**3):.2f} GiB")

    try:
        result = subprocess.run(
            ["bash", "-lc",
             "grep -qi microsoft /proc/version && echo WSL2 || echo Linux"],
            capture_output=True,
            text=True,
            timeout=2,
        )
        st.write("**Environment:**", result.stdout.strip())
    except Exception:
        st.write("**Environment:** Linux")

st.divider()

# Memory details
st.subheader("🧠 Memory Details")

m1, m2, m3 = st.columns(3)
m1.metric("Used", f"{memory.used / (1024**2):.0f} MiB")
m2.metric("Free", f"{memory.free / (1024**2):.0f} MiB")
m3.metric("Available", f"{memory.available / (1024**2):.0f} MiB")

st.progress(memory.percent / 100, text=f"{memory.percent:.1f}% memory used")

st.divider()

# Disk details
st.subheader("💾 Disk Details")

d1, d2, d3 = st.columns(3)
d1.metric("Used", f"{disk.used / (1024**3):.2f} GiB")
d2.metric("Free", f"{disk.free / (1024**3):.2f} GiB")
d3.metric("Total", f"{disk.total / (1024**3):.2f} GiB")

st.divider()

# Process list
st.subheader("⚙️ Running Processes")

processes = []

for proc in psutil.process_iter(
    ["pid", "name", "status", "cpu_percent", "memory_percent"]
):
    try:
        processes.append(proc.info)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        continue

processes.sort(
    key=lambda p: p.get("cpu_percent") or 0,
    reverse=True,
)

st.dataframe(
    [
        {
            "PID": p["pid"],
            "Process": p["name"],
            "Status": p["status"],
            "CPU %": round(p.get("cpu_percent") or 0, 1),
            "Memory %": round(p.get("memory_percent") or 0, 2),
        }
        for p in processes[:15]
    ],
    use_container_width=True,
    hide_index=True,
)

st.caption(
    "Metrics represent the Linux environment visible to WSL2. "
    "Click Refresh Now to take a new measurement."
)

