from pathlib import Path
import streamlit as st
import os

# Configure page layout
st.set_page_config(layout="wide", page_title="Agent Control Panel")

# Title
st.title("Agent Control Panel")

# Get agents from the agents folder
agents_folder = Path("agents")
agents = []

if agents_folder.exists():
    agents = [f.stem for f in agents_folder.glob("*.py") if f.name != "__init__.py"]

# Main layout with sidebar
with st.sidebar:
    st.header("Available Agents")
    selected_agent = st.selectbox("Select an agent:", agents if agents else ["No agents found"])

# Main content area
if agents:
    st.header(f"Agent: {selected_agent}")
    
    # Create columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Configuration")
        # Add input fields for agent parameters
        user_input = st.text_area("Enter input:", height=200)
        
        # Trigger button
        if st.button("Run Agent", type="primary"):
            with st.spinner(f"Running {selected_agent}..."):
                try:
                    # Import and run the selected agent
                    agent_module = __import__(f"agents.{selected_agent}", fromlist=[selected_agent])
                    
                    # Call the main function or execute the agent
                    if hasattr(agent_module, "run"):
                        result = agent_module.run()
                    else:
                        result = "Agent executed successfully"
                    
                    st.success("Agent completed!")
                    st.subheader("Results")
                    st.write(result)
                except Exception as e:
                    st.error(f"Error running agent: {str(e)}")
    
    with col2:
        st.subheader("Agent Info")
        st.info(f"**Agent Name:** {selected_agent}\n\n**Status:** Ready")
else:
    st.warning("No agents found in the 'agents' folder.")