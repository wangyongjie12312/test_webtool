import streamlit as st
from PIL import Image
import os

# page 2 content
st.markdown("# Selection of Customized Results")

# Default values for quick actions
default_customized_body_results = ["Force (F_fb)", "Force Active (F_active)"]
default_customized_rod_results = ["Setpoint (F_sp_CT)",  "S-curve (S_curve_x)"]
default_customized_payload_results = ["v_payload_m", "acc_payload_MRU"]
# Initialize default selections in session state if they don't exist
if 'selected_body_results' not in st.session_state:
    st.session_state.selected_body_results = default_customized_body_results
if 'selected_rod_results' not in st.session_state:
    st.session_state.selected_rod_results = default_customized_rod_results
if 'selected_payload_results' not in st.session_state:
    st.session_state.selected_payload_results = default_customized_payload_results
if 'customized_results' not in st.session_state:
    st.session_state.customized_results = False


# Add this near the top of page_export.py after checking for valid config
rod_function_defaults = {
    'check_box_rod_lock': False,
    'rod_lock_depth': 10.0,
    'rod_lock_operation': 'Lifting Down',
    'rod_lock_mode': 'Auto Lock at Depth',
    'lock_hold_time': 5.0,
    'lock_speed': 0.5,
    'rod_orientation': 'Rod Down (Standard)'
}

for key, default_value in rod_function_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = default_value


st.divider()

results_index = 1 if st.session_state.customized_results else 0
col1, col2 = st.columns([1, 2])
with col1:
    st.markdown("#### Select the results to show in OrcaFlex:")
    selection_box_results = st.selectbox("OrcaFlex defaults", options=["OrcaFlex defaults", "Customized"], key="results_selectbox", index=results_index)

with col2:
    image = Image.open(os.path.join('figures', 'SafelinkTabWiFi.png'))
    col1, col2 = st.columns([1, 1])
    with col2:
        st.image(image, width=300)    

if selection_box_results == "OrcaFlex defaults":
    st.session_state.customized_results = False
    st.markdown("The results will be generated based on the OrcaFlex predefined results.")
    st.divider()
    image = Image.open(os.path.join('figures', 'Lazy_Wave_Riser.png'))
    col01, col02, col03 = st.columns([1, 6, 1])
    with col02:
        st.image(image, width=1000)    
        
