# dashboard.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from simulation.water_env import WaterEnvironment
from simulation.config import GRID_SIZE, START_POS, TARGET_WAYPOINTS, LANDUSE_BY_COUNTRY
from simulation.legal_limits import LEGAL_LIMITS
from src.perception import Perception
from src.detector import ZoneDetector
from src.path_planner import AStarPlanner
from src.navigation import RobotNavigator

# ------------------------------
# Helper functions
# ------------------------------
def plot_landuse_map(landuse_dict, obstacles):
    fig, ax = plt.subplots(figsize=(8,6))
    colors = {
        "Farming (crops)": "lightgreen", "Locality (town)": "lightcoral",
        "Fishery (trout)": "lightblue", "Poultry farm": "orange",
        "Data center": "purple", "Protected area": "darkgreen",
        "Intensive farming (rice/sugarcane)": "lightgreen",
        "Dense locality (village)": "lightcoral", "Shrimp farm": "lightblue",
        "Broiler poultry": "orange", "Textile factory": "brown",
        "Chemical plant": "red", "Corporate farming (corn/soy)": "lightgreen",
        "Suburb": "lightcoral", "Catfish farm": "lightblue",
        "CAFO (cattle)": "orange", "Data center cluster": "purple"
    }
    for name, props in landuse_dict.items():
        x1, y1, x2, y2 = props["rect"]
        rect = plt.Rectangle((y1, x1), y2-y1+1, x2-x1+1,
                             facecolor=colors.get(name, "gray"), alpha=0.5, edgecolor="black")
        ax.add_patch(rect)
        if (x2-x1) > 2 and (y2-y1) > 2:
            ax.text((y1+y2)/2, (x1+x2)/2, name, ha='center', va='center', fontsize=7, weight='bold')
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if obstacles[i][j]:
                ax.add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, hatch='///', fill=False, edgecolor='black'))
    ax.set_xlim(-0.5, GRID_SIZE-0.5)
    ax.set_ylim(GRID_SIZE-0.5, -0.5)
    ax.set_title("Land Use Map (hatched = obstacles)")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    return fig

def run_simulation(country, proposal_loc, discharge_params):
    env = WaterEnvironment(country=country)
    
    # Inject proposed industry discharge at the location
    px, py = proposal_loc
    if not env.is_obstacle(px, py):
        for param, val in discharge_params.items():
            if param in env.params:
                env.params[param][px][py] += val
                
    perception = Perception(env)
    detector = ZoneDetector()
    robot = RobotNavigator(env, perception, detector)
    robot.set_position(*START_POS)
    
    planner = AStarPlanner(env)
    waypoints = list(TARGET_WAYPOINTS) + [tuple(proposal_loc)]
    full_path = []
    current = START_POS
    while waypoints:
        nearest = min(waypoints, key=lambda wp: planner.heuristic(current, wp))
        seg = planner.plan(current, nearest)
        if seg:
            if full_path and seg[0] == full_path[-1]:
                seg = seg[1:]
            full_path.extend(seg)
            current = nearest
        waypoints.remove(nearest)
    
    for step in full_path[1:]:
        robot.move(*step)
    
    return env, robot.log_data, full_path

def check_compliance(log_dicts, limits):
    if not log_dicts:
        return pd.DataFrame()
    df = pd.DataFrame(log_dicts)
    results = []
    for param, limit in limits.items():
        if param in df.columns:
            if param == 'dissolved_oxygen_mgL':
                worst = df[param].min()
                passed = worst >= limit
                worst_display = f"{worst:.2f}"
            elif param == 'ph':
                min_ph = df[param].min()
                max_ph = df[param].max()
                worst_display = f"{min_ph:.2f} - {max_ph:.2f}"
                passed = (min_ph >= limits.get('ph_min', 0) and max_ph <= limits.get('ph_max', 14))
            else:
                worst = df[param].max()
                passed = worst <= limit
                worst_display = f"{worst:.3f}" if worst < 1 else f"{worst:.2f}"
            results.append({
                "Parameter": param,
                "Worst measured": worst_display,
                "Limit": limit,
                "Status": "✅ Pass" if passed else "❌ Violation"
            })
    return pd.DataFrame(results)

def plot_heatmap_with_path(env, path, parameter='nitrate_ppm', limit=10):
    data = env.params.get(parameter, np.zeros((GRID_SIZE, GRID_SIZE)))
    fig, ax = plt.subplots(figsize=(8,6))
    
    cmap = 'RdYlGn' if parameter == 'dissolved_oxygen_mgL' else 'RdYlGn_r'
    vmax = max(np.max(data), limit)
    vmin = min(np.min(data), 0)
    
    im = ax.imshow(data, cmap=cmap, origin='upper', vmin=vmin, vmax=vmax)
    plt.colorbar(im, ax=ax, label=parameter)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if env.is_obstacle(i, j):
                ax.add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, hatch='///', fill=False, edgecolor='gray'))
    if path:
        path_x = [p[1] for p in path]
        path_y = [p[0] for p in path]
        ax.plot(path_x, path_y, 'b-', linewidth=2, marker='o', markersize=4, label='Robot path')
    ax.set_title(f'Water Quality Heatmap ({parameter})')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.legend()
    return fig

