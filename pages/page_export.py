import streamlit as st
import configparser
import io
import pandas as pd

# page content
st.markdown("# Configuration Summary & Export")
st.markdown("Review your configuration and download the file for OrcaFlex.")

st.divider()

def validate_unit_selection():
    """Check if a unit has been selected"""
    return st.session_state.selected_unit is not None

def validate_parameters():
    """Check if all parameters have realistic (non-zero) values"""
    zero_unit_params = []
    zero_payload_params = []
    
    # Check unit parameters (1-10)
    for i in range(1, 11):
        param_value = st.session_state[f'saved_number_{i}_0']
        if param_value == 0:
            param_name = get_unit_parameter_name(i)
            zero_unit_params.append(param_name)
    
    # Check payload parameters (1-10)
    for i in range(1, 11):
        param_value = st.session_state[f'saved_number_{i}_1']
        if param_value == 0:
            param_name = get_payload_parameter_name(i)
            zero_payload_params.append(param_name)
    
    return zero_unit_params, zero_payload_params

def get_unit_parameter_name(index):
    """Get the display name for unit parameter"""
    default_names = [
        "Equilibrium stroke position [m]",
        "Force parameter [Te]", 
        "Mass parameter [m]",
        "Force parameter 2 [Te]",
        "Cross-sectional area [m²]",
        "Gas volume [m³]",
        "Length parameter 1 [m]",
        "Length parameter 2 [m]",
        "Length parameter 3 [m]",
        "Length parameter 4 [m]"
    ]
    
    if 'unit_parameter_names' in st.session_state and index-1 < len(st.session_state.unit_parameter_names):
        return st.session_state.unit_parameter_names[index-1]
    else:
        return default_names[index-1]

def get_payload_parameter_name(index):
    """Get the display name for payload parameter"""
    default_names = [
        "Available lifting height [m]",
        "Payload weight in air [Te]",
        "Weight of slings [Te]",
        "Parameter 4 [Te]",
        "Cross-sectional area [m²]",
        "Volume parameter [m³]",
        "Length parameter 1 [m]",
        "Length parameter 2 [m]",
        "Length parameter 3 [m]",
        "Length parameter 4 [m]"
    ]
    
    if 'payload_parameter_names' in st.session_state and index-1 < len(st.session_state.payload_parameter_names):
        return st.session_state.payload_parameter_names[index-1]
    else:
        return default_names[index-1]

def display_unit_overview():
    """Display the selected unit overview"""
    st.markdown("### Selected unit")
    
    col_overview1, col_overview2 = st.columns([1, 1])
    
    if isinstance(st.session_state.selected_unit, tuple):
        unit_type_display = st.session_state.selected_unit[0]
        unit_id_display = st.session_state.selected_unit[1]
        unit_category = st.session_state.selected_unit_type
        
        with col_overview1:
            st.success(f"**{unit_category}** - {unit_type_display}")
        with col_overview2:
            st.info(f"**Unit ID:** {unit_id_display}")

def display_unit_parameters():
    """Display unit parameters in expandable table"""
    with st.expander("**Unit Parameters**", expanded=False):
        unit_params = []
        
        for i in range(1, 11):
            param_value = st.session_state[f'saved_number_{i}_0']
            param_name = get_unit_parameter_name(i)
            unit_params.append([param_name, f"{param_value}"])
        
        unit_params_df = pd.DataFrame(unit_params, columns=["Parameter", "Value"])
        st.dataframe(unit_params_df, use_container_width=True, hide_index=True, height=450)

def display_payload_parameters():
    """Display payload parameters in expandable table"""
    with st.expander("**Payload Parameters**", expanded=False):
        payload_params = []
        
        for i in range(1, 11):
            param_value = st.session_state[f'saved_number_{i}_1']
            param_name = get_payload_parameter_name(i)
            payload_params.append([param_name, f"{param_value}"])
        
        payload_params_df = pd.DataFrame(payload_params, columns=["Parameter", "Value"])
        st.dataframe(payload_params_df, use_container_width=True, hide_index=True, height=450)

