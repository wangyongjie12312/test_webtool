import streamlit as st
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="Help Documentation - Safelink OrcaFlex Tool",
    page_icon="📖",
    layout="wide"
)

# Header
st.markdown("# 📖 Help Documentation")
st.markdown("### Complete guide for using the Safelink OrcaFlex External Function Configuration Tool")
st.warning("### Opening multiple tools at the same time may cause conflicts.")

# Add custom CSS
st.markdown("""
<style>
    /* Blue button style */
    .link-button-blue .stPageLink > a {
        background-color: #007bff !important;
        color: white !important;
        border: 2px solid #0056b3 !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        text-decoration: none !important;
        display: inline-block !important;
        font-weight: bold !important;
    }
    .link-button-blue .stPageLink > a:hover {
        background-color: #0056b3 !important;
        border-color: #004085 !important;
    }
    
    /* Red button style */
    .link-button-red .stPageLink > a {
        background-color: #dc3545 !important;
        color: white !important;
        border: 2px solid #c82333 !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        text-decoration: none !important;
        display: inline-block !important;
        font-weight: bold !important;
    }
    .link-button-red .stPageLink > a:hover {
        background-color: #c82333 !important;
        border-color: #bd2130 !important;
    }
    
    /* Green button style */
    .link-button-green .stPageLink > a {
        background-color: #28a745 !important;
        color: white !important;
        border: 2px solid #1e7e34 !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        text-decoration: none !important;
        display: inline-block !important;
        font-weight: bold !important;
    }
    .link-button-green .stPageLink > a:hover {
        background-color: #1e7e34 !important;
        border-color: #155724 !important;
    }
    
    /* Orange outline style */
    .link-button-outline .stPageLink > a {
        background-color: transparent !important;
        color: #fd7e14 !important;
        border: 2px solid #fd7e14 !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        text-decoration: none !important;
        display: inline-block !important;
        font-weight: bold !important;
    }
    .link-button-outline .stPageLink > a:hover {
        background-color: #fd7e14 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Main content tabs
tab1, tab2 = st.tabs(["🖥️ Web UI Configuration Tool", "🔧 External Function Usage"])

with tab1:
    st.header("🖥️ How to Use the Web UI Configuration Tool")
    
    image_certificate = Image.open(r"./figures/WebUI_flowchart_short.png")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.image(image_certificate, width=400)    
    # Quick Start Guide
    with st.expander("🚀 Quick Start Guide", expanded=True):
        
        # Step-by-step instructions
        st.markdown("## 📋 Step-by-Step Instructions")
        
        # Step 1: Authentication
        with st.container():
            st.markdown("### Step 1: Authentication & Login")
            
            col_step1_1, col_step1_2 = st.columns([2, 1])
            
            with col_step1_1:
                st.markdown("""
                **🔐 Login Process:**
                - Access the tool through your web browser
                - Enter your username and password. Contact post@safelink.no for full access
                - For demo purposes, use: `demo` / `demo`
                
                    - View welcome page and documentation
                    - Download examples. 
                
                **⚠️ Session Management:**
                - Sessions expire after 30 minutes of inactivity
                - Progress is saved automatically
                """)
            
        
        st.divider()
        
        # Step 2: Unit Selection
        with st.container():
            st.markdown("### Step 2: Unit Selection")
            
            col_step2_1, col_step2_2 = st.columns([2, 1])
            
            with col_step2_1:
                st.markdown("""
                1. **Choose Unit Type:**
                -  **IAHC** - Inline Active Heave Compensator, suitable for lifting operations requiring high control accuracy such as turbine installation.  
                -  **PHC** - Passive Heave Compensator, suitable for splash zone crossing protection, resonance protection, and subsea landing protection. 
                -  **Shock Absorber** - Spring + Damping system, suitable for e.g., protection of hammer and crane during pile running.
                
                2. **Select Specific Unit:**
                - Browse available units with different Unit IDs as marked on the ID plates on real units.  
                - Check technical parameters (stroke, pressure, etc.) from the **Specifications** and special features. 
                - The selected unit will be shown and highlighted. 
                
                3. **Configure Parameters:**
                - Set unit-specific parameters
                - Configure payload parameters
                
                """)
            
            with col_step2_2:
                st.info("""
                Selection is persistent across pages - your choice is remembered even if you navigate away.
                """)
        
        st.divider()
        
        # Step 3: Results Configuration
        with st.container():
            st.markdown("### Step 3: Results Configuration")
            
            col_step3_1, col_step3_2 = st.columns([2, 1])
            
            with col_step3_1:
                st.markdown("""
                **Two Options are:**
                
                1. **OrcaFlex Default:**
                    - Uses standard OrcaFlex result outputs
                    - Minimal configuration required
                    - Optimized simulation speed
                    - Good for basic simulations
                
                2. **Customized Results:**
                    - Add Safelink-specific parameters
                    - Choose from 40+ specialized results
                    - Slows down the simulation slightly 
                    - Organized by three categories:
                    
                        🔵 Body Results
                        🟢 Rod Results
                        🟡 Payload Results
                """)
            
        
        st.divider()
        
        # Step 4: Export
        with st.container():
            st.markdown("### Step 4: Export Configuration")
            
            col_step4_1, col_step4_2 = st.columns([2, 1])
            
            with col_step4_1:
                st.markdown("""
                **📤 Export Process:**
                
                1. **Review Configuration:**
                - Check selected unit details
                - Verify results selections
                - Review export preview
                
                2. **Generate Configuration:**
                - Click "Export" button
                - System generates INI file
                - Includes all your selections
                
                3. **Download File:**
                - File: `safelink_orcaflex_external_function_settings.ini`
                - Note: Allow if download is blocked. 
                
                """)
            
            with col_step4_2:
                st.warning("""
                **⚠️ Before Export:**
                
                - Ensure unit is selected
                - Verify results configuration
                - Check export preview
                """)
                
                st.success("""
                **✅ File Ready:**
                
                Your configuration file is ready for use in OrcaFlex external function setup.
                """)
        
        # Troubleshooting
        st.divider()
        st.markdown("## 🔧 Troubleshooting")
        
        col_trouble1, col_trouble2 = st.columns([1, 1])
        
        with col_trouble1:
            st.markdown("""
            **Common Issues:**
            
            **🔑 Login Problems:**
            - Check username/password spelling
            - Try demo account: `demo`/`demo`
            - Contact support for access issues
            
            **⚙️ Unit Selection Issues:**
            - Refresh page if units don't load
            - Check if unit specifications show
            - Verify unit type matches your hardware
            """ )
        with col_trouble2:
            st.markdown(
            """
            **📊 Results Configuration:**
            - Selections persist across pages
            - Use "Clear All" to reset
            - Check export preview before download
            """)
        
with tab2:
    st.header("🔧 How to Use the External Function in OrcaFlex")
    
    # Overview
    with st.expander("🎯 Overview", expanded=True):
        st.markdown("""
        **The Safelink External Function integrates with OrcaFlex to provide:**
        
        - **Advanced heave compensation modeling**
        - **Real-time control system simulation**
        - **Customizable result outputs**
        - **Professional-grade accuracy**
        
        **Prerequisites:**
        - OrcaFlex license with external function support
        - Safelink external function DLL
        - Configuration file from this web tool
        """)
    
    # Installation
    st.markdown("## 📥 Installation & Setup")
    
    with st.container():
        st.markdown("### Step 1: Install External Function")
        
        col_install1, col_install2 = st.columns([2, 1])
        
        with col_install1:
            st.markdown("""
            1. **Download Components:**
               - Get Safelink external function DLL
               - Obtain function documentation
               - Download example models
            
            2. **Install DLL:**
               - Copy DLL to OrcaFlex installation directory
               - Usually: `C:\\Program Files\\Orcina\\OrcaFlex\\ExternalFunctions\\`
               - Or use project-specific location
            
            3. **Verify Installation:**
               - Start OrcaFlex
               - Check External Functions menu
               - Verify Safelink function appears
            
            **📁 Required Files:**
            - `main.py` - "main" function
            - `support_functions` folder - support functions
            - `config.ini` - Your configuration (from web tool)
            """)
        
        with col_install2:
            st.info("""
            **💡 Note:**
            
            Contact autodept@safelink.no for:
            - DLL files
            - Installation support
            - License information
            """)
    
# Footer
st.markdown("---")

col_footer1, col_footer2, col_footer3 = st.columns([1, 1, 1])

with col_footer1:
    st.markdown("""
    **Info:**
    - Documentation Version: 1.0
    - Last Updated: July 2025
    - Author: Safelink AS
    """)

with col_footer2:
    st.markdown("""
    **🔗 Quick Links:**
    - [Safelink Website](https://safelink.no)
    - [OrcaFlex Documentation](https://orcina.com)
    - [Support Portal](https://support.safelink.no)
    """)

with col_footer3:
    st.markdown("""
    **📞 Contact:**
    - **Email:** post@safelink.no
    - **Phone:** +47 xxx xxx xxx
    - **Address:** Safelink AS, Norway
    """)

# Navigation back to main app
st.divider()
st.markdown("### 🧭 Navigation")
col_nav_final1, col_nav_final2, col_nav_final3, col_nav_final4 = st.columns(4)

with col_nav_final1:
    st.page_link("pages/page_welcome.py", label="🏠 Welcome")
with col_nav_final2:
    st.page_link("pages/page_unit.py", label="⚙️ Unit Configuration")
with col_nav_final3:
    st.page_link("pages/page_results.py", label="📊 Results Selection")
with col_nav_final4:
    st.page_link("pages/page_export.py", label="📤 Export Configuration")