# ------------------------------
# Main dashboard
# ------------------------------
def main():
    st.set_page_config(page_title="Pre‑Establishment Compliance Dashboard", layout="wide")
    st.title("🌊 AI‑Based Autonomous Navigation for Industrial Pre‑Establishment Compliance")
    st.markdown("Select a country/regulation, view land use map, adjust proposed industry parameters, and run compliance simulation.")
    
    with st.sidebar:
        st.header("🌍 Select Regulation")
        country = st.selectbox("Country / Standard", list(LEGAL_LIMITS.keys()), index=list(LEGAL_LIMITS.keys()).index("India_CPCB"))
        
        st.markdown("---")
        st.subheader("📜 Legal Limits")
        limits = LEGAL_LIMITS.get(country, {})
        if limits:
            limit_df = pd.DataFrame(list(limits.items()), columns=["Parameter", "Limit"])
            st.dataframe(limit_df, use_container_width=True)
        
        st.markdown("---")
        st.subheader("🏭 Proposed Industry")
        industry_name = st.text_input("Industry name", "Green_Factory")
        col1, col2 = st.columns(2)
        with col1:
            loc_x = st.number_input("Location X (0-19)", min_value=0, max_value=19, value=18)
        with col2:
            loc_y = st.number_input("Location Y (0-19)", min_value=0, max_value=19, value=18)
        
        st.markdown("**Discharge Parameters (excess)**")
        nitrate = st.number_input("Nitrate (ppm)", value=0.10, step=0.01, format="%.2f")
        phosphate = st.number_input("Phosphate (µg/L)", value=0.10, step=0.01, format="%.2f")
        temp_rise = st.number_input("Temperature rise (°C)", value=1.0, step=0.5)
        ph_shift = st.number_input("pH shift (negative=acidic)", value=0.0, step=0.1)
        bod = st.number_input("BOD (mg/L)", value=5.0, step=1.0)
        cod = st.number_input("COD (mg/L)", value=20.0, step=5.0)
        turbidity = st.number_input("Turbidity (NTU)", value=2.0, step=1.0)
        do_reduction = st.number_input("DO reduction (mg/L)", value=-0.2, step=0.05)
        lead = st.number_input("Lead (µg/L)", value=0.01, step=0.01, format="%.2f")
        mercury = st.number_input("Mercury (µg/L)", value=0.001, step=0.001, format="%.3f")
        
        st.markdown("---")
        evaluate_local_only = st.checkbox("🔍 Evaluate only proposed location (ignore background)", value=True)
        st.caption("If checked, compliance is based only on the cell where the new industry is placed.")
        
        from simulation.config import BASELINE
        heatmap_param = st.selectbox("🗺️ Select Heatmap Parameter", list(BASELINE.keys()), index=0)
        
        run_button = st.button("🚀 Run Compliance Simulation", type="primary")
    
    # Show land use map
    temp_env = WaterEnvironment(country=country)
    landuse_dict = LANDUSE_BY_COUNTRY.get(country, {})
    st.subheader("🗺️ Current Land Use Map (based on selected country)")
    fig_map = plot_landuse_map(landuse_dict, temp_env.obstacles)
    st.pyplot(fig_map)
    
    if run_button:
        with st.spinner("Running autonomous navigation simulation..."):
            discharge = {
                'nitrate_ppm': nitrate,
                'phosphate_ugL': phosphate,
                'temperature_c': temp_rise,
                'ph': ph_shift,
                'bod_mgL': bod,
                'cod_mgL': cod,
                'turbidity_ntu': turbidity,
                'dissolved_oxygen_mgL': do_reduction,
                'lead_ugL': lead,
                'mercury_ugL': mercury,
            }
            env, log_data, path = run_simulation(country, (loc_x, loc_y), discharge)
            
            col_left, col_right = st.columns([2,1])
            with col_left:
                st.subheader("🗺️ Water Quality Heatmap & Robot Path")
                limit_val = limits.get(heatmap_param, np.max(env.params.get(heatmap_param, [10])))
                fig_heat = plot_heatmap_with_path(env, path, parameter=heatmap_param, limit=limit_val)
                st.pyplot(fig_heat)
            with col_right:
                st.subheader("📊 Compliance Report")
                if log_data:
                    df_log = pd.DataFrame(log_data)
                    if evaluate_local_only:
                        local_rows = df_log[(df_log['x'] == loc_x) & (df_log['y'] == loc_y)]
                        if len(local_rows) == 0:
                            st.warning(f"Robot did not visit proposed location ({loc_x},{loc_y}). Falling back to full path.")
                            df_analysis = df_log
                        else:
                            df_analysis = local_rows
                            st.info(f"✅ Evaluating compliance **only at proposed location** ({loc_x},{loc_y}).")
                    else:
                        df_analysis = df_log
                        st.info("📊 Evaluating compliance across **all visited cells** (worst‑case).")
                    
                    compliance_df = check_compliance(df_analysis.to_dict('records'), limits)
                    st.dataframe(compliance_df, use_container_width=True)
                    
                    violations = compliance_df[compliance_df["Status"] == "❌ Violation"]
                    if len(violations) == 0:
                        st.success(f"✅ **RECOMMENDATION:** The proposed {industry_name} at ({loc_x},{loc_y}) **CAN be established** under {country} regulation.")
                    else:
                        st.error(f"⚠️ **RECOMMENDATION:** The proposed {industry_name} **SHOULD NOT be established** without additional treatment. Violations: {', '.join(violations['Parameter'].values)}")
                else:
                    st.warning("No data collected.")
        st.success("Simulation complete.")

if __name__ == "__main__":
    main()
