import streamlit as st
import pandas as pd
import numpy as np
import os
import re

# Page Configuration
st.set_page_config(
    page_title="Streamlit Web App Planner & Generator",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Glassmorphic Dark CSS Styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&family=Outfit:wght@400;600;800&display=swap');

/* Main App Container background */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0b0c10 0%, #151728 100%);
    color: #e2e8f0;
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Sidebar Custom Styling */
[data-testid="stSidebar"] {
    background: rgba(15, 17, 28, 0.95) !important;
    backdrop-filter: blur(12px);
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}

/* Glowing Typography */
.title-container {
    background: linear-gradient(90deg, #8b5cf6 0%, #6366f1 50%, #06b6d4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    font-size: 2.5rem;
    margin-bottom: 0.2rem;
    text-shadow: 0 0 30px rgba(99, 102, 241, 0.15);
}

.subtitle-container {
    color: #94a3b8;
    font-size: 1.05rem;
    margin-bottom: 2rem;
    font-weight: 300;
}

/* Glassmorphism Cards */
.spec-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    backdrop-filter: blur(8px);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
}

.spec-card:hover {
    border-color: rgba(99, 102, 241, 0.25);
    box-shadow: 0 8px 32px 0 rgba(99, 102, 241, 0.05);
    transform: translateY(-2px);
}

/* Glowing subheaders */
.step-header {
    font-family: 'Outfit', sans-serif;
    color: #f1f5f9;
    font-size: 1.5rem;
    font-weight: 600;
    border-bottom: 2px solid rgba(99, 102, 241, 0.2);
    padding-bottom: 8px;
    margin-bottom: 20px;
}

.stat-box {
    background: rgba(99, 102, 241, 0.08);
    border: 1px solid rgba(99, 102, 241, 0.15);
    border-radius: 12px;
    padding: 15px;
    text-align: center;
    margin-bottom: 15px;
}

.stat-num {
    font-size: 1.8rem;
    font-weight: 700;
    color: #a78bfa;
}

/* Style Inputs */
.stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
    background-color: rgba(255, 255, 255, 0.03) !important;
    color: #f8fafc !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 8px !important;
}

.stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
}