def display_special_functions():
    """Display special functions configuration"""
    with st.expander("**Special Functions**", expanded=False):
        unit_capabilities = st.session_state['unit_capabilities']
        
        if any(unit_capabilities.values()):
            special_function_params = []
            
            # Rod Functions Section
            special_function_params.append(["**Rod Functions**", ""])
            
            # Rod Orientation
            if unit_capabilities["rod_orientation"]:
                rod_orientation = st.session_state.rod_orientation
                special_function_params.append(["Rod Orientation", rod_orientation])
            
            # Rod Lock Parameters
            if st.session_state['check_box_rod_lock'] and unit_capabilities["rod_lock"]:
                special_function_params.extend([
                    ["Rod Lock - Enabled", "Yes"],
                    ["Rod Lock - Depth", f"{st.session_state['rod_lock_depth']} m"],
                    ["Rod Lock - Operation", st.session_state['rod_lock_operation']],
                    ["Rod Lock - Mode", st.session_state['rod_lock_mode']],
                    ["Rod Lock - Hold Time", f"{st.session_state['lock_hold_time']} s"],
                    ["Rod Lock - Speed", f"{st.session_state['lock_speed']} m/s"]
                ])
            elif unit_capabilities["rod_lock"]:
                special_function_params.append(["Rod Lock - Enabled", "No"])
            
            # Control Modes Section
            special_function_params.append(["", ""])
            special_function_params.append(["**Control Modes**", ""])
            
            # Quick Lifting Parameters
            if st.session_state['check_box_quicklifting'] and unit_capabilities["quick_lifting"]:
                special_function_params.extend([
                    ["Quick Lifting - Enabled", "Yes"],
                    ["Quick Lifting - Start Time", f"{st.session_state['quick_start_time']} s"],
                    ["Quick Lifting - Max Acceleration", f"{st.session_state['quick_acceleration_limit']} m/s²"]
                ])
            elif unit_capabilities["quick_lifting"]:
                special_function_params.append(["Quick Lifting - Enabled", "No"])
            
            # Constant Tension Parameters
            if st.session_state['check_box_constant_tension'] and unit_capabilities["constant_tension"]:
                special_function_params.extend([
                    ["Constant Tension - Enabled", "Yes"],
                    ["Constant Tension - Start Time", f"{st.session_state['tension_start_time']} s"],
                    ["Constant Tension - Tolerance", f"{st.session_state['tension_tolerance']} Te"]
                ])
            elif unit_capabilities["constant_tension"]:
                special_function_params.append(["Constant Tension - Enabled", "No"])
            
            # Active Heave Compensation Parameters
            if st.session_state['check_box_active_heave_compensation'] and unit_capabilities["ahc"]:
                special_function_params.extend([
                    ["Heave Comp. - Enabled", "Yes"],
                    ["Heave Comp. - Start Time", f"{st.session_state['heave_start_time']} s"],
                    ["Heave Comp. - Max Stroke Rate", f"{st.session_state['max_stroke_speed']} m/s"],
                    ["Heave Comp. - MRU Source", st.session_state['motion_reference']]
                ])
            elif unit_capabilities["ahc"]:
                special_function_params.append(["Heave Comp. - Enabled", "No"])
            
            # Safety Parameters
            special_function_params.append(["", ""])
            special_function_params.append(["**Safety Parameters**", ""])
            special_function_params.append(["Max Force Limit", f"{st.session_state['max_force_limit']} Te"])
            
            if special_function_params:
                special_df = pd.DataFrame(special_function_params, columns=["Parameter", "Value"])
                st.dataframe(special_df, use_container_width=True, hide_index=True, height=450)
            else:
                st.info("No special functions configured")
        else:
            st.info("No special functions available for this unit type")