elif selection_box_results == "Customized":
    if st.session_state.selected_unit != None and st.session_state.selected_unit != "None":
        st.session_state.customized_results = True
        
        # Auto-set defaults when customized is selected for the first time
        if (not st.session_state.selected_body_results and 
            not st.session_state.selected_rod_results and 
            not st.session_state.selected_payload_results):
            
            st.session_state.selected_body_results = default_customized_body_results.copy()
            st.session_state.selected_rod_results = default_customized_rod_results.copy()
            st.session_state.selected_payload_results = default_customized_payload_results.copy()
            
        # Show a message to inform the user
        st.info("**Default customized results are selected!** Modify the selections below to show more results in addition to the OrcaFlex defaults.")
        st.markdown("See [Help documentation](https://www.safelink.no) for detailed explaination of the results listed bellow. Contact [Safelink]() if more results are needed.")
        st.divider()
        options = [
                    "Force (F_fb)",                 
                    "Force (d_PID_CT_dt)",           
                    "Force (F_CT_point)",            
                    "Force External (F_external)",   
                    "Force Internal (F_internal)",   
                    "Force Passive (F_passive)",     
                    "Force Active (F_active)",       
                    "Force Spring (F_spring)",       
                    "Force Damping (F_damping)",     
                    "Force Friction (F_friction)",   
                    "Force Feedforward (F_ff)",      
                    "Force (F_CT)",                     
                    "Force (Target_CT)",             
                    "Measured Force (F_IAHC_total_m)",  
                    "Measured Stroke (S_m)",          
                    "Measured Stroke Velocity (vS_m)",
                    "Measured Stroke Acc (acc_S_m)",  
                    "Measured velocity (v_rod_m)",    
                    "Measured heave (h_rod_m)",       
                    "Setpoint (F_sp_CT)",             
                    "Setpoint (F_sp_HC)",             
                    "Setpoint (v_rod_sp)",            
                    "Setpoint (h_rod_sp)",            
                    "Orcaflex Stroke (S_orc)",          
                    "Orcaflex Stroke Velocity (vS_orc)",
                    "Filtered (S_m_LP)",        
                    "Filtered (vS_m_LP)",       
                    "Filtered (acc_S_m_LP)",    
                    "Tracking error (e_h_rod)",         
                    "Tracking error (e_v_payload)",     
                    "Tracking error (e_F_CT)",          
                    "Tracking error (e_v_body)",      
                    "S-curve (S_curve_x)",              
                    "S-curve (S_curve_v)",              
                    "S-curve (S_curve_j)",              
                    "S-curve (S_curve_acc)",            
                    "S-curve (S_curve_x_k)",          
                    "S-curve (S_curve_v_k)",          
                    "S-curve (S_curve_acc_k)",        
                    "F_fb_limit_lower",               
                    "F_fb_limit_upper",               
                    ]
        options_payload =[
                    "acc_payload_MRU",        
                    "acc_external_MRU",       
                    "acc_external_MRU_inverted",
                    "acc_payload_sp",         
                    "acc_payload_sp_fb",      
                    "v_payload_sp_fb",        
                    "v_payload_m",            
                    "v_external_MRU",         
                    "h_external_MRU",         
                    "v_external_MRU_inverted",
                    "h_external_MRU_inverted",
                    "acc_limit_lower",        
                    "acc_limit_upper",        
                    "v_payload_limit_lower",  
                    "v_payload_limit_upper",  
                    ]
        #%% system parameters

        st.markdown("### Available Results")
        
        col_c1, col_c2, col_c3 = st.columns([1, 1, 1])
            
        # Function to create a clean key from option name
        def create_clean_key(prefix, option):
            return f"{prefix}_{option.replace(' ', '_').replace('(', '').replace(')', '').replace('/', '_')}"

        # Function to update body results based on checkbox changes
        def update_body_results():
            new_selections = []
            for option in options[:15]:
                checkbox_key = create_clean_key("body", option)
                if st.session_state[checkbox_key]:
                    new_selections.append(option)
            st.session_state.selected_body_results = new_selections

        # Function to update rod results based on checkbox changes
        def update_rod_results():
            new_selections = []
            for option in options[15:]:
                checkbox_key = create_clean_key("rod", option)
                if st.session_state[checkbox_key]:
                    new_selections.append(option)
            st.session_state.selected_rod_results = new_selections

        # Function to update payload results based on checkbox changes
        def update_payload_results():
            new_selections = []
            for option in options_payload:
                checkbox_key = create_clean_key("payload", option)
                if st.session_state[checkbox_key]:
                    new_selections.append(option)
            st.session_state.selected_payload_results = new_selections

        col_c1, col_c2, col_c3 = st.columns([1, 1, 1])
            
        with col_c1:
            st.markdown("#### Body")
            
            # Get current body count for expander title
            body_count = len(st.session_state.selected_body_results)
            
            with st.expander(f"🔵 Body Results ({body_count}/15)", expanded=body_count >= 2):
                # Process each body option
                for option in options[:15]:
                    checkbox_key = create_clean_key("body", option)
                    
                    # Check if this option is currently selected
                    is_currently_selected = option in st.session_state.selected_body_results
                    
                    # Create checkbox with current state and callback
                    st.checkbox(
                        option, 
                        value=is_currently_selected, 
                        key=checkbox_key,
                        on_change=update_body_results,
                        height=500
                    )
            
        with col_c2:
            st.markdown("#### Rod")
            
            # Get current rod count for expander title
            rod_count = len(st.session_state.selected_rod_results)
            rod_total = len(options[15:])
            
            with st.expander(f"🟢 Rod Results ({rod_count}/{rod_total})", expanded=rod_count >= 2):
                # Process each rod option
                for option in options[15:]:
                    checkbox_key = create_clean_key("rod", option)
                    
                    # Check if this option is currently selected
                    is_currently_selected = option in st.session_state.selected_rod_results
                    
                    # Create checkbox with current state and callback
                    st.checkbox(
                        option, 
                        value=is_currently_selected, 
                        key=checkbox_key,
                        on_change=update_rod_results,
                        height=500
                    )
            
        with col_c3:
            st.markdown("#### Payload")
            
            # Get current payload count for expander title
            payload_count = len(st.session_state.selected_payload_results)
            payload_total = len(options_payload)
            
            with st.expander(f"🟡 Payload Results ({payload_count}/{payload_total})", expanded=payload_count >= 2):
                # Process each payload option
                for option in options_payload:
                    checkbox_key = create_clean_key("payload", option)
                    
                    # Check if this option is currently selected
                    is_currently_selected = option in st.session_state.selected_payload_results
                    
                    # Create checkbox with current state and callback
                    st.checkbox(
                        option, 
                        value=is_currently_selected, 
                        key=checkbox_key,
                        on_change=update_payload_results,
                        height=500
                    )

        
        # Display summary of selections
        
        total_selections = len(st.session_state.selected_body_results) + len(st.session_state.selected_rod_results) + len(st.session_state.selected_payload_results)
        
        if total_selections == 0:
            st.info("ℹ️ **No custom results selected** - Select checkboxes above to customize results or proceed with OrcaFlex defaults")
            st.markdown("### Selected Results")
            
            # Show summary in expandable sections
            col_summary1, col_summary2, col_summary3 = st.columns([1, 1, 1])
            
            with col_summary1:
                if st.session_state.selected_body_results:
                    with st.expander(f"Body Results ({len(st.session_state.selected_body_results)})"):
                        for result in st.session_state.selected_body_results:
                            st.write(f"• {result}")
            
            with col_summary2:
                if st.session_state.selected_rod_results:
                    with st.expander(f"Rod Results ({len(st.session_state.selected_rod_results)})"):
                        for result in st.session_state.selected_rod_results:
                            st.write(f"• {result}")
            
            with col_summary3:
                if st.session_state.selected_payload_results:
                    with st.expander(f"Payload Results ({len(st.session_state.selected_payload_results)})"):
                        for result in st.session_state.selected_payload_results:
                            st.write(f"• {result}")

        st.markdown("<br>"*1, unsafe_allow_html=True)
        _, _, col_action3, col_action4 = st.columns([2, 3, 1, 1])
        
        with col_action3:
            if st.button("📋 Select Default Results", use_container_width=True, type='secondary', help="Predefined parameters"):
                # Pre-select commonly used results
                st.session_state.selected_body_results = default_customized_body_results.copy()
                st.session_state.selected_rod_results = default_customized_rod_results.copy()
                st.session_state.selected_payload_results = default_customized_payload_results.copy()
                st.session_state.results_manually_cleared = False  # Reset flag since user selected defaults
                st.rerun()

        with col_action4:
            total_available = len(options) + len(options_payload)
            if st.button(f"✅ Select All ({total_available})", use_container_width=True, type = 'secondary', help="All available results"):
                st.session_state.selected_body_results = options[:15]
                st.session_state.selected_rod_results = options[15:]
                st.session_state.selected_payload_results = options_payload
                st.rerun()

        results_dict = {
                "body_results": st.session_state.selected_body_results,
                "rod_results": st.session_state.selected_rod_results,
                "payload_results": st.session_state.selected_payload_results
            }
        st.session_state.selected_results = results_dict

    else:
        st.warning("⚠️ **No Unit Selected** - Please choose a unit.")
        st.page_link("pages/page_unit.py", label="← Back to **Unit Selection**")
        