/* Clean divider */
hr {
    border: 0;
    height: 1px;
    background: linear-gradient(to right, rgba(99, 102, 241, 0), rgba(99, 102, 241, 0.3), rgba(99, 102, 241, 0));
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# Helper Paths
SPEC_FILE = os.path.join(os.path.dirname(__file__), "test.md")

# 1. Parsing function
def parse_markdown(filepath):
    data = {
        "project_name": "My Streamlit Web App",
        "purpose": "",
        "target_user": "",
        "features": [],
        "sidebar": "",
        "main_page": "",
        "libraries": ["streamlit", "pandas"],
        "data_flow": "",
        "layout_type": "Multi-Tab Navigation",
        "tabs": ["Dashboard", "Analytics", "Settings"],
        "session_state_vars": [
            ["data_loaded", "bool", "False", "Tracks if the dataset is successfully loaded"],
            ["df", "DataFrame", "None", "The parsed data structure"],
            ["theme", "str", "'Dark'", "Interface presentation theme mode"]
        ]
    }
    
    if not os.path.exists(filepath):
        return data
        
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Parse Project Name
        match_name = re.search(r"# 프로젝트명:\s*(.*?)\s*-\s*Streamlit Web App", content)
        if not match_name:
            match_name = re.search(r"# 프로젝트명:\s*(.*)", content)
        if match_name:
            name_val = match_name.group(1).strip()
            if name_val and "[추후 결정]" not in name_val:
                data["project_name"] = name_val
                
        # Parse Purpose
        match_purpose = re.search(r"-\s*\*\*목적:\*\*\s*(.*)", content)
        if match_purpose:
            purpose_val = match_purpose.group(1).strip()
            if purpose_val and "(예:" not in purpose_val:
                data["purpose"] = purpose_val
                
        # Parse Target User
        match_user = re.search(r"-\s*\*\*타겟 유저:\*\*\s*(.*)", content)
        if match_user:
            user_val = match_user.group(1).strip()
            if user_val and "(예:" not in user_val:
                data["target_user"] = user_val
                
        # Parse Features
        feature_lines = re.findall(r"-\s*\[([ xX])\]\s*(.*)", content)
        parsed_features = []
        for checked_char, text in feature_lines:
            text_clean = text.strip()
            if "기능 " in text_clean and text_clean.endswith("..."):
                continue  # Skip template placeholders
            parsed_features.append({
                "checked": checked_char.lower() == "x",
                "text": text_clean
            })
        if parsed_features:
            data["features"] = parsed_features
            
        # Parse Sidebar Layout
        match_sidebar = re.search(r"-\s*\*\*Sidebar:\*\*\s*(.*)", content)
        if match_sidebar:
            sidebar_val = match_sidebar.group(1).strip()
            if sidebar_val and "(사이드바" not in sidebar_val:
                data["sidebar"] = sidebar_val
                
        # Parse Main Page Layout
        match_main = re.search(r"-\s*\*\*Main Page:\*\*\s*(.*)", content)
        if match_main:
            main_val = match_main.group(1).strip()
            if main_val and "(메인" not in main_val:
                data["main_page"] = main_val
                
        # Parse Libraries
        match_lib = re.search(r"-\s*\*\*필요한 라이브러리:\*\*\s*(.*)", content)
        if match_lib:
            lib_val = match_lib.group(1).strip()
            if lib_val and "streamlit, pandas 등" not in lib_val:
                libs = lib_val.split(",")
                data["libraries"] = [l.strip() for l in libs if l.strip()]
                
        # Parse Data Flow
        match_flow = re.search(r"-\s*\*\*데이터 흐름:\*\*\s*(.*)", content)
        if match_flow:
            flow_val = match_flow.group(1).strip()
            if flow_val and "(State" not in flow_val:
                data["data_flow"] = flow_val
                
    except Exception as e:
        st.warning(f"Error parsing test.md: {str(e)}. Loading default specifications.")
        
    return data

# 2. Saving function
def generate_markdown_content(data):
    features_md = ""
    for f in data["features"]:
        check = "x" if f["checked"] else " "
        features_md += f"- [{check}] {f['text']}\n"
    if not features_md:
        features_md = "- [ ] 기능 1: ...\n- [ ] 기능 2: ...\n"
        
    libs_str = ", ".join(data["libraries"])
    
    # Session state description formatted nicely for Markdown
    session_states_md = ""
    for var in data["session_state_vars"]:
        session_states_md += f"  - `st.session_state['{var[0]}']` (Type: {var[1]}, Default: {var[2]}): {var[3]}\n"
        
    ai_guidelines = f"""- "너는 시니어 파이썬 Streamlit 개발자야. 아래 규칙을 지켜서 코드를 작성해줘"
- 가독성이 높고 모듈화가 잘 된 클린 코드로 구현할 것.
- Streamlit의 최신 API 규격 및 session_state 흐름 설계 가이드를 엄수할 것.
- 시각적인 완성도를 높이기 위해 CSS 주입 및 레이아웃을 매끄럽게 다듬을 것."""

    content = f"""# 프로젝트명: {data['project_name']} - Streamlit Web App

## 1. 프로젝트 개요
- **목적:** {data['purpose'] if data['purpose'] else '(예: 어떤 문제를 해결하기 위한 앱인지)'}
- **타겟 유저:** {data['target_user'] if data['target_user'] else '(예: 일반 사용자, 내부 직원 등)'}

## 2. 주요 기능 요구사항 (Features)
{features_md}
## 3. UI/UX 및 페이지 구조 (Streamlit Layout)
- **Sidebar:** {data['sidebar'] if data['sidebar'] else '(사이드바 구성 요소)'}
- **Main Page:** {data['main_page'] if data['main_page'] else '(메인 화면 레이아웃 및 탭 구성)'}
  - **Layout Type:** {data['layout_type']}
  - **Tabs/Pages:** {", ".join(data['tabs'])}

## 4. 데이터 및 시스템 구조
- **필요한 라이브러리:** {libs_str}
- **데이터 흐름:** {data['data_flow'] if data['data_flow'] else '(State 관리, Session State 활용 계획)'}
{session_states_md}
## 5. AI 에이전트를 위한 구현 지침 (Prompt for Cursor/Windsurf)
{ai_guidelines}
"""
    return content

# 3. Boilerplate Code Generator Function
def generate_boilerplate_code(data):
    imports = ["import streamlit as st"]
    for lib in data["libraries"]:
        lib_clean = lib.split()[0].strip() # Handles 'pandas' vs 'pandas as pd' etc.
        if lib_clean not in ["streamlit", "st", ""]:
            imports.append(f"import {lib_clean}")
            
    # Add optional pandas/numpy mock elements just in case they are needed for demo
    if "pandas" not in [l.split()[0].strip() for l in data["libraries"]]:
        imports.append("# import pandas as pd  # Optional dependency")
        
    imports_str = "\n".join(imports)
    
    # Session state init
    session_states_init = []
    session_states_init.append("# Initialize defined session state variables")
    for key, val_type, initial_val, desc in data["session_state_vars"]:
        session_states_init.append(f"if '{key}' not in st.session_state:")
        # Attempt syntax matching for initialization
        init_repr = initial_val
        if val_type.lower() in ["string", "str"] and not (init_repr.startswith("'") or init_repr.startswith('"')):
            init_repr = f"'{init_repr}'"
        session_states_init.append(f"    st.session_state['{key}'] = {init_repr}  # {desc}")
        
    session_states_init_str = "\n    ".join(session_states_init)
    
    # Custom CSS mockup for generating code
    custom_css_inject = """
    # Custom CSS Injection for modern sleek styling
    st.markdown(\"\"\"
    <style>
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
    </style>
    \"\"\", unsafe_allow_html=True)
    """

    # Title styling
    title_section = f"""# Page configuration
st.set_page_config(
    page_title="{data['project_name']}",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

{custom_css_inject}

# App Title & Subtitle
st.title("✨ {data['project_name']}")
st.markdown("*{data['purpose']}*")
"""

    # Sidebar section
    sidebar_code = f"""# Sidebar Layout
with st.sidebar:
    st.header("⚙️ Configuration")
    st.markdown("### Controls & Metadata")
    st.info("{data['sidebar'] if data['sidebar'] else 'Define sidebar inputs and actions'}")
    
    # Boilerplate controls
    st.subheader("Filter Criteria")
    selected_option = st.selectbox("View mode", ["Overview", "Detailed Report"])
    slider_val = st.slider("Sample Threshold", 0, 100, 50)
"""

    # Main page layout setup
    main_page_code = ""
    layout_type = data["layout_type"]
    tabs_list = data["tabs"]
    
    if layout_type == "Multi-Tab Navigation" and tabs_list:
        tabs_str = ", ".join([f'"{tab}"' for tab in tabs_list])
        main_page_code = f"""# Tabs Layout
tabs = st.tabs([{tabs_str}])
"""
        for i, tab in enumerate(tabs_list):
            main_page_code += f"""
with tabs[{i}]:
    st.header("📊 {tab}")
    st.write("Layout & data placeholder for the **{tab}** container.")
    
    # Demo elements
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="metric-card"><h4>Primary Stat</h4><h2>1,452</h2><p style="color:#10b981">▲ 12.4% vs last week</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h4>System Performance</h4><h2>98.9%</h2><p style="color:#6366f1">SLA Target Achieved</p></div>', unsafe_allow_html=True)
        
    st.markdown("---")
    st.write("🚀 **Interactive widgets:**")
    st.button("Perform Action on {tab}", key="btn_{tab.lower().replace(' ', '_')}")
"""
    elif layout_type == "Sidebar Navigation" and tabs_list:
        main_page_code = f"""# Sidebar Navigation Layout
st.sidebar.markdown("---")
navigation_option = st.sidebar.radio("Navigate Sections", [{', '.join([f'"{tab}"' for tab in tabs_list])}])

st.subheader(f"📍 Navigation: {{navigation_option}}")
st.write(f"Focusing workspace view on the **{{navigation_option}}** section.")

# Dynamic structure
col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("Functional Workspace")
    st.write("Insert principal UI elements, charts, and tables here.")
    st.code("# Code block target\\nprint('Hello Streamlit User!')", language="python")
with col2:
    st.subheader("Quick Actions")
    st.button("Sync Data", help="Simulate data fetch operations")
"""
    else:
        # Single Page layout
        main_page_code = f"""# Single Page Layout
st.subheader("📋 Core Application Workflow")
st.write("{data['main_page'] if data['main_page'] else 'Specify dashboard controls and data presentation panels'}")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Requirements", "{len(data['features'])}")
with col2:
    st.metric("Required Packages", "{len(data['libraries'])}")
with col3:
    st.metric("Initialized Variables", "{len(data['session_state_vars'])}")

st.markdown("### Required Checklist Items")
"""
        for i, feat in enumerate(data["features"]):
            check_val = "True" if feat["checked"] else "False"
            main_page_code += f"st.checkbox('{feat['text']}', value={check_val}, key='feat_chk_{i}')\n"

    code = f"""\"\"\"
Generated Streamlit Boilerplate Code
Project: {data['project_name']}
Purpose: {data['purpose']}
Target User: {data['target_user']}
\"\"\"

{imports_str}

{title_section}

def main():
    {session_states_init_str}
    
    {sidebar_code}
    
    {main_page_code}
    
    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: gray;'>Designed & Generated by Streamlit Web App Planner</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
"""
    return code


# Initialize App Session State
if "spec" not in st.session_state:
    st.session_state["spec"] = parse_markdown(SPEC_FILE)

# Layout Setup
col_left, col_right = st.columns([1, 4])

with col_left:
    st.markdown('<div class="stat-box"><div class="stat-num">Planner</div>Workspace</div>', unsafe_allow_html=True)
    
    # Step Selection Sidebar Menu
    step = st.radio(
        "Navigation Steps",
        [
            "📋 Project Overview",
            "🎯 Feature Requirements",
            "🎨 UI Layout Designer",
            "⚙️ System & State",
            "🚀 Generate Code & Spec"
        ]
    )
    
    st.markdown("---")
    # File statistics
    st.markdown(f"**Loaded Spec File:**\n`{os.path.basename(SPEC_FILE)}`")
    if os.path.exists(SPEC_FILE):
        st.success("File Found & Loaded")
    else:
        st.warning("Template File Missing")

with col_right:
    # Header Banner
    st.markdown('<div class="title-container">Streamlit App Planner</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-container">Design layout structures, set session state parameters, and compile ready-to-run boilerplate script.</div>', unsafe_allow_html=True)

    spec = st.session_state["spec"]

    # STEP 1: Overview
    if step == "📋 Project Overview":
        st.markdown('<div class="step-header">📋 Step 1: Project Overview & Meta Information</div>', unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="spec-card">', unsafe_allow_html=True)
            spec["project_name"] = st.text_input("Project Name (프로젝트명)", spec["project_name"])
            spec["purpose"] = st.text_area("App Purpose & Goals (목적)", spec["purpose"], placeholder="Explain what problem this app resolves...")
            spec["target_user"] = st.text_input("Target Users (타겟 유저)", spec["target_user"], placeholder="Internal team, public users, managers, etc.")
            st.markdown('</div>', unsafe_allow_html=True)
            
    # STEP 2: Feature Requirements
    elif step == "🎯 Feature Requirements":
        st.markdown('<div class="step-header">🎯 Step 2: Feature Requirements Checklists</div>', unsafe_allow_html=True)
        st.markdown("Define specific checklists for the application functions.")
        
        # Add new feature form
        with st.form("new_feature_form", clear_on_submit=True):
            new_feat = st.text_input("Add New Feature", placeholder="Type feature description and press Add")
            submitted = st.form_submit_button("Add Feature")
            if submitted and new_feat.strip():
                spec["features"].append({"checked": False, "text": new_feat.strip()})
                st.success(f"Added: '{new_feat.strip()}'")
                st.rerun()

        # Display and edit current features
        if spec["features"]:
            st.markdown("### Current Features Checklist")
            st.caption("Toggle checkbox status or modify description texts:")
            
            features_to_remove = []
            for idx, feat in enumerate(spec["features"]):
                col_check, col_text, col_del = st.columns([1, 12, 2])
                with col_check:
                    feat["checked"] = st.checkbox("", value=feat["checked"], key=f"feat_chk_{idx}")
                with col_text:
                    feat["text"] = st.text_input("", value=feat["text"], key=f"feat_txt_{idx}", label_visibility="collapsed")
                with col_del:
                    if st.button("🗑️ Delete", key=f"feat_del_{idx}"):
                        features_to_remove.append(idx)
            
            if features_to_remove:
                for idx in sorted(features_to_remove, reverse=True):
                    spec["features"].pop(idx)
                st.rerun()
        else:
            st.info("No features defined. Please use the form above to add features.")

    # STEP 3: UI Layout Designer
    elif step == "🎨 UI Layout Designer":
        st.markdown('<div class="step-header">🎨 Step 3: UI/UX & Page Layout Configurations</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="spec-card">', unsafe_allow_html=True)
        spec["sidebar"] = st.text_area("Sidebar Widgets Description", spec["sidebar"], placeholder="Describe widgets to load in the sidebar (filters, uploaders, status texts)")
        spec["main_page"] = st.text_area("Main Page Content Description", spec["main_page"], placeholder="Explain dashboard layouts, graphics, and interactive columns")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Layout selector
        st.markdown("### Interactive Structural Wireframe Designer")
        col_wire_left, col_wire_right = st.columns([2, 3])
        
        with col_wire_left:
            spec["layout_type"] = st.selectbox(
                "App Layout Type", 
                ["Single Page Layout", "Multi-Tab Navigation", "Sidebar Navigation"]
            )
            
            if spec["layout_type"] in ["Multi-Tab Navigation", "Sidebar Navigation"]:
                st.markdown("#### Page / Tab Configuration")
                tabs_string = st.text_input("Define Tab/Page names (comma-separated)", ", ".join(spec["tabs"]))
                spec["tabs"] = [t.strip() for t in tabs_string.split(",") if t.strip()]
        
        with col_wire_right:
            st.markdown("**Visual Wireframe Preview (Mockup):**")
            # Draw preview container based on chosen structure
            if spec["layout_type"] == "Single Page Layout":
                st.code("""
┌────────────────────────────────────────────────────────┐
│  ✨ TITLE: """ + spec["project_name"] + """
├────────────────────────────────────────────────────────┤
│  [Sidebar Controls]      │  [Main Panel Section]       │
│  - Filters & Slider      │  - Metrics Summary Cards    │
│  - Info description      │  - Checked Requirement Lists│
│                          │  - Primary Action Buttons   │
└────────────────────────────────────────────────────────┘
""", language="text")
            elif spec["layout_type"] == "Multi-Tab Navigation":
                tabs_preview = " | ".join([f"[{t}]" for t in spec["tabs"]])
                st.code(f"""
┌────────────────────────────────────────────────────────┐
│  ✨ TITLE: {spec["project_name"]}
├────────────────────────────────────────────────────────┤
│  [Sidebar Controls]      │  Tabs: {tabs_preview}
│  - Filters & Slider      ├─────────────────────────────┤
│  - Info description      │  Active Tab Content Panel   │
│                          │  - Mockup Charts & Metrics  │
└────────────────────────────────────────────────────────┘
""", language="text")
            else: # Sidebar Navigation
                radio_preview = "\n│  (o) " + "\n│  ( ) ".join(spec["tabs"])
                st.code(f"""
┌────────────────────────────────────────────────────────┐
│  ✨ TITLE: {spec["project_name"]}
├────────────────────────────────────────────────────────┤
│  [Sidebar Controls]      │  [Section Content Window]   │
│  Navigation Menu:        │  - Functional work grids    │
{radio_preview}               │  - Subheader dashboards     │
│                          │  - Code block consoles      │
└────────────────────────────────────────────────────────┘
""", language="text")

    # STEP 4: System Config & State
    elif step == "⚙️ System & State":
        st.markdown('<div class="step-header">⚙️ Step 4: Data Structures, Libraries & Session State</div>', unsafe_allow_html=True)
        
        col_sys1, col_sys2 = st.columns(2)
        
        with col_sys1:
            st.markdown("### Package Dependencies")
            # Select python libraries
            lib_options = ["streamlit", "pandas", "numpy", "matplotlib", "seaborn", "plotly", "scikit-learn", "requests", "sqlite3", "openpyxl"]
            # Filter valid options from what was parsed
            valid_parsed_libs = [lib for lib in spec["libraries"] if lib in lib_options]
            selected_libs = st.multiselect("Select libraries to import in code", lib_options, default=valid_parsed_libs if valid_parsed_libs else ["streamlit", "pandas"])
            
            # Custom library text inputs
            other_lib = st.text_input("Add other packages (comma-separated)", "")
            if other_lib:
                other_libs_list = [l.strip() for l in other_lib.split(",") if l.strip()]
                for ol in other_libs_list:
                    if ol not in selected_libs:
                        selected_libs.append(ol)
            
            spec["libraries"] = selected_libs
            
            st.markdown("### Data Flow Description")
            spec["data_flow"] = st.text_area("Global Data Operations Spec", spec["data_flow"], placeholder="How data loads, parses, filter modifications, and cached computations")
            
        with col_sys2:
            st.markdown("### Session State Configuration")
            st.caption("Initialize global variables loaded instantly in `st.session_state`:")
            
            # Add state variable form
            with st.form("new_var_form", clear_on_submit=True):
                col_n1, col_n2, col_n3 = st.columns(3)
                with col_n1:
                    new_var_name = st.text_input("Var Name", placeholder="e.g. data_df")
                with col_n2:
                    new_var_type = st.selectbox("Type", ["bool", "int", "str", "list", "dict", "DataFrame", "None"])
                with col_n3:
                    new_var_val = st.text_input("Default Val", placeholder="e.g. False, 'User'")
                    
                new_var_desc = st.text_input("Variable Description", placeholder="Tracks session values across widgets...")
                submitted_var = st.form_submit_button("Add State Variable")
                
                if submitted_var and new_var_name.strip():
                    spec["session_state_vars"].append([
                        new_var_name.strip(), 
                        new_var_type, 
                        new_var_val.strip() if new_var_val.strip() else "None", 
                        new_var_desc.strip()
                    ])
                    st.success(f"Added State Variable: '{new_var_name.strip()}'")
                    st.rerun()
                    
            # Display current session state vars
            if spec["session_state_vars"]:
                st.markdown("#### Initializing States List")
                var_to_remove = []
                for idx, var in enumerate(spec["session_state_vars"]):
                    col_v_info, col_v_del = st.columns([12, 3])
                    with col_v_info:
                        st.markdown(f"🔑 **`st.session_state['{var[0]}']`** ({var[1]}) ➔ Default: `{var[2]}`\n*{var[3]}*")
                    with col_v_del:
                        if st.button("🗑️ Delete", key=f"var_del_{idx}"):
                            var_to_remove.append(idx)
                            
                if var_to_remove:
                    for idx in sorted(var_to_remove, reverse=True):
                        spec["session_state_vars"].pop(idx)
                    st.rerun()

    # STEP 5: Generate Spec & Code
    elif step == "🚀 Generate Code & Spec":
        st.markdown('<div class="step-header">🚀 Step 5: Export Markdown Specifications & Python App Boilerplate</div>', unsafe_allow_html=True)
        
        md_content = generate_markdown_content(spec)
        code_content = generate_boilerplate_code(spec)
        
        col_exp1, col_exp2 = st.columns(2)
        
        with col_exp1:
            st.subheader("📝 Updated Markdown Spec (`test.md`)")
            st.markdown("This shows what will be written to `test.md` inside your workspace.")
            st.text_area("Markdown Preview", md_content, height=400)
            
            # Action: Save Markdown
            if st.button("💾 Save Specification to test.md", use_container_width=True):
                try:
                    with open(SPEC_FILE, "w", encoding="utf-8") as f:
                        f.write(md_content)
                    st.success("Successfully updated `test.md` in workspace!")
                except Exception as e:
                    st.error(f"Failed to save to `test.md`: {str(e)}")
                    
        with col_exp2:
            st.subheader("🐍 Generated Streamlit App (`generated_app.py`)")
            st.markdown("A ready-to-run skeleton utilizing defined states, layouts, and libraries.")
            st.text_area("Python Code Preview", code_content, height=400)
            
            # Save Boilerplate code to file
            boilerplate_path = os.path.join(os.path.dirname(__file__), "generated_app.py")
            if st.button("🚀 Write Boilerplate to generated_app.py", use_container_width=True):
                try:
                    with open(boilerplate_path, "w", encoding="utf-8") as f:
                        f.write(code_content)
                    st.success(f"Successfully created `{os.path.basename(boilerplate_path)}` in workspace!")
                except Exception as e:
                    st.error(f"Failed to write boilerplate: {str(e)}")
                    
            st.info("💡 You can run the generated app using: `streamlit run generated_app.py`")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748b;'>Antigravity Streamlit Web App Planner & Generator © 2026</p>", unsafe_allow_html=True)
