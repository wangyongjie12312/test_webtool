import streamlit as st
from PIL import Image
import os 

#%% set up the page configuration
st.set_page_config(
    page_title="Safelink OrcaFlex Configuration Tool",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Define a colored border style (e.g., blue border)
box_style = """
    <div style="
        border: 2px solid #1f77b4;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        background-color: #f9f9f9;
    ">
"""

# Initialize session state variables for authentication
st.session_state.setdefault('logged_in', False)
st.session_state.setdefault('username', '')
st.session_state.setdefault('show_login_dialog', True)
# st.session_state.setdefault('last_activity', str(datetime.now()))

# is_demo_user = st.session_state.usesrname == "demo"

def handle_login(username, password):
    """Handle user authentication"""
    # Simple authentication - in production, use proper authentication
    valid_users = {
        "admin": "password123",
        "user": "user123",
        "demo": "demo",
        "safelink": "safelink2025"
    }
    
    if username in valid_users and valid_users[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.show_login_dialog = False
        return True
    return False

def handle_logout():
    """Handle user logout"""
    st.session_state.logged_in = False
    st.session_state.username = ''
    st.session_state.show_login_dialog = True
    st.rerun()

def show_login_screen():
    """Display the login screen"""
    # Safelink logo
    try:
        image = Image.open(os.path.join('figures', 'SafelinkTabWiFi.png'))
        _, col2,_ = st.columns([1, 1, 1])
        with col2:
            st.image(image, width=800)
    except:
        st.title("🔧 Safelink OrcaFlex Configuration Tool")
    
    st.divider()
    
    # Login form
    _, col_login2, _ = st.columns([1, 2, 1])
    with col_login2:
        st.markdown("### 🔐 Authentication Required")
        st.markdown("Please login to access the Safelink OrcaFlex External Function Configuration Tool")
        
        with st.form("login_form"):
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            
            col_btn1, col_btn2 = st.columns([1, 1])
            with col_btn1:
                login_submitted = st.form_submit_button("🚀 Login", use_container_width=True, type="primary")
            with col_btn2:
                demo_submitted = st.form_submit_button("🎯 Demo Login", use_container_width=True)
            
            if login_submitted:
                if username and password:
                    if handle_login(username, password):
                        st.success(f"✅ Welcome, {username}!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
                else:
                    st.warning("⚠️ Please enter both username and password")
            
            if demo_submitted:
                if handle_login("demo", "demo"):
                    st.success("✅ Demo login successful!")
                    st.balloons()
                    st.rerun()
        
        # Demo credentials info
        with st.expander("🔍 View Demo Credentials"):
            st.info("""
            **Demo Account (Quick Access):**
            - Username: `demo`
            - Password: `demo`
            
            **Other Test Accounts:**
            - Username: `admin` / Password: `password123`
            - Username: `user` / Password: `user123`
            - Username: `safelink` / Password: `safelink2025`
            """)
    
    # Company information (public)
    st.divider()
    col_info1, col_info2 = st.columns([1, 1])
    with col_info1:
        with st.container():
            # st.markdown(box_style, unsafe_allow_html=True)
            st.subheader("About [Safelink](http://safelink.no)")
            st.markdown("""
            - Leading provider of heave compensation systems
            - Advanced marine motion control solutions
            - Professional simulation and configuration tools
            - Trusted by offshore industry professionals
            """)
            st.markdown("</div>", unsafe_allow_html=True)  # Close styled div
        
    with col_info2:
        with st.container():
            st.markdown("""
            #### 📞 Contact Information
            - **Website**: https://safelink.no/
            - **General Inquiries**: post@safelink.no
            - **Simulation Support**: autodept@safelink.no
            """)

def show_main_app():
    """Display the main application with navigation"""
    # Add logout button in sidebar
    with st.sidebar:
        st.markdown(f"**👤 Logged in as:** {st.session_state.username}")
        if st.button("🚪 Logout", use_container_width=True):
            handle_logout()
        st.divider()
    
    # Define pages only when authenticated
    page_welcome = st.Page("pages/page_welcome.py", title="Home", icon="🏠")
    page_unit = st.Page("pages/page_unit.py", title="Configure a Unit", icon="⚙️")
    page_results = st.Page("pages/page_results.py", title="Select Results", icon="📄")
    page_export = st.Page("pages/page_export.py", title="Export Configuration", icon="📤")
    page_help = st.Page("pages/page_help.py", title="Help documentation", icon="📖")

    # Set up navigation
    pg = st.navigation(
        pages=[page_welcome, page_unit, page_results, page_export, page_help],
        # pages=[page_welcome, page_unit, page_system_parameters, page_results, page_export, page_help],
        expanded= False,
        # position="top"
        position="sidebar"
    )

    # In a shared utils file or main page
    def initialize_session_state():
        if 'user_data' not in st.session_state:
            st.session_state.user_data = {}
        if 'current_step' not in st.session_state:
            st.session_state.current_step = 1
        if "counter" not in st.session_state:
            st.session_state.counter = 0
        if 'selected_unit' not in st.session_state:
            st.session_state.selected_unit = None
        if 'selected_unit_type' not in st.session_state:
            st.session_state.selected_unit_type = None
        if 'customized_results' not in st.session_state:
            st.session_state.customized_results = False
        if 'selected_body_results' not in st.session_state:
            st.session_state.selected_body_results = []
        if 'selected_rod_results' not in st.session_state:
            st.session_state.selected_rod_results = []
        if 'selected_payload_results' not in st.session_state:
            st.session_state.selected_payload_results = []
        if 'selected_results' not in st.session_state:
            st.session_state.selected_results = {}
        if 'check_box_quicklifting' not in st.session_state:
            st.session_state.check_box_quicklifting = False
        if 'check_box_constant_tension' not in st.session_state:
            st.session_state.check_box_constant_tension = False
        if 'check_box_active_heave_compensation' not in st.session_state:
            st.session_state.check_box_active_heave_compensation = False
        if 'version' not in st.session_state:
            st.session_state.version = '0.0.1'
        
            # Special function checkboxes
        if 'check_box_constant_tension' not in st.session_state:
            st.session_state.check_box_constant_tension = False
        if 'check_box_quicklifting' not in st.session_state:
            st.session_state.check_box_quicklifting = False
        if 'check_box_active_heave_compensation' not in st.session_state:
            st.session_state.check_box_active_heave_compensation = False
        
        # Special function parameters - constant tension
        if 'tension_start_time' not in st.session_state:
            st.session_state.tension_start_time = 5.0
        if 'tension_tolerance' not in st.session_state:
            st.session_state.tension_tolerance = 5.0
        
        # Special function parameters - quick lifting
        if 'quick_start_time' not in st.session_state:
            st.session_state.quick_start_time = 10.0
        if 'quick_acceleration_limit' not in st.session_state:
            st.session_state.quick_acceleration_limit = 0.8
        if 'unit_capabilities' not in st.session_state:
            st.session_state.unit_capabilities = {"ahc": False, "quick_lifting": False, "constant_tension": False}
        
        # Special function parameters - active heave compensation
        if 'heave_start_time' not in st.session_state:
            st.session_state.heave_start_time = 15.0
        if 'max_stroke_speed' not in st.session_state:
            st.session_state.max_stroke_speed = 2.0
        if 'motion_reference' not in st.session_state:
            st.session_state.motion_reference = 'Onboard'
        
        # Safety parameters
        if 'max_force_limit' not in st.session_state:
            st.session_state.max_force_limit = 2000.0
            
        # unit parameters
        for i in range(1, max_number :=11):
            if f'number_{i}_0' not in st.session_state:
                st.session_state[f'number_{i}_0'] = 0.0 
            if f'number_{i}_1' not in st.session_state:
                st.session_state[f'number_{i}_1'] = 0.0 
            if f'saved_number_{i}_0' not in st.session_state:
                st.session_state[f'saved_number_{i}_0'] = 0.0 
            if f'saved_number_{i}_1' not in st.session_state:
                st.session_state[f'saved_number_{i}_1'] = 0.0 
        
        # unit parameter names
        if 'payload_names' not in st.session_state:
            st.session_state.payload_names = [
                    "Available lifting height",
                    "Payload weight in air",
                    "Sling weight",
                    "Parameter 4",
                    "Cross-sectional area", 
                    "Volume parameter",
                    "Length parameter 1",
                    "Length parameter 2",
                    "Length parameter 3",
                    "Length parameter 4"
                ]
                
        if 'unit_parameter_names' not in st.session_state:
            st.session_state.unit_parameter_names = [
                    "Equilibrium stroke position",
                    "Force parameter", 
                    "Mass parameter",
                    "Force parameter 2",
                    "Cross-sectional area",
                    "Gas volume",
                    "Length parameter 1",
                    "Length parameter 2", 
                    "Length parameter 3",
                    "Length parameter 4"
                ]
                
        if 'payload_parameter_names' not in st.session_state:
            st.session_state.payload_parameter_names = [
                    "Available lifting height",
                    "Payload weight in air",
                    "Sling weight",
                    "Parameter 4",
                    "Cross-sectional area", 
                    "Volume parameter",
                    "Length parameter 1",
                    "Length parameter 2",
                    "Length parameter 3",
                    "Length parameter 4"
                ]
                
        if 'results_manually_cleared' not in st.session_state:
            st.session_state.results_manually_cleared = True
                
    initialize_session_state()
    # Run the selected page
    pg.run()

#%% Main application logic
if not st.session_state.logged_in:
    # Show login screen if not authenticated
    show_login_screen()
else:
    # Show main application if authenticated
    show_main_app()