def display_selected_results():
    """Display selected results configuration"""
    with st.expander("**Selected Results**", expanded=False):
        customized_results = st.session_state['customized_results']
        
        if customized_results:
            all_results = []
            
            # Body Results
            body_results = st.session_state['selected_body_results']
            if body_results:
                for result in body_results:
                    all_results.append([result, "🔵 Body"])
            
            # Rod Results
            rod_results = st.session_state['selected_rod_results']
            if rod_results:
                if all_results:  # Add spacing if there are already results
                    all_results.append(["", ""])
                for result in rod_results:
                    all_results.append([result, "🟢 Rod"])
            
            # Payload Results
            payload_results = st.session_state['selected_payload_results']
            if payload_results:
                if all_results:  # Add spacing if there are already results
                    all_results.append(["", ""])
                for result in payload_results:
                    all_results.append([result, "🟡 Payload"])
            
            if all_results:
                results_df = pd.DataFrame(all_results, columns=["Result", "Type"])
                st.dataframe(results_df, use_container_width=True, hide_index=True, height=450)
            else:
                st.info("No custom results selected")
        else:
            st.info("🔧 **Using OrcaFlex Default Results**\n\nNo custom results configured")

def generate_config_file():
    """Generate and provide download for configuration file"""
    config = configparser.ConfigParser()
    from datetime import datetime
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    version = st.session_state['version']
    
    # Unit configuration
    config["Unit"] = {
        "category": st.session_state.selected_unit_type,
        "unit_type": st.session_state.selected_unit[0] if isinstance(st.session_state.selected_unit, tuple) else str(st.session_state.selected_unit),
        "unit_id": st.session_state.selected_unit[1] if isinstance(st.session_state.selected_unit, tuple) else str(st.session_state.selected_unit),
    }
    
    # Special functions configuration
    config["Special_Functions"] = {
        "quick_lifting": str(st.session_state.check_box_quicklifting),
        "constant_tension": str(st.session_state.check_box_constant_tension),
        "active_heave_compensation": str(st.session_state.check_box_active_heave_compensation),
        "rod_lock": str(st.session_state.check_box_rod_lock)
    }
    
    # Special function parameters
    config["Function_Parameters"] = {}
    
    # Rod Functions parameters
    config["Function_Parameters"]["rod_orientation"] = str(st.session_state.rod_orientation)
    
    if st.session_state.check_box_rod_lock:
        config["Function_Parameters"]["rod_lock_depth"] = str(st.session_state.rod_lock_depth)
        config["Function_Parameters"]["rod_lock_operation"] = str(st.session_state.rod_lock_operation)
        config["Function_Parameters"]["rod_lock_mode"] = str(st.session_state.rod_lock_mode)
        config["Function_Parameters"]["lock_hold_time"] = str(st.session_state.lock_hold_time)
        config["Function_Parameters"]["lock_speed"] = str(st.session_state.lock_speed)
    
    # Quick lifting parameters
    if st.session_state.check_box_quicklifting:
        config["Function_Parameters"]["quick_start_time"] = str(st.session_state.quick_start_time)
        config["Function_Parameters"]["quick_acceleration_limit"] = str(st.session_state.quick_acceleration_limit)
    
    # Constant tension parameters
    if st.session_state.check_box_constant_tension:
        config["Function_Parameters"]["tension_start_time"] = str(st.session_state.tension_start_time)
        config["Function_Parameters"]["tension_tolerance"] = str(st.session_state.tension_tolerance)
    
    # Active heave compensation parameters
    if st.session_state.check_box_active_heave_compensation:
        config["Function_Parameters"]["heave_start_time"] = str(st.session_state.heave_start_time)
        config["Function_Parameters"]["max_stroke_speed"] = str(st.session_state.max_stroke_speed)
        config["Function_Parameters"]["motion_reference"] = str(st.session_state.motion_reference)
    
    # Safety parameters
    config["Safety_Parameters"] = {
        "max_force_limit": str(st.session_state.max_force_limit),
    }
    
    # Unit parameters
    config["Unit_Parameters"] = {}
    for i in range(1, 11):
        param_value = st.session_state[f'saved_number_{i}_0']
        config["Unit_Parameters"][f"parameter_{i}"] = str(param_value)
    
    # Payload parameters  
    config["Payload_Parameters"] = {}
    for i in range(1, 11):
        param_value = st.session_state[f'saved_number_{i}_1']
        config["Payload_Parameters"][f"parameter_{i}"] = str(param_value)
        
    # Results configuration
    config["Results"] = {
        "customized": str(st.session_state.customized_results),
        "body_results": ", ".join(st.session_state.selected_body_results) if st.session_state.selected_body_results else "None",
        "rod_results": ", ".join(st.session_state.selected_rod_results) if st.session_state.selected_rod_results else "None",
        "payload_results": ", ".join(st.session_state.selected_payload_results) if st.session_state.selected_payload_results else "None",
    }
    
    # Save to in-memory file
    ini_file = io.StringIO()
    
    # Write custom header comments first
    ini_file.write("# External function Configuration File\n")
    ini_file.write("# Generated by Safelink OrcaFlex Configuration Web Tool\n")
    ini_file.write(f"# Version: {version}\n")
    ini_file.write(f"# Datetime: {current_time}\n")
    ini_file.write("# Contact Safelink post@safelink.no if any questions.\n")
    ini_file.write("#\n\n")
    
    # Write the configuration
    config.write(ini_file)
    ini_bytes = ini_file.getvalue().encode("utf-8")
    
    # Generate filename with unit info
    unit_id = st.session_state.selected_unit[1] if isinstance(st.session_state.selected_unit, tuple) else str(st.session_state.selected_unit)
    filename = f"safelink_orcaflex_config_{unit_id}.ini"
    
    st.success("**Configuration Complete** - Ready to download!")
    
    # Download button
    st.download_button(
        label="💾 Download Configuration File",
        data=ini_bytes,
        file_name=filename,
        mime="text/plain",
        use_container_width=True
    )

    st.markdown("#### **Next Steps:**")
    st.markdown("""
    1. **Save** the downloaded .ini file to local folder where the OrcaFlex model is.
    2. **Copy/Move** Safelink OrcaFlex External Function package to the same folder. See [How to implement External Function](). 
    3. **Run** your simulation with the configured parameters. 
    """)

