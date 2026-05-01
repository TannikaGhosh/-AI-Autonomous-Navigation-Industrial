import subprocess
import time

params = ['nitrate_ppm', 'bod_mgL', 'lead_ugL']

with open('dashboard.py', 'r', encoding='utf-8') as f:
    orig = f.read()

try:
    for param in params:
        new_content = orig.replace(
            'heatmap_param = st.selectbox("🗺️ Select Heatmap Parameter", list(BASELINE.keys()), index=list(BASELINE.keys()).index("India_CPCB"))',
            'heatmap_param = st.selectbox("🗺️ Select Heatmap Parameter", list(BASELINE.keys()), index=0)' # Just a placeholder since the replace below will fix it
        ) # wait, the file currently has index=0.
        
        new_content = orig.replace(
            'heatmap_param = st.selectbox("🗺️ Select Heatmap Parameter", list(BASELINE.keys()), index=0)',
            f'heatmap_param = st.selectbox("🗺️ Select Heatmap Parameter", list(BASELINE.keys()), index=list(BASELINE.keys()).index("{param}"))'
        )
        with open('dashboard.py', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        # Wait a moment for Streamlit to hot-reload
        time.sleep(2)
        
        print(f"Running capture for {param}...")
        subprocess.run(["python", "capture_screenshots.py"], check=True)
        
        print(f"Renaming output to output_{param}.png")
        subprocess.run(["powershell", "-Command", f"Move-Item -Path 'images\\output_sample.png' -Destination 'images\\output_{param}.png' -Force"], check=True)

finally:
    with open('dashboard.py', 'w', encoding='utf-8') as f:
        f.write(orig)