# go to next page
st.markdown("<br>"*3, unsafe_allow_html=True)
col_next_1, col_next_2, col_next_3 = st.columns([1, 1, 1])
# Check if configuration is complete enough
is_ready = (st.session_state.selected_unit and 
            st.session_state.selected_unit != "None")

with col_next_2:
    if is_ready:
        # Check if any custom results are selected
        if selection_box_results == "Customized":
            # Check if any results are selected in customized mode
            has_custom_results = (
                len(st.session_state.selected_body_results) > 0 or
                len(st.session_state.selected_rod_results) > 0 or
                len(st.session_state.selected_payload_results) > 0
            )
            
            if has_custom_results:
                if st.button("Proceed with Customized Defaults ->", use_container_width=True, type="primary"):
                    st.switch_page("pages/page_export.py")
            else:
                # No custom results selected, fall back to OrcaFlex defaults
                if st.button("Proceed with OrcaFlex Defaults ->", use_container_width=True, type="primary"):
                    # Set session state to use defaults
                    st.session_state.customized_results = False
                    st.session_state.selected_results = {
                        "body_results": [],
                        "rod_results": [],
                        "payload_results": []
                    }
                    # Navigate to export page
                    st.switch_page("pages/page_export.py")
        else:
            # OrcaFlex defaults mode
            if st.button("Proceed with OrcaFlex Defaults ->", use_container_width=True, type="primary"):
                st.switch_page("pages/page_export.py")