def display_validation_errors(zero_unit_params, zero_payload_params):
    """Display parameter validation error messages"""
    st.error("❌ **Configuration Incomplete** - Some parameters are set to zero.")
    
    if zero_unit_params:
        st.error(f"**Unit Parameters with zero values:** {', '.join(zero_unit_params)}")
    
    if zero_payload_params:
        st.error(f"**Payload Parameters with zero values:** {', '.join(zero_payload_params)}")
    
    st.info("Please go to page: **Configure a unit -> Parameter Inputs** and enter realistic values for all parameters.")

def display_navigation_buttons():
    """Display navigation and session management buttons"""
    st.markdown("---")
    st.markdown("### **Session Management**")

    col_nav1, col_nav2, col_nav3, col_nav4, col_nav5 = st.columns([1, 1, 1, 1, 1])

    with col_nav1:
        if st.button("← ⚙️ **Back to Unit configuration**", use_container_width=True, type="secondary"):
            st.switch_page("pages/page_unit.py")

    with col_nav2:
        if st.button("← 📄 **Back to Select Results**", use_container_width=True, type="secondary"):
            st.switch_page("pages/page_results.py")
            
    with col_nav3:
        if st.button("🔄 **Clear All Settings**", use_container_width=True, type="secondary"):
            # Clear only configuration-related session state, preserve login/auth data
            config_keys_to_clear = [
                'selected_unit', 'selected_unit_type', 'unit_capabilities',
                'customized_results', 'selected_body_results', 'selected_rod_results', 'selected_payload_results',
                'check_box_quicklifting', 'check_box_constant_tension', 'check_box_active_heave_compensation', 'check_box_rod_lock',
                'rod_orientation', 'rod_lock_depth', 'rod_lock_operation', 'rod_lock_mode', 'lock_hold_time', 'lock_speed',
                'quick_start_time', 'quick_acceleration_limit', 'tension_start_time', 'tension_tolerance',
                'heave_start_time', 'max_stroke_speed', 'motion_reference', 'max_force_limit', 'max_stroke_limit',
                'unit_parameter_names', 'payload_parameter_names'
            ]
            
            # Clear unit and payload parameters (saved_number_X_Y)
            for i in range(1, 11):
                config_keys_to_clear.extend([f'saved_number_{i}_0', f'saved_number_{i}_1'])
            
            # Remove only configuration keys, keep login/auth related keys
            for key in config_keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
            
            st.success("✅ **Configuration cleared!** You can now start a new configuration.")
            st.rerun()
            
    with col_nav4:
        if st.button("📖 **Help documentation**", use_container_width=True, type="secondary"):
            st.switch_page("pages/page_help.py")
        
    with col_nav5:
        if st.button("🚪 **Logout & Close**", use_container_width=True, type="secondary"):
            # Clear session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            
            # Show logout confirmation
            st.success("✅ **Logged out successfully!**")
            st.info("💡 **Tip:** You can now close this browser tab or start a new configuration.")
            
            # JavaScript to close window (works in some browsers)
            st.markdown("""
            <script>
            setTimeout(function() {
                window.close();
            }, 2000)
            </script>
            """, unsafe_allow_html=True)
            st.rerun()

