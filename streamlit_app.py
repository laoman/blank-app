import streamlit as st
import time

# 1. SETUP PAGE
st.set_page_config(page_title="Pro App", layout="wide")

# This simulates a slow global data load (Only happens once due to cache)
@st.cache_data
def get_heavy_data():
    time.sleep(20) # Simulated delay
    return {"status": "Ready"}

data_status = get_heavy_data()
st.title(f"Multi-Tab Dashboard ({data_status['status']})")

# 2. DEFINE FRAGMENTED TAB CONTENT
# Wrapping the internal logic in a fragment makes it "snappy"
@st.fragment
def render_tab_content(tab_name, color):
    st.subheader(f"Content for {tab_name}")
    
    # Interaction here ONLY reruns this specific function
    col1, col2 = st.columns(2)
    with col1:
        val = st.slider(f"Adjust {tab_name}", 0, 100, key=f"slider_{tab_name}")
    with col2:
        if st.button(f"Process {tab_name}", key=f"btn_{tab_name}"):
            st.success(f"Calculated: {val * 42}!")
            
    st.info(f"Last updated: {time.strftime('%H:%M:%S')}")

# 3. CREATE TABS
t1, t2, t3, t4, t5, t6 = st.tabs([
    "📈 Overview", "📊 Analytics", "⚙️ Settings", 
    "🧪 Lab", "📂 Files", "👤 Profile"
])

# 4. DISTRIBUTE CONTENT
with t1: render_tab_content("Overview", "blue")
with t2: render_tab_content("Analytics", "green")
with t3: render_tab_content("Settings", "orange")
with t4: render_tab_content("Lab", "purple")
with t5: render_tab_content("Files", "red")
with t6: render_tab_content("Profile", "grey")

# This button is OUTSIDE fragments and will trigger the 2-second cache check
st.divider()
if st.button("Full App Refresh"):
    st.rerun()
