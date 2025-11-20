import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. APP CONFIGURATION ---
st.set_page_config(
    page_title="Advanced AHP Tool by Sayeem",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. STATE MANAGEMENT ---
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark' # Default to dark for "modern" look
if 'factors' not in st.session_state:
    st.session_state.factors = ["Cost", "Feasibility", "Impact"]
if 'matrix' not in st.session_state:
    st.session_state.matrix = np.ones((3, 3))

def toggle_theme():
    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'

# --- 3. ADVANCED STYLING (CSS) ---
# This CSS handles the animations, glassmorphism, and professional typography
st.markdown(f"""
<style>
    /* GLOBAL ANIMATIONS */
    @keyframes fadeIn {{
        0% {{ opacity: 0; transform: translateY(10px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
    }}
    .animate-fade {{
        animation: fadeIn 0.6s ease-out forwards;
    }}

    /* TOP BANNER STYLING */
    .top-banner {{
        padding: 1.5rem;
        border-radius: 0 0 15px 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
    }}
    .top-banner h1 {{
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        margin: 0;
        font-size: 2rem;
        color: white !important;
        letter-spacing: 1px;
    }}

    /* CARD STYLING */
    .st-card {{
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
        border: 1px solid rgba(128, 128, 128, 0.2);
    }}
    .st-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }}

    /* METRIC BOXES */
    .metric-container {{
        display: flex;
        justify-content: space-between;
        gap: 10px;
    }}
    .metric-item {{
        flex: 1;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
    }}

    /* BUTTONS */
    .stButton > button {{
        border-radius: 6px;
        font-weight: 600;
        transition: transform 0.1s;
    }}
    .stButton > button:active {{
        transform: scale(0.98);
    }}
    
    /* SEARCH LINKS */
    .search-link {{
        display: inline-block;
        padding: 10px 20px;
        border-radius: 50px;
        text-decoration: none;
        font-weight: 600;
        margin-top: 10px;
        transition: opacity 0.2s;
    }}
    .search-link:hover {{ opacity: 0.8; }}
</style>
""", unsafe_allow_html=True)

# --- THEME COLORS INJECTION ---
if st.session_state.theme == 'dark':
    st.markdown("""
    <style>
        .stApp { background-color: #0f1116; color: #e0e0e0; }
        .st-card { background-color: #1e212b; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        .stExpander { background-color: #1e212b; border: 1px solid #2d333b; }
        h1, h2, h3, h4 { color: #64ffda !important; }
        .metric-item { background-color: #2d333b; border-left: 4px solid #64ffda; }
        .sidebar .sidebar-content { background-color: #161b22; }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        .stApp { background-color: #f4f7f6; color: #333; }
        .st-card { background-color: #ffffff; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
        .stExpander { background-color: #ffffff; border: 1px solid #e0e0e0; }
        h1, h2, h3, h4 { color: #1e3c72 !important; }
        .metric-item { background-color: #eef2f5; border-left: 4px solid #1e3c72; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. HEADER ---
st.markdown("""
    <div class="top-banner animate-fade">
        <h1>Advanced AHP Tool by Sayeem</h1>
        <p style="margin-top:5px; opacity:0.9;">Professional Multi-Criteria Decision Analysis System</p>
    </div>
""", unsafe_allow_html=True)

# --- 5. SIDEBAR NAVIGATION ---
with st.sidebar:
    # Theme Toggle
    col_l, col_r = st.columns([4,1])
    with col_l:
        st.write(f"Mode: **{st.session_state.theme.title()}**")
    with col_r:
        if st.session_state.theme == 'light':
            st.button("🌙", on_click=toggle_theme, key="theme_toggle", help="Dark Mode")
        else:
            st.button("☀️", on_click=toggle_theme, key="theme_toggle", help="Light Mode")
    
    st.markdown("---")
    
    # Navigation Menu
    nav_options = [
        "🏠 Learn AHP", 
        "🛠️ Custom Analysis", 
        "📂 Geospatial Presets", 
        "📊 Final Results", 
        "❓ Help & Guide"
    ]
    
    selection = st.radio("Navigation", nav_options, label_visibility="collapsed")
    
    st.markdown("---")
    
    # Context-Aware Sidebar Content (Only show factor editing in Analysis mode)
    if selection == "🛠️ Custom Analysis":
        st.subheader("📝 Manage Criteria")
        new_factor = st.text_input("New Factor", placeholder="Type and press Enter")
        if st.button("Add Factor") and new_factor:
            if new_factor not in st.session_state.factors:
                st.session_state.factors.append(new_factor)
                n = len(st.session_state.factors)
                st.session_state.matrix = np.ones((n, n))
                st.rerun()
                
        if len(st.session_state.factors) > 0:
            rem = st.selectbox("Delete Factor", st.session_state.factors)
            if st.button("Remove Selected"):
                st.session_state.factors.remove(rem)
                n = len(st.session_state.factors)
                st.session_state.matrix = np.ones((n, n))
                st.rerun()
        
        st.caption(f"Total Factors: {len(st.session_state.factors)}")

# --- 6. PAGE CONTENT ROUTING ---

# >>> PAGE: LEARN AHP <<<
if selection == "🏠 Learn AHP":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        <div class="st-card animate-fade">
            <h3>👋 Welcome to the Advanced Engine</h3>
            <p>This tool, developed by Sayeem, provides a professional environment for conducting 
            <b>Analytic Hierarchy Process (AHP)</b> studies. It is optimized for geospatial analysis, 
            business decision-making, and academic research.</p>
            <br>
            <h4>How it Works:</h4>
            <ol>
                <li><b>Define:</b> Choose your criteria in the "Custom Analysis" tab or load a Preset.</li>
                <li><b>Compare:</b> Use the slider to judge relative importance.</li>
                <li><b>Research:</b> Use the AI assistant to validate your judgments.</li>
                <li><b>Export:</b> Download your consistent weights for your paper.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="st-card animate-fade" style="text-align:center;">
            <h3>🚀 Quick Actions</h3>
            <p>Jump straight into common tasks</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start New Analysis", use_container_width=True):
            st.session_state.factors = ["A", "B"]
            st.rerun() # In a real app, this would switch tabs, here it resets
        
        st.info("Tip: Use the 'Geospatial Presets' tab for instant setups like Flood Risk or Site Suitability.")

# >>> PAGE: CUSTOM ANALYSIS (THE MAIN TOOL) <<<
elif selection == "🛠️ Custom Analysis":
    factors = st.session_state.factors
    n = len(factors)
    
    st.markdown(f"### 🛠️ Pairwise Comparison Wizard ({n} Factors)")
    
    if n < 2:
        st.warning("⚠️ Please add at least 2 factors in the sidebar to begin analysis.")
    else:
        # 1. AI RESEARCH BAR
        with st.expander("🧠 AI Research Assistant (Open to Validate Factors)"):
            st.markdown("Select two factors to see what experts say about their relative importance.")
            rc1, rc2 = st.columns(2)
            rf1 = rc1.selectbox("Factor 1", factors, index=0, key="rf1")
            rf2 = rc2.selectbox("Factor 2", factors, index=1 if n>1 else 0, key="rf2")
            
            q_google = f"importance of {rf1} vs {rf2} in geospatial analysis"
            q_scholar = f"AHP weight {rf1} {rf2}"
            
            btn_col1, btn_col2 = st.columns(2)
            btn_col1.markdown(f'<a href="https://www.google.com/search?q={q_google}" target="_blank" class="search-link" style="background:#4285F4; color:white;">🔍 Google Search</a>', unsafe_allow_html=True)
            btn_col2.markdown(f'<a href="https://scholar.google.com/scholar?q={q_scholar}" target="_blank" class="search-link" style="background:#db4437; color:white;">🎓 Google Scholar</a>', unsafe_allow_html=True)

        # 2. THE WIZARD
        st.markdown("<br>", unsafe_allow_html=True)
        
        for i in range(n - 1):
            # Modern Header for sections
            st.markdown(f"<h4 style='margin-top:20px; border-bottom:1px solid #555;'>Comparing: {factors[i]}</h4>", unsafe_allow_html=True)
            
            for j in range(i + 1, n):
                # Logic to get values
                val = st.session_state.matrix[i, j]
                if val >= 1:
                    sel_idx = 0 # A
                    curr_score = int(round(val))
                else:
                    sel_idx = 1 # B
                    curr_score = int(round(1/val)) if val != 0 else 1
                
                # Card for each comparison
                st.markdown(f"<div class='st-card'>", unsafe_allow_html=True)
                
                c_factorA, c_factorB, c_control = st.columns([2, 2, 4])
                
                with c_factorA:
                    st.markdown(f"**{factors[i]}**")
                    if sel_idx == 0: st.caption(f"Winner (Intensity: {curr_score})")
                
                with c_factorB:
                    st.markdown(f"**{factors[j]}**")
                    if sel_idx == 1: st.caption(f"Winner (Intensity: {curr_score})")
                
                with c_control:
                    # Winner Selection
                    choice = st.radio(f"Winner {i}-{j}", ["Left is Important", "Right is Important"], 
                                      index=sel_idx, horizontal=True, label_visibility="collapsed", key=f"rad_{i}_{j}")
                    
                    # Intensity Slider
                    score = st.select_slider(f"Intensity {i}-{j}", options=[1,2,3,4,5,6,7,8,9], 
                                             value=curr_score, label_visibility="collapsed", key=f"slide_{i}_{j}")
                
                st.markdown("</div>", unsafe_allow_html=True)

                # Update State
                final_val = float(score)
                if choice == "Left is Important":
                    st.session_state.matrix[i, j] = final_val
                    st.session_state.matrix[j, i] = 1 / final_val
                else:
                    st.session_state.matrix[i, j] = 1 / final_val
                    st.session_state.matrix[j, i] = final_val

# >>> PAGE: PRESETS <<<
elif selection == "📂 Geospatial Presets":
    st.markdown("### 📂 Analysis Templates")
    st.markdown("Select a preset to instantly load standard criteria for geospatial analysis.")
    
    col_p1, col_p2, col_p3 = st.columns(3)
    
    with col_p1:
        st.markdown("<div class='st-card animate-fade'><h4>🌊 Flood Risk</h4><p>Rainfall, Slope, Soil Type, Elevation, Land Use</p></div>", unsafe_allow_html=True)
        if st.button("Load Flood Risk"):
            st.session_state.factors = ["Rainfall", "Slope", "Soil Type", "Elevation", "Land Use"]
            n = len(st.session_state.factors)
            st.session_state.matrix = np.ones((n, n))
            st.success("Flood Risk Factors Loaded!")
            st.rerun()

    with col_p2:
        st.markdown("<div class='st-card animate-fade'><h4>🗑️ Landfill Suitability</h4><p>Dist. to River, Dist. to Road, Slope, Land Cost</p></div>", unsafe_allow_html=True)
        if st.button("Load Landfill"):
            st.session_state.factors = ["Dist to River", "Dist to Road", "Slope", "Land Cost"]
            n = len(st.session_state.factors)
            st.session_state.matrix = np.ones((n, n))
            st.success("Landfill Factors Loaded!")
            st.rerun()

    with col_p3:
        st.markdown("<div class='st-card animate-fade'><h4>🏥 Hospital Site</h4><p>Pop. Density, Dist. to Major Road, Land Cost</p></div>", unsafe_allow_html=True)
        if st.button("Load Hospital"):
            st.session_state.factors = ["Pop Density", "Dist to Major Road", "Land Cost"]
            n = len(st.session_state.factors)
            st.session_state.matrix = np.ones((n, n))
            st.success("Hospital Factors Loaded!")
            st.rerun()

# >>> PAGE: RESULTS <<<
elif selection == "📊 Final Results":
    st.markdown("### 📊 Analysis Report")
    
    factors = st.session_state.factors
    A = st.session_state.matrix
    n = len(factors)
    
    try:
        # Calculations
        col_sums = A.sum(axis=0)
        norm_matrix = A / col_sums
        weights = norm_matrix.mean(axis=1)
        
        # Consistency
        lambda_max = (A @ weights / weights).mean()
        CI = (lambda_max - n) / (n - 1)
        ri_dict = {1:0, 2:0, 3:0.58, 4:0.90, 5:1.12, 6:1.24, 7:1.32, 8:1.41, 9:1.45, 10:1.49}
        RI = ri_dict.get(n, 1.59)
        CR = CI / RI if RI != 0 else 0
        
        # Metrics Display
        st.markdown("<div class='metric-container animate-fade'>", unsafe_allow_html=True)
        
        # Custom HTML Metrics
        st.markdown(f"<div class='metric-item'><div>Lambda Max (λ)</div><div style='font-size:1.5em'>{lambda_max:.4f}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-item'><div>Consistency Index</div><div style='font-size:1.5em'>{CI:.4f}</div></div>", unsafe_allow_html=True)
        
        cr_color = "#00C851" if CR < 0.1 else "#ff4444"
        cr_status = "PASS" if CR < 0.1 else "FAIL"
        st.markdown(f"<div class='metric-item' style='border-left: 4px solid {cr_color}; color:{cr_color};'><div>Consistency Ratio</div><div style='font-size:1.5em'>{CR:.4f} ({cr_status})</div></div>", unsafe_allow_html=True)
        
        st.markdown("</div><br>", unsafe_allow_html=True)

        if CR > 0.1:
            st.error("⚠️ Inconsistency Detected: Please review your comparisons in the 'Custom Analysis' tab.")
        else:
            st.success("✅ Consistency Check Passed. These weights are scientifically valid.")

        # Visualization & Table
        c_vis, c_tab = st.columns([3, 2])
        
        df_res = pd.DataFrame({"Criteria": factors, "Weight": weights, "Percentage": weights*100})
        df_res = df_res.sort_values("Weight", ascending=False)

        with c_vis:
            st.markdown("<div class='st-card'>", unsafe_allow_html=True)
            st.markdown("#### Weight Distribution")
            fig, ax = plt.subplots(figsize=(6, 4))
            
            # Plot Theme Logic
            bg = '#1e212b' if st.session_state.theme == 'dark' else '#ffffff'
            fg = 'white' if st.session_state.theme == 'dark' else '#333'
            
            fig.patch.set_facecolor(bg)
            ax.set_facecolor(bg)
            sns.barplot(x="Weight", y="Criteria", data=df_res, ax=ax, palette="viridis")
            
            ax.tick_params(colors=fg)
            ax.xaxis.label.set_color(fg)
            ax.yaxis.label.set_color(fg)
            for spine in ax.spines.values(): spine.set_color(fg)
            
            st.pyplot(fig)
            st.markdown("</div>", unsafe_allow_html=True)

        with c_tab:
            st.markdown("<div class='st-card'>", unsafe_allow_html=True)
            st.markdown("#### Data Export")
            st.dataframe(
                df_res.style.format({"Weight": "{:.4f}", "Percentage": "{:.2f}%"}).background_gradient(cmap="Greens"),
                use_container_width=True
            )
            csv = df_res.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download CSV", csv, "ahp_final_weights.csv", "text/csv", type="primary")
            st.markdown("</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Calculation Error: {e}")

# >>> PAGE: HELP <<<
elif selection == "❓ Help & Guide":
    st.markdown("### 📚 Reference Guide")
    
    with st.expander("📏 Saaty's Fundamental Scale (The 'Intensity' Slider)", expanded=True):
        saaty_data = {
            "Intensity": [1, 3, 5, 7, 9],
            "Definition": ["Equal", "Moderate", "Strong", "Very Strong", "Extreme"],
            "Explanation": [
                "Factors are equally important.",
                "Experience slightly favors one.",
                "Experience strongly favors one.",
                "Dominance is demonstrated in practice.",
                "Highest possible order of affirmation."
            ]
        }
        st.table(pd.DataFrame(saaty_data))
    
    with st.expander("❓ How to fix Inconsistency (CR > 0.1)"):
        st.write("""
        If your CR is high, it means your judgments are circular or illogical. 
        * Example of logic: If A > B and B > C, then A must be > C.
        * Example of inconsistency: A > B, B > C, but C > A.
        
        **Solution:** Go back to 'Custom Analysis' and check for these circular loops.
        """)

# --- FOOTER ---
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align: center; opacity: 0.6; font-size: 0.9em;'>"
    "Advanced AHP Tool by Sayeem | v2.0 Professional Edition"
    "</div>", 
    unsafe_allow_html=True
)