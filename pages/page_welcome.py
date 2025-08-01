import streamlit as st
from PIL import Image
import datetime
import os

#%% set up the page configuration
st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed"  # or "auto"
)

# Initialize session state variables
st.session_state.setdefault('image_welcome', True)
st.session_state.setdefault('logged_in', False)
st.session_state.setdefault('username', '')
st.session_state.setdefault('show_login_dialog', False)

def hide_welcome_image():
    st.session_state.image_welcome = False

def show_login_dialog():
    st.session_state.show_login_dialog = True

def hide_login_dialog():
    st.session_state.show_login_dialog = False

def handle_login(username, password):
    # Simple authentication - in production, use proper authentication
    valid_users = {
        "admin": "password123",
        "user": "user123",
        "demo": "demo"
    }
    
    if username in valid_users and valid_users[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.show_login_dialog = False
        st.success(f"Welcome, {username}!")
        st.rerun()
    else:
        st.error("Invalid username or password")

def handle_logout():
    st.session_state.logged_in = False
    st.session_state.username = ''
    st.session_state.show_login_dialog = False
    st.success("Logged out successfully!")
    st.rerun()

# Main page content
image = Image.open( os.path.join('figures', 'Safelink Logo Medium.png'))
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.image(image, width=1000)

#%% Login/Logout section
st.divider()
col_login1, col_login2, col_login3 = st.columns([3, 1, 3])

with col_login2:
    if not st.session_state.logged_in:
        if st.button("🔐 Login", use_container_width=True, type="primary"):
            show_login_dialog()
    else:
        st.success(f"👤 Welcome, {st.session_state.username}")

# Login Dialog
if st.session_state.show_login_dialog and not st.session_state.logged_in:
    with st.container():
        st.markdown("### 🔐 Login to Safelink Configuration Tool")
        
        col_dialog1, col_dialog2, col_dialog3 = st.columns([1, 2, 1])
        with col_dialog2:
            with st.form("login_form"):
                st.markdown("**Please enter your credentials:**")
                username = st.text_input("Username", placeholder="Enter username")
                password = st.text_input("Password", type="password", placeholder="Enter password")
                
                col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
                with col_btn1:
                    login_submitted = st.form_submit_button("Login", use_container_width=True, type="primary")
                with col_btn2:
                    cancel_submitted = st.form_submit_button("Cancel", use_container_width=True)
                with col_btn3:
                    demo_submitted = st.form_submit_button("Demo Login", use_container_width=True)
                
                if login_submitted and username and password:
                    handle_login(username, password)
                
                if cancel_submitted:
                    hide_login_dialog()
                    st.rerun()
                
                if demo_submitted:
                    handle_login("demo", "demo")
            
            # Demo credentials info
            with st.expander("Demo Credentials"):
                st.info("""
                **Demo Account:**
                - Username: demo
                - Password: demo
                
                **Test Accounts:**
                - Username: admin, Password: password123
                - Username: user, Password: user123
                """)

# Only show main content if logged in
if st.session_state.logged_in:
    #%% Main welcome content
    col31, col32, col33 = st.columns([1, 1, 1])
    with col32:
        st.markdown("### Welcome to Safelink OrcaFlex External Function Configuration Tool!")
    col31, col32, col33 = st.columns([1, 1, 1])
    with col32:
        st.markdown("##### Safelink products and solutions: https://safelink.no/")
        st.markdown("Version: 0.1.0")
        st.markdown("Release date: 2025-08-01")
        st.markdown(f"Today is: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")
        st.markdown("General questions and technical sales: post@safelink.no.")
        st.markdown("Technical support of OrcaFlex simulation: autodept@safelink.no.")
    st.divider()
        
    image = Image.open(os.path.join('figures', 'Cover-final0.jpg'))
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.session_state.image_welcome:
            st.image(image, width=1000)
    st.divider()

    # introduction to AHC and PHC
    col1, col2 = st.columns([1, 1])
    st.divider()
    with col1:
        # AHC introduction
        with open("./materials/AHC_introduction.md", "r", encoding="utf-8") as file:
            AHC_introduction = file.read()
        st.markdown(AHC_introduction, unsafe_allow_html=True)
        
        # a AHC photo
        col11, col21, col31 = st.columns([1, 1, 1])
        with col21:
            st.markdown("<br>"*1, unsafe_allow_html=True)
            image = Image.open(os.path.join('figures', 'IAHC 700 undocked 003.png'))
            st.image(image, width=200)
            
    with col2:
        # PHC introduction
        with open("./materials/PHC_introduction.md", "r", encoding="utf-8") as file:
            PHC_introduction = file.read()
        st.markdown(PHC_introduction, unsafe_allow_html=True)
        
        # a PHC photo
        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            st.markdown("<br>"*1, unsafe_allow_html=True)
            image = Image.open(os.path.join('figures', '10.png'))
            st.image(image, width=400)
    
    # Simulation service
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<br>"*1, unsafe_allow_html=True)
        with open("./materials/simulation_service.md", "r", encoding="utf-8") as file:
            simulation_service = file.read()
        st.markdown(simulation_service, unsafe_allow_html=True)
    
    with col2:
        # decorative image
        st.markdown("<br>"*6, unsafe_allow_html=True)
        image = Image.open( os.path.join('figures', 'shutterstock_162848774.jpg'))
        st.image(image, width=270)

    # OrcaFlex simulation image
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        image = Image.open(os.path.join('figures', 'orcaflex_simulation.png'))
        st.image(image, width=1000)
        
    
    #%% Safelink certificates
    st.divider()
    image_certificate = Image.open( os.path.join('figures', 'shutterstock_1904707174.jpg'))
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.image(image_certificate, width=500)    
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("Proceed to Configure a Unit ->", use_container_width=True, type="primary"):
                        st.switch_page("pages/page_unit.py")


else:
    # Show limited content when not logged in
    st.markdown("### 🔒 Please login to access the Safelink Configuration Tool")
    st.info("This tool requires authentication to access unit configurations and system parameters.")
    
    col_info1, col_info2 = st.columns([1, 1])
    with col_info1:
        st.markdown("""
        #### About [Safelink](http://safelink.no)
        - Leading provider of heave compensation systems
        - Advanced marine motion control solutions
        - Professional simulation and configuration tools
        """)
    
    with col_info2:
        st.markdown("""
        #### Contact Information
        - **General**: post@safelink.no
        - **Technical Support**: autodept@safelink.no
        - **Website**: https://safelink.no/
        """)

#%% feature selection share (only if logged in)
if st.session_state.logged_in:
    st.session_state.radio_choice = "Manual"
    