# MAIN LOGIC
# ==========

# Step 1: Check if unit is selected
unit_selected = validate_unit_selection()

if not unit_selected:
    # No unit selected - show start message
    st.warning("⚠️ **No Configuration Found** - Please complete the unit selection and parameter configuration first.")
    
    col_start1, col_start2, col_start3 = st.columns([1, 1, 1])
    with col_start2:
        if st.button("**Start Configuration**", use_container_width=True, type="primary"):
            st.switch_page("pages/page_unit.py")

else:
    # Step 2: Unit selected - validate parameters
    zero_unit_params, zero_payload_params = validate_parameters()
    all_params_valid = not zero_unit_params and not zero_payload_params
    
    # Step 3: Display configuration overview (always show if unit selected)
    display_unit_overview()
    
    # Detailed Configuration in Four Columns
    st.markdown("---")
    st.markdown("### 🔍 **Detailed Configuration**")
    
    col_config1, col_config2, col_config3, col_config4 = st.columns([1, 1, 1, 1])
    
    with col_config1:
        display_unit_parameters()
    
    with col_config2:
        display_payload_parameters()
    
    with col_config3:
        display_special_functions()
    
    with col_config4:
        display_selected_results()
    
    # Step 4: Export Section
    st.markdown("---")
    st.markdown("### 📤 **Export Configuration**")
    
    if all_params_valid:
        # All parameters are valid - show export button
        col_export1, col_export2, col_export3 = st.columns([1, 1, 1])
        
        with col_export2:
            if st.button("📁 **Generate Configuration File**", 
                        type='primary', 
                        use_container_width=True,
                        help="Download INI file"):
                generate_config_file()
    
    else:
        # Parameters invalid - show error messages
        display_validation_errors(zero_unit_params, zero_payload_params)
        
        col_back1, col_back2, col_back3 = st.columns([1, 1, 1])
        with col_back2:
            if st.button("← **Go Back to Unit configuration**", use_container_width=True, type="secondary"):
                st.switch_page("pages/page_unit.py")

# Step 5: Navigation (always show)
display_navigation_buttons()

st.divider()
