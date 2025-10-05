"""
app.py
Main Streamlit application for quantum circuit visualization.
Provides UI for building and simulating quantum circuits.
All outputs use BIG-ENDIAN convention (q0 is leftmost bit).
Includes Bloch sphere visualization for 1-2 qubits and state city for 3 qubits.
"""

import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from qiskit.visualization import (
    plot_histogram, 
    circuit_drawer
)
from qiskit.quantum_info import DensityMatrix #nxt updt
import numpy as np

#custom modules
from gates import create_circuit, AVAILABLE_GATES, get_gate_description
from utils import (
    run_circuit, 
    calculate_probabilities, 
    format_statevector,
    get_measurement_counts,
    format_complex_number,
    get_circuit_stats,
    get_single_qubit_density_matrices,
    statevector_to_bloch_vector,
    density_matrix_to_bloch_vector,
    plot_bloch_sphere_plotly,
    plot_state_city_big_endian
)








st.set_page_config(
    page_title="Quantum Circuit Visualizer",
    page_icon="", # if you have a good icon, put in here :)
    layout="wide"
)




def main():
    """Main application function."""
    
    st.title("Quantum Visualizer")
    st.markdown("""
    Build and simulate quantum circuits with various gates.
    Select the number of qubits and add gates to see the resulting quantum state.
    
    **Note:** Qubit ordering follows big-endian convention (q0 is the leftmost bit in output).
    """)
    
    # sidebar
    st.sidebar.header("Circuit Configuration")
    
    # selecgt nunber qubit
    num_qubits = st.sidebar.selectbox(
        "Number of Qubits",
        options=[1, 2, 3],
        index=0,
        help="Choose how many qubits to use in the circuit"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Build Gate Sequence")
    
    # init session state for gate sequence
    if 'gate_sequence' not in st.session_state:
        st.session_state.gate_sequence = []
    
    available_gates = AVAILABLE_GATES[num_qubits]
    
    col1, col2 = st.sidebar.columns([2, 1])
    
    with col1:
        selected_gate = st.selectbox(
            "Select Gate",
            options=available_gates,
            format_func=lambda x: f"{x} - {get_gate_description(x).split(' - ')[1]}"
        )
    
    # gate descritpion
    st.sidebar.info(get_gate_description(selected_gate))
    
    # specifics parameters
    gate_params = None
    
    if selected_gate in ['H', 'X', 'Y', 'Z', 'S', 'T']:
        # single qubit gates
        qubit = st.sidebar.selectbox(
            "Target Qubit",
            options=list(range(num_qubits)),
            format_func=lambda x: f"q{x}"
        )
        gate_params = qubit
        
    elif selected_gate == 'CNOT':
        col_c, col_t = st.sidebar.columns(2)
        with col_c:
            control = st.selectbox(
                "Control",
                options=list(range(num_qubits)),
                format_func=lambda x: f"q{x}"
            )
        with col_t:
            target_options = [q for q in range(num_qubits) if q != control]
            target = st.selectbox(
                "Target",
                options=target_options,
                format_func=lambda x: f"q{x}"
            )
        gate_params = (control, target)
        
    elif selected_gate == 'SWAP':
        col_q1, col_q2 = st.sidebar.columns(2)
        with col_q1:
            qubit1 = st.selectbox(
                "Qubit 1",
                options=list(range(num_qubits)),
                format_func=lambda x: f"q{x}"
            )
        with col_q2:
            qubit2_options = [q for q in range(num_qubits) if q != qubit1]
            qubit2 = st.selectbox(
                "Qubit 2",
                options=qubit2_options,
                format_func=lambda x: f"q{x}"
            )
        gate_params = (qubit1, qubit2)
        
    elif selected_gate == 'Toffoli':
        col_c1, col_c2, col_t = st.sidebar.columns(3)
        with col_c1:
            control1 = st.selectbox(
                "Ctrl 1",
                options=list(range(num_qubits)),
                format_func=lambda x: f"q{x}"
            )
        with col_c2:
            control2_options = [q for q in range(num_qubits) if q != control1]
            control2 = st.selectbox(
                "Ctrl 2",
                options=control2_options,
                format_func=lambda x: f"q{x}"
            )
        with col_t:
            target_options = [q for q in range(num_qubits) if q not in [control1, control2]]
            target = st.selectbox(
                "Target",
                options=target_options,
                format_func=lambda x: f"q{x}"
            )
        gate_params = (control1, control2, target)
    



    # gate button
    if st.sidebar.button("➕ Add Gate", use_container_width=True):
        st.session_state.gate_sequence.append((selected_gate, gate_params))
        st.rerun()
    
    # dsiplay current gate sequence
    if st.session_state.gate_sequence:
        st.sidebar.markdown("---")
        st.sidebar.subheader("Current Gate Sequence")
        
        for idx, (gate, params) in enumerate(st.session_state.gate_sequence):
            col_info, col_del = st.sidebar.columns([4, 1])
            with col_info:
                if isinstance(params, tuple):
                    params_str = f"({', '.join(f'q{p}' for p in params)})"
                else:
                    params_str = f"q{params}"
                st.text(f"{idx+1}. {gate} {params_str}")
            with col_del:
                if st.button("🗑️", key=f"del_{idx}"):
                    st.session_state.gate_sequence.pop(idx)
                    st.rerun()
        
        # clear all button
        if st.sidebar.button("🗑️ Clear All", use_container_width=True):
            st.session_state.gate_sequence = []
            st.rerun()
    




    # simulation parameters
    st.sidebar.markdown("---")
    shots = st.sidebar.slider(
        "Measurement Shots",
        min_value=100,
        max_value=10000,
        value=1024,
        step=100,
        help="Number of times to measure the circuit"
    )
    
    # main content area
    if not st.session_state.gate_sequence:
        st.info("Add gates from the sidebar to build your quantum circuit")
        
        # Show qubit ordering explanation
        st.markdown("---")
        st.subheader("Qubit Ordering Convention")
        st.markdown("""
        This application uses **big-endian** notation for outputs:
        - **q0 is the leftmost bit** in all displayed results
        - **qN is the rightmost bit**
        
        **Example for 2 qubits:**
        - State `|01⟩` means: q0=0, q1=1
        - State `|10⟩` means: q0=1, q1=0
        
        **Example for 3 qubits:**
        - State `|101⟩` means: q0=1, q1=0, q2=1
        
        This matches the intuitive left-to-right reading order.
        """)
        return
    



    # create and run circuit
    try:
        circuit = create_circuit(num_qubits, st.session_state.gate_sequence)
        
        # circuit statistics
        stats = get_circuit_stats(circuit)
        
        # circuit statistics (display)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Qubits", stats['num_qubits'])
        with col2:
            st.metric("Circuit Depth", stats['depth'])
        with col3:
            st.metric("Total Gates", stats['size'])
        with col4:
            st.metric("Gate Types", len(stats['num_gates']))
        
        st.markdown("---")
        
        # display circuit diagram
        st.subheader("🔷 Circuit Diagram")
        fig = circuit.draw(output='mpl', style='iqp')
        st.pyplot(fig)
        plt.close()
        
        st.markdown("---")
        


        # run simulation
        with st.spinner("Running quantum simulation..."):
            results = run_circuit(circuit, shots=shots)
            statevector = results['statevector']
        

        # add bloch sphere / state visualization section
        st.subheader("Quantum State Visualization")
        
        if num_qubits == 1:
            # single qubit
            st.markdown("**Interactive Bloch Sphere Representation**")
            st.markdown("""
            The Bloch sphere shows the quantum state as a vector in 3D space:
            - **X-axis (Red)**: Real part of superposition
            - **Y-axis (Green)**: Imaginary part (phase)
            - **Z-axis (Blue)**: Population difference (|0⟩ vs |1⟩)
            
            **Click and drag to rotate the sphere!**
            """)
            


            bloch_vec = statevector_to_bloch_vector(statevector)
            
            fig = plot_bloch_sphere_plotly(bloch_vec, title="Single Qubit State")
            st.plotly_chart(fig, use_container_width=True)
            
            # bloch vector components
            x, y, z = bloch_vec
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("X (Real)", f"{x:.4f}")
            with col2:
                st.metric("Y (Imaginary)", f"{y:.4f}")
            with col3:
                st.metric("Z (Population)", f"{z:.4f}")
            
        elif num_qubits == 2:
            # 2 qubits
            st.markdown("**Individual Qubit Bloch Spheres** (Reduced Density Matrices)")
            st.markdown("""
            Each sphere shows the state of one qubit after tracing out the other.
            - **Pure state**: Vector touches sphere surface (|r| = 1)
            - **Mixed state**: Vector inside sphere (|r| < 1, indicates entanglement)
            
            **Click and drag each sphere to rotate!**
            """)
            


            reduced_dms = get_single_qubit_density_matrices(statevector, num_qubits)
            
            col_bloch1, col_bloch2 = st.columns(2)
            
            with col_bloch1:
                st.markdown("**Qubit 0 (q0)**")
                bloch_vec_0 = density_matrix_to_bloch_vector(reduced_dms[0])
                
                fig0 = plot_bloch_sphere_plotly(bloch_vec_0, title="Qubit 0 State")
                st.plotly_chart(fig0, use_container_width=True)
                
                r0 = np.sqrt(sum(c**2 for c in bloch_vec_0))
                if r0 > 0.99:
                    st.success(f"Pure state (|r|={r0:.4f})")
                else:
                    st.warning(f"Mixed state (|r|={r0:.4f}) - Entangled!")
                
                #components
                x0, y0, z0 = bloch_vec_0
                st.text(f"X: {x0:.4f}, Y: {y0:.4f}, Z: {z0:.4f}")
            
            with col_bloch2:
                st.markdown("**Qubit 1 (q1)**")
                bloch_vec_1 = density_matrix_to_bloch_vector(reduced_dms[1])
                
                fig1 = plot_bloch_sphere_plotly(bloch_vec_1, title="Qubit 1 State")
                st.plotly_chart(fig1, use_container_width=True)
                
                r1 = np.sqrt(sum(c**2 for c in bloch_vec_1))
                if r1 > 0.99:
                    st.success(f"Pure state (|r|={r1:.4f})")
                else:
                    st.warning(f"Mixed state (|r|={r1:.4f}) - Entangled!")
                
                # components
                x1, y1, z1 = bloch_vec_1
                st.text(f"X: {x1:.4f}, Y: {y1:.4f}, Z: {z1:.4f}")
            
        elif num_qubits == 3:
            # 3 qubits: 
            st.markdown("**3D State City Visualization** (3 Qubits)")
            st.markdown("""
            3D bar chart showing amplitude components for each basis state:
            - **Red bars**: Real part (positive = red, negative = dark red)
            - **Blue bars**: Imaginary part (positive = blue, negative = dark blue)
            - **X-axis**: Basis states in big-endian order (q0 q1 q2)
            - **Bar height**: Amplitude magnitude
            """)
            
            fig = plot_state_city_big_endian(statevector, num_qubits, 
                                             title='3-Qubit State Amplitudes (Big-Endian)')
            st.pyplot(fig)
            plt.close()
            
            st.info("**Tip:** The visualization shows all 8 basis states with their complex amplitudes.")
        
        st.markdown("---")
        
        # results in columns
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("Statevector (Big-Endian)")
            formatted_sv = format_statevector(statevector)
            
            st.markdown("**Quantum State Amplitudes:**")
            st.markdown("*(q0 is leftmost, qN is rightmost)*")
            for basis_state, amplitude, probability in formatted_sv:
                amp_str = format_complex_number(amplitude)
                st.markdown(
                    f"- `|{basis_state}⟩`: {amp_str} "
                    f"(probability: {probability:.4f})"
                )
            
            # probabilitise table
            st.markdown("---")
            st.markdown("**Probability Distribution:**")


            probs = calculate_probabilities(statevector)
            
            prob_data = []
            for state, prob in sorted(probs.items(), key=lambda x: x[1], reverse=True):
                if prob > 1e-10:  # 0nly show non zero probabilities
                    prob_data.append({
                        'State': f"|{state}⟩",
                        'Probability': f"{prob:.6f}",
                        'Percentage': f"{prob*100:.2f}%"
                    })
            
            st.dataframe(prob_data, use_container_width=True)
        
        with col_right:
            st.subheader("Measurement Results (Big-Endian)")
            counts = get_measurement_counts(circuit, shots=shots)
            
            # histogram
            fig = plot_histogram(counts, figsize=(8, 6), color='#6366f1')
            st.pyplot(fig)
            plt.close()
            
            # raw counts
            st.markdown("---")
            st.markdown("**Raw Measurement Counts:**")
            st.markdown("*(q0 is leftmost, qN is rightmost)*")
            
            counts_data = []
            for state, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
                counts_data.append({
                    'State': state,
                    'Count': count,
                    'Frequency': f"{count/shots:.4f}"
                })
            
            st.dataframe(counts_data, use_container_width=True)
        
        # additional analysis
        st.markdown("---")
        st.subheader("Circuit Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Gate Operations:**")
            for gate_name, count in stats['num_gates'].items():
                st.markdown(f"- {gate_name}: {count}")
        
        with col2:
            st.markdown("**Quantum Properties:**")
            if num_qubits > 1:
                single_qubit_probs = [abs(amp)**2 for amp in statevector]
                max_prob = max(single_qubit_probs)
                if max_prob < 0.99:
                    st.markdown("- State appears to be **entangled**")
                else:
                    st.markdown("- State appears to be **separable**")
            
            # kalau superposisi
            non_zero_states = sum(1 for p in probs.values() if p > 1e-10)
            if non_zero_states > 1:
                st.markdown(f"- **Superposition** of {non_zero_states} states")
            else:
                st.markdown("- Classical state (no superposition)")
        
        # qubit ordering reminder
        st.markdown("---")
        st.info("**Reminder:** All results use big-endian notation (q0 is leftmost bit)")
        
        # footer
        st.markdown("---")
        st.markdown(
            "<div style='text-align: center; color: gray; padding: 20px;'>"
            "Powered by Qiskit | by Rexzea"
            "</div>",
            unsafe_allow_html=True
        )
        
    except Exception as e:
        st.error(f"Error running circuit: {str(e)}")
        st.exception(e)


if __name__ == "__main__":
    main()