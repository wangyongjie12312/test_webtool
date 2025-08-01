import streamlit as st
from PIL import Image
import pandas as pd
import os


def auto_save_param(param_name):
    """Auto-save parameter when it changes"""
    if param_name in st.session_state:
        st.session_state[f"saved_{param_name}"] = st.session_state[param_name]
        
# page content
st.markdown("# Unit Selection and Configuration")
st.divider()

# Import safelink units from Excel file
@st.cache_data
def load_unit_data():
    """Load and process unit data from Excel file"""
    try:
        df = pd.read_excel( os.path.join('materials', 'Safelink_units.xlsx'), header=0)
        df.sort_values(by="Unit Type", inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df
    except Exception as e:
        st.error(f"Error loading unit data: {e}")
        return pd.DataFrame()

# Load the data

safelink_units = load_unit_data()
# Categorize units based on actual data
iahc_units = safelink_units[safelink_units['Unit Type'].str.contains('IAHC', case=False, na=False)]
poseidon_units = safelink_units[safelink_units['Unit Type'].str.contains('Poseidon', case=False, na=False)]
other_units = safelink_units[~safelink_units['Unit Type'].str.contains('IAHC|Poseidon', case=False, na=False)]

# Create unit lists with tuples (Unit Type, Unit ID) - WITHOUT "None" options
IAHC_units = [unit for unit in zip(iahc_units['Unit Type'].tolist(), iahc_units['Unit ID'].tolist())]
PHC_units = [unit for unit in zip(poseidon_units['Unit Type'].tolist(), poseidon_units['Unit ID'].tolist())]
shock_absorber_units = [unit for unit in zip(other_units['Unit Type'].tolist(), other_units['Unit ID'].tolist())]

# Create a lookup dictionary for unit specifications
unit_specs_lookup = {}
for _, row in safelink_units.iterrows():
    unit_specs_lookup[row['Unit ID']] = {
        'stroke': f"{row['stroke [m]']} m",
        'overall_size': row['overall size [L/W/H, m]'],
        'design_pressure': f"{row['design pressure [bar]']} bar",
        'design_water_depth': f"{row['design water depth [m]']} m",
        'gas_volume': f"{row['gas volume [m3 @ atm]']} m³",
        'weight': f"{row['weight [kg]']/1000:.1f} tonnes",  # Convert kg to tonnes
        'SWL': f"{row['SWL [Te]']:.1f} Te", 
        }

# Define default images for each category
default_images = {
    "IAHC": os.path.join('figures', 'ahc.jpg'),
    "PHC":  os.path.join('figures', 'phc.jpg'),
    "Shock absorber": os.path.join('figures', 'shock_absorber.jpg'),
}

def get_unit_image(unit_serial, unit_type):
    """
    Get the appropriate image for the selected unit.
    First tries to load unit-specific image, falls back to default category image.
    """
    
    # Try unit-specific image first
    unit_specific_image = os.path.join('figures', f"{unit_serial}.jpg" )
    
    # Check if unit-specific image exists
    if os.path.exists(unit_specific_image):
        return unit_specific_image
    else:
        # Always fall back to default category image if unit-specific doesn't exist
        return default_images.get(unit_type, os.path.join('figures', 'ahc.jpg'))

# Find current selection index based on session state
def get_selection_index(units_list, session_unit):
    for i, unit in enumerate(units_list):
        if isinstance(unit, tuple) and unit[1] == session_unit[1]:  # Compare Unit IDs
            return i

# Determine which category the currently selected unit belongs to
def get_unit_type(session_unit):
    if session_unit and isinstance(session_unit, tuple):
        if any("IAHC" in unit[0] for unit in IAHC_units if isinstance(unit, tuple) and unit[1] == session_unit[1]):
            return "IAHC"
        elif any("Poseidon" in unit[0] for unit in PHC_units if isinstance(unit, tuple) and unit[1] == session_unit[1]):
            return "PHC"
        else:
            return "Shock absorber"
    # If no unit selected, default to the first available category
    if IAHC_units:
        return "IAHC"
    elif PHC_units:
        return "PHC"
    elif shock_absorber_units:
        return "Shock absorber"
    else:
        return "IAHC"  # Final fallback

# Check if selected unit supports special features
def get_unit_capabilities(selected_unit, unit_type):
    """Determine which special features are available for the selected unit"""
    if not selected_unit:
        return {"ahc": False, "quick_lifting": False, "constant_tension": False, "rod_lock": False, "rod_orientation": True}
    # IAHC units support all features including rod functions
    if unit_type == "IAHC":
        return {"ahc": True, "quick_lifting": True, "constant_tension": True, "rod_lock": True, "rod_orientation": True}
    # PHC units support most features including rod functions
    elif unit_type == "PHC":
        return {"ahc": False, "quick_lifting": True, "constant_tension": True, "rod_lock": True, "rod_orientation": True}
    # Shock absorber units support basic features
    elif unit_type == "Shock absorber":
        return {"ahc": False, "quick_lifting": True, "constant_tension": False, "rod_lock": True, "rod_orientation": True}
    # Other units have minimal features
    else:
        return {"ahc": False, "quick_lifting": False, "constant_tension": False, "rod_lock": False, "rod_orientation": False}

# Initialize session state with first available unit if none selected
if 'selected_unit' not in st.session_state or st.session_state['selected_unit'] == "None" or st.session_state['selected_unit'] is None:
    if IAHC_units:
        st.session_state.selected_unit = IAHC_units[0]
        st.session_state.selected_unit_type = "IAHC"
    elif PHC_units:
        st.session_state.selected_unit = PHC_units[0]
        st.session_state.selected_unit_type = "PHC"
    elif shock_absorber_units:
        st.session_state.selected_unit = shock_absorber_units[0]
        st.session_state.selected_unit_type = "Shock absorber"

# Initialize session state variables with defaults
session_defaults = {
    # Existing features
    'check_box_constant_tension': False,
    'tension_start_time': 5.0,
    'tension_tolerance': 5.0,
    'check_box_quicklifting': False,
    'quick_start_time': 10.0,
    'quick_acceleration_limit': 0.5,
    'check_box_active_heave_compensation': False,
    'heave_start_time': 15.0,
    'max_stroke_speed': 2.0,
    'motion_reference': 'Onboard',
    # New rod functions
    'check_box_rod_lock': False,
    'rod_lock_depth': 10.0,
    'rod_lock_operation': 'Lifting Down',
    'rod_lock_mode': 'Auto Lock at Depth',
    'lock_hold_time': 5.0,
    'lock_speed': 0.5,
    'rod_orientation': 'Rod Down (Standard)',
    'rod_up_max_extension': 10.0,
    'rod_up_safety_factor': 2.0,
    'rod_down_max_extension': 10.0,
    'rod_down_compensation': True,
    'compensation_factor': 1.0,
    # System integration
    'combined_lock_tension': False,
    'safety_interlocks': True,
    'rod_position_monitoring': True,
    'monitoring_frequency': '10 Hz',
    # Parameters
    'number_1_0': 1.0, 'number_2_0': 100.0, 'number_3_0': 2.0, 'number_4_0': 50.0, 'number_5_0': 0.5,
    'number_6_0': 10.0, 'number_7_0': 3.0, 'number_8_0': 4.0, 'number_9_0': 1.5, 'number_10_0': 2.5,
    'number_1_1': 5.0, 'number_2_1': 200.0, 'number_3_1': 15.0, 'number_4_1': 25.0, 'number_5_1': 0.8,
    'number_6_1': 20.0, 'number_7_1': 6.0, 'number_8_1': 8.0, 'number_9_1': 3.0, 'number_10_1': 5.0
}

# Initialize session state with defaults
for key, default_value in session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = default_value

# Set the selectbox to show the category of the currently selected unit
current_type = get_unit_type(st.session_state['selected_unit'])
category_index = ["IAHC", "PHC", "Shock absorber"].index(current_type)

# Unit formatter function
def format_unit_display(unit):
    if isinstance(unit, tuple) and len(unit) == 2:
        unit_type, unit_id = unit
        return f"{unit_type:<30} │ {unit_id}"
    else:
        return str(unit)

def get_unit_specifications(unit_data):
    """Get specifications for the selected unit from Excel data"""
    if not unit_data or not isinstance(unit_data, tuple):
        return None
    
    unit_type_name, unit_id = unit_data
    
    # Look up specifications from the loaded Excel data
    return unit_specs_lookup[unit_id]

st.markdown("### 1. Unit Selection")
st.markdown("Select the unit to be used in your lifting simulations/operations.")
st.write("Contact [Safelink AS]() and consult  [help documentation](http://safelink.no) for detailed unit specifications.")
col1, col2, col3 = st.columns([2, 1, 2])
with col1:
    selection_box_unit_type = st.selectbox("IAHC", options=["IAHC", "PHC", "Shock absorber"], key="unit_selectbox", index=category_index)
    
    unit_config = {
        "IAHC": {"units": IAHC_units, "key": "iahc_selectbox", "spacing": True},
        "PHC": {"units": PHC_units, "key": "phc_selectbox", "spacing": False},
        "Shock absorber": {"units": shock_absorber_units, "key": "shock_selectbox", "spacing": True}
    }
    
    config = unit_config[selection_box_unit_type]
    current_index = get_selection_index(config["units"], st.session_state['selected_unit'])
    
    selected_unit_serial = st.radio("", 
                                options=config["units"], 
                                format_func=format_unit_display,
                                key=config["key"], 
                                index=current_index,
                                )
    
    # Update session state only if selection changed
    if selected_unit_serial != st.session_state['selected_unit']:
        st.session_state.selected_unit = selected_unit_serial
        st.session_state.selected_unit_type = selection_box_unit_type
        
    # Add spacing for specific unit types
    if config["spacing"]:
            st.markdown("<br>"*11, unsafe_allow_html=True)
            
with col2:
    specs = get_unit_specifications(st.session_state.selected_unit)
    
    st.markdown("<br>"*1, unsafe_allow_html=True)
    if specs:
        # Create specifications dataframe
        specs_data = {
            "Unit Specification": [
                "Stroke",
                "Overall Size (L/W/H)", 
                "Design Pressure",
                "Design Water Depth",
                "Gas Volume", 
                "Weight",
                "SWL"
            ],
            "Value": [
                specs["stroke"],
                specs["overall_size"],
                specs["design_pressure"], 
                specs["design_water_depth"],
                specs["gas_volume"],
                specs["weight"],
                specs["SWL"],
            ]
        }
        
        specs_df = pd.DataFrame(specs_data)
        
        # Display the dataframe with custom configuration
        st.dataframe(
            specs_df,
            use_container_width=True,
            hide_index=True,
            height = 400,
            column_config={
                "Specification": st.column_config.TextColumn(
                    "Specification",
                    help="Technical specification parameter",
                    width="medium",
                ),
                "Value": st.column_config.TextColumn(
                    "Value", 
                    help="Specification value for selected unit",
                    width="medium",
                )
            }
        )
    
with col3:
    _, col_unit_2,_ = st.columns([2,3,2])
    with col_unit_2:
        # Photo of Safelink unit in operation
        st.markdown("<br>"*2, unsafe_allow_html=True)
        
        # Use session state for consistent image display
        display_unit_type = st.session_state['selected_unit_type']
        display_unit_serial = st.session_state['selected_unit']
        
        image_path = get_unit_image(display_unit_serial, display_unit_type)
        try: 
            image = Image.open(image_path)
            st.image(image, use_container_width=True)
            
        except Exception as e:
            fallback_path = os.path.join('figures', 'ahc.jpg')
            try:
                fallback_image = Image.open(fallback_path)
                st.image(fallback_image, use_container_width=True)
            except:
                st.warning("Image not found")


#%% System Parameters and User Inputs
st.divider()

col_1, col_2 = st.columns([3,2])
with col_1:
    st.markdown("### 2. Unit configurations")
    st.write("See [help documentation](http://safelink.no) for detailed explanation of parameters and settings.")
with col_2:
    try:
        image_certificate = Image.open(os.path.join('figures', 'Safelink_Tablet_red.jpg'))
        _, col2,_ = st.columns([2,3,2])
        with col2:
            st.markdown("<br>"*1, unsafe_allow_html=True)
            st.image(image_certificate,use_container_width=True)
    except:
        st.info("Certificate image not found")
# Special Functionalities Section with Rod Functions

# Check what features are available for current unit
unit_capabilities = st.session_state.unit_capabilities = get_unit_capabilities(st.session_state.selected_unit, st.session_state.selected_unit_type)

# Define callback functions for immediate state updates
def update_constant_tension():
    pass
def update_tension_params():
    pass
def update_quick_lifting():
    pass
def update_quick_params():
    pass
def update_active_heave():
    pass
def update_heave_params():
    pass
def update_rod_lock():
    pass
def update_rod_lock_params():
    pass
def update_rod_orientation():
    pass

if any(unit_capabilities.values()):
    current_unit_type = st.session_state['selected_unit_type']    
    # Create tabs for better organization with more features
    tab1, tab2 = st.tabs([ "Control Modes", "System Settings"])
    
    with tab1:
        # Create three columns for the control features
        col_func1, col_func2, col_func3, col_func4 = st.columns(4)
        
        # Quick Lifting Mode
        with col_func1:
            if unit_capabilities["quick_lifting"]:
                quick_lifting = st.checkbox(
                    "#### ⚡ Quick Lifting Mode", 
                    value=st.session_state.check_box_quicklifting, 
                    help="Enables faster payload lifting speed",
                    on_change=update_quick_lifting
                )
                st.session_state.check_box_quicklifting = quick_lifting
                
                if quick_lifting:
                    with st.expander("Quick Lifting Settings", expanded=True):
                        quick_start_time = st.number_input(
                            "Start Time [s]",
                            min_value=0.0,
                            max_value=60.0,
                            value=st.session_state.quick_start_time,
                            step=0.5,
                            on_change=update_quick_params
                        )
                        st.session_state.quick_start_time = quick_start_time
                        
                        quick_acceleration_limit = st.number_input(
                            "Max Acceleration [m/s²]",
                            min_value=0.1,
                            max_value=2.0,
                            value=st.session_state.quick_acceleration_limit,
                            step=0.05,
                            on_change=update_quick_params
                        )
                        st.session_state.quick_acceleration_limit = quick_acceleration_limit
        # Constant Tension Mode
        with col_func2:
            if unit_capabilities["constant_tension"]:
                constant_tension = st.checkbox(
                    "#### 🎯 Constant Tension Mode", 
                    value=st.session_state.check_box_constant_tension, 
                    help="Maintains steady tension force automatically",
                    on_change=update_constant_tension
                )
                st.session_state.check_box_constant_tension = constant_tension
                
                if constant_tension:
                    with st.expander("Constant Tension Settings", expanded=True):
                        tension_start_time = st.number_input(
                            "Start Time [s]",
                            min_value=0.0,
                            max_value=60.0,
                            value=st.session_state.tension_start_time,
                            step=0.5,
                            on_change=update_tension_params
                        )
                        st.session_state.tension_start_time = tension_start_time
                        
                        tension_tolerance = st.number_input(
                            "Tolerance [Te]",
                            min_value=1.0,
                            max_value=20.0,
                            value=st.session_state.tension_tolerance,
                            step=0.5,
                            on_change=update_tension_params
                        )
                        st.session_state.tension_tolerance = tension_tolerance
        
        with col_func3:
            # rod lock unlock
            if unit_capabilities["rod_lock"]:
                
                rod_lock_enabled = st.checkbox(
                    "##### 🔒 Rod Lock/ Unlock", 
                    value=st.session_state.check_box_rod_lock,
                    help="Automatically locks/unlocks rod at specified depth during lifting operations",
                    on_change=update_rod_lock
                )
                st.session_state.check_box_rod_lock = rod_lock_enabled
                
                if rod_lock_enabled:
                    # Lock depth
                    rod_lock_depth = st.number_input(
                        "Lock/Unlock Depth [m]",
                        min_value=0.0,
                        max_value=3000.0,
                        value=st.session_state.rod_lock_depth,
                        step=1.0,
                        help="Depth at which rod lock/unlock operation occurs",
                        on_change=update_rod_lock_params
                    )
                    st.session_state.rod_lock_depth = rod_lock_depth
                    
                    # Lock operation during lifting
                    rod_lock_operation = st.selectbox(
                        "Lock Operation During:",
                        options=["Lifting Down", "Lifting Up", "Both Directions"],
                        index=["Lifting Down", "Lifting Up", "Both Directions"].index(st.session_state.rod_lock_operation),
                        help="When the rod lock/unlock should activate during lifting operations",
                        on_change=update_rod_lock_params
                    )
                    st.session_state.rod_lock_operation = rod_lock_operation
                    
                    # Lock mode
                    rod_lock_mode = st.radio(
                        "Lock Mode:",
                        options=["Auto Lock at Depth", "Auto Unlock at Depth"],
                        index=["Auto Lock at Depth", "Auto Unlock at Depth"].index(st.session_state.rod_lock_mode),
                        help="How the rod lock mechanism should operate",
                        on_change=update_rod_lock_params
                    )
                    st.session_state.rod_lock_mode = rod_lock_mode
                    
                    # Additional parameters for auto modes
                    if rod_lock_mode in ["Auto Lock at Depth", "Auto Unlock at Depth"]:
                        col_lock1, col_lock2 = st.columns(2)
                        
                        with col_lock1:
                            lock_hold_time = st.number_input(
                                "Hold Time [s]",
                                min_value=1.0,
                                max_value=30.0,
                                value=st.session_state.lock_hold_time,
                                step=1.0,
                                help="Time to hold lock/unlock position",
                                on_change=update_rod_lock_params
                            )
                            st.session_state.lock_hold_time = lock_hold_time
                        
                        with col_lock2:
                            lock_speed = st.number_input(
                                "Lock Speed [m/s]",
                                min_value=0.1,
                                max_value=2.0,
                                value=st.session_state.lock_speed,
                                step=0.1,
                                help="Speed of lock/unlock operation",
                                on_change=update_rod_lock_params
                            )
                            st.session_state.lock_speed = lock_speed
                    
                    # Visual indicator
                    if rod_lock_mode == "Auto Lock at Depth":
                        st.success(f"🔒 Rod will automatically LOCK at {rod_lock_depth}m depth during {rod_lock_operation.lower()}")
                    elif rod_lock_mode == "Auto Unlock at Depth":
                        st.info(f"🔓 Rod will automatically UNLOCK at {rod_lock_depth}m depth during {rod_lock_operation.lower()}")
                    else:
                        st.warning(f"🎛️ Rod lock will be manually controlled at {rod_lock_depth}m depth")
                        
        # Active Heave Compensation
        with col_func4:
            if unit_capabilities["ahc"]:
                active_heave = st.checkbox(
                    "#### 🌊 Active Heave Compensation (AHC)", 
                    value=st.session_state.check_box_active_heave_compensation, 
                    help="Counteracts vessel heave motion automatically",
                    on_change=update_active_heave
                )
                st.session_state.check_box_active_heave_compensation = active_heave 
                
                if active_heave:
                    with st.expander("⚙️ AHC Parameters", expanded=True):
                        heave_start_time = st.number_input(
                            "Start Time [s]",
                            min_value=0.0,
                            max_value=60.0,
                            value=st.session_state.heave_start_time,
                            step=0.5,
                            on_change=update_heave_params
                        )
                        st.session_state.heave_start_time = heave_start_time
                        
                        max_stroke_speed = st.number_input(
                            "Max Stroke Speed [m/s]",
                            min_value=0.5,
                            max_value=5.0,
                            value=st.session_state.max_stroke_speed,
                            step=0.1,
                            on_change=update_heave_params
                        )
                        st.session_state.max_stroke_speed = max_stroke_speed
                        
                        motion_reference = st.selectbox(
                            "MRU Source",
                            options=["Onboard", "External"],
                            index=["Onboard", "External"].index(st.session_state.motion_reference),
                            disabled=not active_heave
                        )
                        st.session_state.motion_reference = motion_reference
    
    
    with tab2:
        # Rod Orientation Mode
        if unit_capabilities["rod_orientation"]:
            rod_orientation = st.radio(
                "↕️ Rod Orientation",
                options=["Rod Down (Standard)", "Rod Up (Inverted)"],
                index=["Rod Down (Standard)", "Rod Up (Inverted)"].index(st.session_state.rod_orientation),
                help="Select the physical orientation of the unit for lifting operation",
                on_change=update_rod_orientation
            )
            st.session_state.rod_orientation = rod_orientation
        

else:
    # No special features available
    current_unit_type = st.session_state.selected_unit_type
    st.warning(f"⚠️ **{current_unit_type} units** do not support special control features.")
    
    st.markdown("### 💡 Feature Availability by Unit Type")
    
    col_avail1, col_avail2, col_avail3 = st.columns([1, 1, 1])
    
    with col_avail1:
        st.markdown("#### IAHC Units")
        st.success("✅ Constant Tension Mode")
        st.success("✅ Active Heave Compensation")
        st.success("✅ Quick Lifting Mode")
        st.success("✅ Rod Lock/Unlock Mode")
        st.success("✅ Rod Orientation Control")
    
    with col_avail2:
        st.markdown("#### PHC Units")
        st.success("✅ Constant Tension Mode")
        st.warning("❌ Active Heave Compensation")
        st.success("✅ Quick Lifting Mode")
        st.success("✅ Rod Lock/Unlock Mode")
        st.success("✅ Rod Orientation Control")
    
    with col_avail3:
        st.markdown("#### Other Units")
        st.warning("❌ Constant Tension Mode")
        st.warning("❌ Active Heave Compensation")
        st.success("✅ Quick Lifting Mode")
        st.warning("❌ Rod Lock/Unlock Mode")
        st.success("✅ Rod Orientation Control")
    
    if not safelink_units.empty:
        st.markdown("### 📋 Available Units by Type")
        col_units1, col_units2, col_units3 = st.columns([1, 1, 1])
        
        with col_units1:
            if len(iahc_units) > 0:
                st.markdown("##### IAHC Units Available:")
                for _, unit in iahc_units.iterrows():
                    st.write(f"• {unit['Unit Type']}")
            else:
                st.info("No IAHC units available")
        
        with col_units2:
            if len(poseidon_units) > 0:
                st.markdown(f"##### PHC Units Available ({len(poseidon_units)}):")
                # Show first few, then indicate more
                for i, (_, unit) in enumerate(poseidon_units.iterrows()):
                    if i < 3:
                        st.write(f"• {unit['Unit Type']}")
                    elif i == 3:
                        st.write(f"• ... and {len(poseidon_units) - 3} more")
                        break
            else:
                st.info("No PHC units available")
        
        with col_units3:
            if len(other_units) > 0:
                st.markdown("##### Other Units Available:")
                for _, unit in other_units.iterrows():
                    st.write(f"• {unit['Unit Type']}")
            else:
                st.info("No other units available")
                
#%% parameters
st.divider()
# st.markdown("<br>"*1, unsafe_allow_html=True)
st.markdown('### 3. Parameter Inputs')
# Parameters section with callbacks
with st.expander('Expand to view & edit'):
    left_col, right_col = st.columns(2)
    
    # Define parameter update callbacks
    def update_unit_params():
        """Force immediate update for unit parameters"""
        pass
        
    def update_payload_params():
        """Force immediate update for payload parameters"""
        pass
        
    with left_col:
        st.markdown("#### Unit Parameters")
        col1, col2 = st.columns([1,2])
        with col1:
            number_1_0 = st.number_input("Number_1_0", min_value=0.0, max_value=10.0, value=st.session_state['saved_number_1_0'], step=0.1,key = "number_1_0", on_change=auto_save_param, args=("number_1_0",))
            number_2_0 = st.number_input("Number_2_0", min_value=0.0, max_value=1000.0, value=st.session_state['saved_number_2_0'], step=0.1,key = "number_2_0", on_change=auto_save_param, args=("number_2_0",))
            number_3_0 = st.number_input("Number_3_0", min_value=0.0, max_value=10.0, value=st.session_state['saved_number_3_0'], step=0.1,key = "number_3_0", on_change=auto_save_param, args=("number_3_0",))
            number_4_0 = st.number_input("Number_4_0", min_value=0.0, max_value=10.0, value=st.session_state['saved_number_4_0'], step=0.1,key = "number_4_0", on_change=auto_save_param, args=("number_4_0",))
            number_5_0 = st.number_input("Number_5_0", min_value=0.0, max_value=10.0, value=st.session_state['saved_number_5_0'], step=0.1,key = "number_5_0", on_change=auto_save_param, args=("number_5_0",))
            number_6_0 = st.number_input("Number_6_0", min_value=0.0, max_value=10.0, value=st.session_state['saved_number_6_0'], step=0.1,key = "number_6_0", on_change=auto_save_param, args=("number_6_0",))
            number_7_0 = st.number_input("Number_7_0", min_value=0.0, max_value=10.0, value=st.session_state['saved_number_7_0'], step=0.1,key = "number_7_0", on_change=auto_save_param, args=("number_7_0",))
            number_8_0 = st.number_input("Number_8_0", min_value=0.0, max_value=10.0, value=st.session_state['saved_number_8_0'], step=0.1,key = "number_8_0", on_change=auto_save_param, args=("number_8_0",))
            number_9_0 = st.number_input("Number_9_0", min_value=0.0, max_value=10.0, value=st.session_state['saved_number_9_0'], step=0.1,key = "number_9_0", on_change=auto_save_param, args=("number_9_0",))
            number_10_0 = st.number_input("Number_10_0", min_value=0.0, max_value=10.0, value=st.session_state['saved_number_10_0'], step=0.1,key = "number_10_0", on_change=auto_save_param, args=("number_10_0",))

        
        with col2:
            st.write("")
            st.write("")
            st.write(r"$[m]$ Equilibrium stroke position")
            st.write("")
            st.write("")
            st.write("")
            st.write(r"[Te] Force parameter")
            st.write("")
            st.write("")
            st.write("")
            st.write(r"$[m]$ Mass parameter")
            st.write("")
            st.write("")
            st.write("")
            st.write(r"[Te] Force parameter 2")
            st.write("")
            st.write("")
            st.write("")
            st.write(r"$[m^2]$ Cross-sectional area")
            st.write("")
            st.write("")
            st.write(r"$[m^3]$ Gas volume")
            st.write("")
            st.write("")
            st.write("")
            st.write(r"$[m]$ Length parameter 1")
            st.write("")
            st.write("")
            st.write(r"$[m]$ Length parameter 2")
            st.write("")
            st.write("")
            st.write(r"$[m]$ Length parameter 3")
            st.write("")
            st.write("")
            st.write("")
            st.write(r"$[m]$ Length parameter 4")

    with right_col:
        st.markdown("#### Payload Parameters")
        col1, col2 = st.columns([1,2])
        with col1:
            number_1_1 = st.number_input("Number_1_1", min_value=0.0, max_value=10.0, value=st.session_state['saved_number_1_1'], step=0.1,key = "number_1_1", on_change=auto_save_param, args=("number_1_1",))
            number_2_1 = st.number_input("Number_2_1", min_value=0.0, max_value=1000.0, value=st.session_state['saved_number_2_1'], step=0.1,key = "number_2_1", on_change=auto_save_param, args=("number_2_1",))
            number_3_1 = st.number_input("Number_3_1", min_value=0.0, max_value=10.0, value=st.session_state['saved_number_3_1'], step=0.1,key = "number_3_1", on_change=auto_save_param, args=("number_3_1",))
            number_4_1 = st.number_input("Number_4_1", min_value=0.0, max_value=10.0, value=st.session_state['saved_number_4_1'], step=0.1,key = "number_4_1", on_change=auto_save_param, args=("number_4_1",))
            number_5_1 = st.number_input("Number_5_1", min_value=0.0, max_value=10.0, value=st.session_state['saved_number_5_1'], step=0.1,key = "number_5_1", on_change=auto_save_param, args=("number_5_1",))
            number_6_1 = st.number_input("Number_6_1", min_value=0.0, max_value=10.0, value=st.session_state['saved_number_6_1'], step=0.1,key = "number_6_1", on_change=auto_save_param, args=("number_6_1",))
            number_7_1 = st.number_input("Number_7_1", min_value=0.0, max_value=10.0, value=st.session_state['saved_number_7_1'], step=0.1,key = "number_7_1", on_change=auto_save_param, args=("number_7_1",))
            number_8_1 = st.number_input("Number_8_1", min_value=0.0, max_value=10.0, value=st.session_state['saved_number_8_1'], step=0.1,key = "number_8_1", on_change=auto_save_param, args=("number_8_1",))
            number_9_1 = st.number_input("Number_9_1", min_value=0.0, max_value=10.0, value=st.session_state['saved_number_9_1'], step=0.1,key = "number_9_1", on_change=auto_save_param, args=("number_9_1",))
            number_10_1 = st.number_input("Number_10_1", min_value=0.0, max_value=10.0, value=st.session_state['saved_number_10_1'], step=0.1,key = "number_10_1", on_change=auto_save_param, args=("number_10_1",))
            
        
        with col2:
            st.write("")
            st.write("")
            st.write(r"$[m]$ Available lifting height")
            st.write("")
            st.write("")
            st.write("")
            st.write(r"[Te] Payload weight in air" )
            st.write("")
            st.write("")
            st.write(r"[Te] Total weight of slings between rod and payload")
            st.write("")
            st.write("")
            st.write("")
            st.write(r"[Te] Parameter 4")
            st.write("")
            st.write("")
            st.write("")
            st.write(r"$[m^2]$ Cross-sectional area")
            st.write("")
            st.write("")
            st.write(r"$[m^3]$ Volume parameter")
            st.write("")
            st.write("")
            st.write("")
            st.write(r"$[m]$ Length parameter 1")
            st.write("")
            st.write("")
            st.write("")
            st.write(r"$[m]$ Length parameter 2")
            st.write("")
            st.write("")
            st.write(r"$[m]$ Length parameter 3")
            st.write("")
            st.write("")
            st.write("")
            st.write(r"$[m]$ Length parameter 4")

# Navigation to next page
col_next_1, col_next_2, col_next_3 = st.columns([1, 1, 1])
with col_next_2:
    # Always enabled since there's always a unit selected
    st.markdown("<br>"*2, unsafe_allow_html=True)
    if st.button("Proceed to Select Results →", use_container_width=True, type="primary", help="Continue to results page"):
        st.switch_page("pages/page_results.py")


# for i in range(1,11):
#     st.markdown("---")
#     st.session_state[f'number_{i}_0']
#     st.session_state[f'number_{i}_1']