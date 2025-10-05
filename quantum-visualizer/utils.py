"""
utils.py
Utility functions for quantum circuit simulation and result processing.
Handles statevector extraction, probability calculations, and formatting.
Includes conversion from Qiskit's little-endian to intuitive big-endian format.
"""

import numpy as np
from qiskit_aer import Aer
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D   # for lane 598






def reverse_bitstring(bitstring):
    return bitstring[::-1]


def convert_counts_to_big_endian(counts):
    return {reverse_bitstring(state): count for state, count in counts.items()}


def convert_probs_to_big_endian(probabilities):
    return {reverse_bitstring(state): prob for state, prob in probabilities.items()}





def run_circuit(circuit, shots=1024):
    # aer simulator backend (new api)
    backend = Aer.get_backend('aer_simulator')
    
    # run the circuit (new api: backend.run() instead of execute())
    job = backend.run(circuit, shots=shots)
    
    #results
    result = job.result()
    statevector = result.data()['statevector']
    
    return {
        'statevector': statevector,
        'result': result
    }





def calculate_probabilities(statevector):
    probabilities = {}
    num_qubits = int(np.log2(len(statevector)))
    
    for i, amplitude in enumerate(statevector):
        # convert index to binary string (basis state) - this is little endian from Qiskit
        basis_state_little_endian = format(i, f'0{num_qubits}b')
        # convert to big endian 
        basis_state_big_endian = reverse_bitstring(basis_state_little_endian)
        # probability is magnitude squared of amplitude
        probability = abs(amplitude) ** 2
        probabilities[basis_state_big_endian] = probability
    
    return probabilities





def format_statevector(statevector, threshold=1e-10):
    formatted = []
    num_qubits = int(np.log2(len(statevector)))
    
    for i, amplitude in enumerate(statevector):
        # only include non negligible amplitudes
        if abs(amplitude) > threshold:
            # qiskit uses little endian, convert to big endian
            basis_state_little_endian = format(i, f'0{num_qubits}b')
            basis_state_big_endian = reverse_bitstring(basis_state_little_endian)
            probability = abs(amplitude) ** 2
            formatted.append((basis_state_big_endian, amplitude, probability))
    
    return formatted





def get_measurement_counts(circuit, shots=1024):
    measured_circuit = circuit.copy()
    measured_circuit.measure_all()
    
    # run on simulator
    backend = Aer.get_backend('aer_simulator')
    job = backend.run(measured_circuit, shots=shots)
    result = job.result()
    
    # counts (these are in little endian format from Qiskit)
    counts_little_endian = result.get_counts()
    counts_big_endian = convert_counts_to_big_endian(counts_little_endian)
    
    return counts_big_endian





def format_complex_number(complex_num):
    real = complex_num.real
    imag = complex_num.imag
    
    # handle pure real numbers
    if abs(imag) < 1e-10: # IMPORTANT
        return f"{real:.4f}"
    
    # handle pure imaginary numbers
    if abs(real) < 1e-10: # IMPORTANT
        return f"{imag:.4f}i"
    
    # Handle complex numbers
    sign = '+' if imag >= 0 else '' # IMPORTANT
    return f"{real:.4f}{sign}{imag:.4f}i"





def normalize_counts(counts, shots):
    return {state: count / shots for state, count in counts.items()}





def get_circuit_depth(circuit):
    return circuit.depth()





def get_circuit_stats(circuit):
    return {
        'num_qubits': circuit.num_qubits,
        'depth': circuit.depth(),
        'size': circuit.size(),  # total number of gate operations
        'num_gates': dict(circuit.count_ops())  # count of each gqte type
    }





def statevector_to_density_matrix(statevector):
    sv = np.array(statevector).reshape(-1, 1)
    return sv @ sv.conj().T





def partial_trace(density_matrix, keep_qubit, num_qubits):
    dim = 2 ** num_qubits
    
    # reshape density matrix for partial trace
    # we need to trace out all qubits except the one we want to keep
    reduced_dm = np.zeros((2, 2), dtype=complex)
    
    for i in range(dim):
        for j in range(dim):
            # extract bit values for each qubit
            bits_i = [(i >> q) & 1 for q in range(num_qubits)]
            bits_j = [(j >> q) & 1 for q in range(num_qubits)]
            
            # check if all qubits except keep_qubit match
            trace_match = all(
                bits_i[q] == bits_j[q] 
                for q in range(num_qubits) 
                if q != keep_qubit
            )
            
            if trace_match:
                reduced_dm[bits_i[keep_qubit], bits_j[keep_qubit]] += density_matrix[i, j]
    
    return reduced_dm





def get_single_qubit_density_matrices(statevector, num_qubits):
    # convert stqtevector to full density matrix
    full_dm = statevector_to_density_matrix(statevector)
    
    # reduced density matrix for each qubit
    reduced_dms = []
    for qubit_idx in range(num_qubits):
        reduced_dm = partial_trace(full_dm, qubit_idx, num_qubits)
        reduced_dms.append(reduced_dm)
    
    return reduced_dms





def density_matrix_to_bloch_vector(density_matrix):
    # pauli matrices
    sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
    
    # calculate Bloch vector components
    x = np.real(np.trace(density_matrix @ sigma_x))
    y = np.real(np.trace(density_matrix @ sigma_y))
    z = np.real(np.trace(density_matrix @ sigma_z))
    
    return x, y, z





def statevector_to_bloch_vector(statevector):
    # for single qubit
    alpha = statevector[0]
    beta = statevector[1]
    
    #bloch vector coordinates
    x = 2 * np.real(np.conj(alpha) * beta)
    y = 2 * np.imag(np.conj(alpha) * beta)
    z = np.abs(alpha)**2 - np.abs(beta)**2
    
    return x, y, z




# ====================================================================================================================================================================
def plot_bloch_sphere_custom(bloch_vector, title="Bloch Sphere", show_axes_labels=True):
    from mpl_toolkits.mplot3d import Axes3D
    
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Bloch sphere
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x_sphere = np.outer(np.cos(u), np.sin(v))
    y_sphere = np.outer(np.sin(u), np.sin(v))  # Y (Imaginary)
    z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))
    
    ax.plot_surface(x_sphere, y_sphere, z_sphere, color='cyan', alpha=0.1, edgecolor='none')
    
    # equator and meridians
    theta = np.linspace(0, 2 * np.pi, 100)
    
    #(XY plane)
    ax.plot(np.cos(theta), np.sin(theta), 0, 'gray', alpha=0.3, linewidth=1)
    
    # prime meridian (XZ plane)
    phi = np.linspace(0, np.pi, 100)
    ax.plot(np.sin(phi), 0, np.cos(phi), 'gray', alpha=0.3, linewidth=1)
    
    # meridian (YZ plane)
    ax.plot(0, np.sin(phi), np.cos(phi), 'gray', alpha=0.3, linewidth=1)
    
    # coordinate axes
    axis_length = 1.3
    
    # x axis (red)
    ax.quiver(0, 0, 0, axis_length, 0, 0, color='red', arrow_length_ratio=0.1, linewidth=2)
    ax.text(axis_length + 0.1, 0, 0, 'X', fontsize=14, color='red', weight='bold')
    
    # y axis (green) - IMAGINARY COMPONENT
    ax.quiver(0, 0, 0, 0, axis_length, 0, color='green', arrow_length_ratio=0.1, linewidth=2)
    ax.text(0, axis_length + 0.1, 0, 'Y', fontsize=14, color='green', weight='bold')
    
    # z axis (blue)
    ax.quiver(0, 0, 0, 0, 0, axis_length, color='blue', arrow_length_ratio=0.1, linewidth=2)
    ax.text(0, 0, axis_length + 0.1, 'Z', fontsize=14, color='blue', weight='bold')
    
    # Bloch vector
    x, y, z = bloch_vector
    vector_length = np.sqrt(x**2 + y**2 + z**2)
    
    if vector_length > 0.01:  # if vector is significant
        # vector arrow
        ax.quiver(0, 0, 0, x, y, z, color='purple', arrow_length_ratio=0.15, linewidth=3)
        
        # point at end of vector
        ax.scatter([x], [y], [z], color='purple', s=100, marker='o')
        
        # vector length annotation
        ax.text(x * 1.1, y * 1.1, z * 1.1, 
                f'|r|={vector_length:.3f}',
                fontsize=10, color='purple', weight='bold')
    
    # labels states
    ax.text(0, 0, 1.4, '|0⟩', fontsize=12, ha='center')
    ax.text(0, 0, -1.4, '|1⟩', fontsize=12, ha='center')
    ax.text(1.4, 0, 0, '|+⟩', fontsize=12, ha='center')
    ax.text(-1.4, 0, 0, '|-⟩', fontsize=12, ha='center')
    ax.text(0, 1.4, 0, '|+i⟩', fontsize=12, ha='center')
    ax.text(0, -1.4, 0, '|-i⟩', fontsize=12, ha='center')
    
    # equal aspect ratio and limits
    ax.set_xlim([-1.5, 1.5])
    ax.set_ylim([-1.5, 1.5])
    ax.set_zlim([-1.5, 1.5])
    ax.set_box_aspect([1, 1, 1])
    
    if show_axes_labels:
        ax.set_xlabel('X (Real)', fontsize=10)
        ax.set_ylabel('Y (Imaginary)', fontsize=10)
        ax.set_zlabel('Z (Population)', fontsize=10)
    
    ax.set_title(title, fontsize=14, weight='bold')
    ax.view_init(elev=20, azim=45)
    
    plt.tight_layout()
    
    return fig




# ====================================================================================================================================================================
def plot_bloch_sphere_plotly(bloch_vector, title="Bloch Sphere"):
    import plotly.graph_objects as go
    
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    x_sphere = np.outer(np.cos(u), np.sin(v))
    y_sphere = np.outer(np.sin(u), np.sin(v))
    z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))
    
    fig = go.Figure()
    
    fig.add_trace(go.Surface(
        x=x_sphere, y=y_sphere, z=z_sphere,
        colorscale=[[0, 'lightblue'], [1, 'lightblue']],
        showscale=False,
        opacity=0.3,
        name='Bloch Sphere'
    ))
    
    theta = np.linspace(0, 2 * np.pi, 100)
    fig.add_trace(go.Scatter3d(
        x=np.cos(theta), y=np.sin(theta), z=np.zeros_like(theta),
        mode='lines',
        line=dict(color='gray', width=2),
        name='Equator',
        showlegend=False
    ))
    
    # meridian (XZ plane)
    phi = np.linspace(0, 2 * np.pi, 100)
    fig.add_trace(go.Scatter3d(
        x=np.cos(phi), y=np.zeros_like(phi), z=np.sin(phi),
        mode='lines',
        line=dict(color='gray', width=2),
        name='Meridian XZ',
        showlegend=False
    ))
    
    # meridian (YZ plane)
    fig.add_trace(go.Scatter3d(
        x=np.zeros_like(phi), y=np.cos(phi), z=np.sin(phi),
        mode='lines',
        line=dict(color='gray', width=2),
        name='Meridian YZ',
        showlegend=False
    ))
    
    # x axis (red)
    fig.add_trace(go.Scatter3d(
        x=[0, 1.3], y=[0, 0], z=[0, 0],
        mode='lines+text',
        line=dict(color='red', width=6),
        text=['', 'X'],
        textposition='top center',
        textfont=dict(size=16, color='red'),
        name='X-axis (Real)',
        showlegend=True
    ))
    
    # y axis (green)
    fig.add_trace(go.Scatter3d(
        x=[0, 0], y=[0, 1.3], z=[0, 0],
        mode='lines+text',
        line=dict(color='green', width=6),
        text=['', 'Y'],
        textposition='top center',
        textfont=dict(size=16, color='green'),
        name='Y-axis (Imaginary)',
        showlegend=True
    ))
    
    # z axis (blue)
    fig.add_trace(go.Scatter3d(
        x=[0, 0], y=[0, 0], z=[0, 1.3],
        mode='lines+text',
        line=dict(color='blue', width=6),
        text=['', 'Z'],
        textposition='top center',
        textfont=dict(size=16, color='blue'),
        name='Z-axis (Population)',
        showlegend=True
    ))
    
    #state labels
    states = [
        (0, 0, 1.4, '|0⟩'),
        (0, 0, -1.4, '|1⟩'),
        (1.4, 0, 0, '|+⟩'),
        (-1.4, 0, 0, '|-⟩'),
        (0, 1.4, 0, '|+i⟩'),
        (0, -1.4, 0, '|-i⟩')
    ]
    
    for x, y, z, label in states:
        fig.add_trace(go.Scatter3d(
            x=[x], y=[y], z=[z],
            mode='text',
            text=[label],
            textfont=dict(size=14, color='black'),
            showlegend=False
        ))
    
    # Bloch vector
    x, y, z = bloch_vector
    vector_length = np.sqrt(x**2 + y**2 + z**2)
    
    if vector_length > 0.01:
        # vector line
        fig.add_trace(go.Scatter3d(
            x=[0, x], y=[0, y], z=[0, z],
            mode='lines',
            line=dict(color='purple', width=8),
            name=f'State Vector (|r|={vector_length:.3f})',
            showlegend=True
        ))
        
        # arrowhead (cone)
        fig.add_trace(go.Cone(
            x=[x], y=[y], z=[z],
            u=[x*0.1], v=[y*0.1], w=[z*0.1],
            colorscale=[[0, 'purple'], [1, 'purple']],
            showscale=False,
            sizemode='absolute',
            sizeref=0.3,
            name='Vector Head',
            showlegend=False
        ))
        
        # point at vector end
        fig.add_trace(go.Scatter3d(
            x=[x], y=[y], z=[z],
            mode='markers',
            marker=dict(size=8, color='purple'),
            name='State Point',
            showlegend=False
        ))
    


    # layout
    fig.update_layout(
        title=dict(text=title, font=dict(size=18)),
        scene=dict(
            xaxis=dict(range=[-1.5, 1.5], title='Y (Imaginary)'),
            yaxis=dict(range=[-1.5, 1.5], title='X (Real)'),
            zaxis=dict(range=[-1.5, 1.5], title='Z (Population)'),
            aspectmode='cube',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        showlegend=True,
        legend=dict(x=0.7, y=0.9),
        height=600,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    return fig

    
    # from mpl_toolkits.mplot3d import Axes3D
    # 
    # fig = plt.figure(figsize=(8, 8))
    # ax = fig.add_subplot(111, projection='3d')
    # 
    # # the Bloch sphere
    # u = np.linspace(0, 2 * np.pi, 100)
    # v = np.linspace(0, np.pi, 100)
    # x_sphere = np.outer(np.cos(u), np.sin(v))
    # y_sphere = np.outer(np.sin(u), np.sin(v))
    # z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))
    # 
    # ax.plot_surface(x_sphere, y_sphere, z_sphere, color='cyan', alpha=0.1, edgecolor='none')
    # 
    # #equator and meridians
    # theta = np.linspace(0, 2 * np.pi, 100)
    # 
    # # equator (XY plane)
    # ax.plot(np.cos(theta), np.sin(theta), 0, 'gray', alpha=0.3, linewidth=1)
    # 
    # # prime meridian (xz plane)
    # phi = np.linspace(0, np.pi, 100)
    # ax.plot(np.sin(phi), 0, np.cos(phi), 'gray', alpha=0.3, linewidth=1)
    # 
    # # meridian (YZ plane)
    # ax.plot(0, np.sin(phi), np.cos(phi), 'gray', alpha=0.3, linewidth=1)
    # 
    # #coordinate axes
    # axis_length = 1.3
    # 
    # # x axis (red)
    # ax.quiver(0, 0, 0, axis_length, 0, 0, color='red', arrow_length_ratio=0.1, linewidth=2)
    # ax.text(axis_length + 0.1, 0, 0, 'X', fontsize=14, color='red', weight='bold')
    # 
    # # y axis (green) - IMAGINARY COMPONENT
    # ax.quiver(0, 0, 0, 0, axis_length, 0, color='green', arrow_length_ratio=0.1, linewidth=2)
    # ax.text(0, axis_length + 0.1, 0, 'Y', fontsize=14, color='green', weight='bold')
    # 
    # # z axis (blue)
    # ax.quiver(0, 0, 0, 0, 0, axis_length, color='blue', arrow_length_ratio=0.1, linewidth=2)
    # ax.text(0, 0, axis_length + 0.1, 'Z', fontsize=14, color='blue', weight='bold')
    # 
    # # Bloch vector
    # x, y, z = bloch_vector
    # vector_length = np.sqrt(x**2 + y**2 + z**2)
    # 
    # if vector_length > 0.01:  # if vector is significant
    #     # Draw vector as arrow
    #     ax.quiver(0, 0, 0, x, y, z, color='purple', arrow_length_ratio=0.15, linewidth=3)
    #     
    #     # Draw point at end of vector
    #     ax.scatter([x], [y], [z], color='purple', s=100, marker='o')
    #     
    #     # Add vector length annotation
    #     ax.text(x * 1.1, y * 1.1, z * 1.1, 
    #             f'|r|={vector_length:.3f}',
    #             fontsize=10, color='purple', weight='bold')
    # 
    # # labels states
    # ax.text(0, 0, 1.4, '|0⟩', fontsize=12, ha='center')
    # ax.text(0, 0, -1.4, '|1⟩', fontsize=12, ha='center')
    # ax.text(1.4, 0, 0, '|+⟩', fontsize=12, ha='center')
    # ax.text(-1.4, 0, 0, '|-⟩', fontsize=12, ha='center')
    # ax.text(0, 1.4, 0, '|+i⟩', fontsize=12, ha='center')
    # ax.text(0, -1.4, 0, '|-i⟩', fontsize=12, ha='center')
    # 
    # # set equal aspect ratio and lkmits
    # ax.set_xlim([-1.5, 1.5])
    # ax.set_ylim([-1.5, 1.5])
    # ax.set_zlim([-1.5, 1.5])
    # ax.set_box_aspect([1, 1, 1])
    # 
    # if show_axes_labels:
    #     ax.set_xlabel('X (Real)', fontsize=10)
    #     ax.set_ylabel('Y (Imaginary)', fontsize=10)
    #     ax.set_zlabel('Z (Population)', fontsize=10)
    # 
    # ax.set_title(title, fontsize=14, weight='bold')
    # 
    # # set viewing angle for better perspective
    # ax.view_init(elev=20, azim=45)
    # 
    # plt.tight_layout()
    # 
    # return fig


def reorder_statevector_to_big_endian(statevector, num_qubits):
    dim = 2 ** num_qubits
    reordered = np.zeros(dim, dtype=complex)
    
    for i in range(dim):
        bits_little = format(i, f'0{num_qubits}b')
        bits_big = bits_little[::-1]
        j = int(bits_big, 2)
        reordered[j] = statevector[i]
    
    return reordered




# ====================================================================================================================================================================
def plot_state_city_big_endian(statevector, num_qubits, title="State City"):
    from mpl_toolkits.mplot3d import Axes3D
    
    sv_big_endian = reorder_statevector_to_big_endian(statevector, num_qubits)
    
    dim = 2 ** num_qubits
    
    real_parts = np.real(sv_big_endian)
    imag_parts = np.imag(sv_big_endian)
    fig = plt.figure(figsize=(14, 7))
    labels = [format(i, f'0{num_qubits}b') for i in range(dim)]
    
    x_pos = np.arange(dim)
    width = 0.35
    
    # 3D axes
    ax = fig.add_subplot(111, projection='3d')
    
    # real parts (red bars)
    for i, (x, real) in enumerate(zip(x_pos, real_parts)):
        if abs(real) > 1e-10:  # plot non zero values
            color = 'red' if real > 0 else 'darkred'
            ax.bar3d(x - width/2, 0, 0, width, 0.5, real, 
                    color=color, alpha=0.8, label='Real' if i == 0 else '')
    
    # imaginary parts (blue bars)
    for i, (x, imag) in enumerate(zip(x_pos, imag_parts)):
        if abs(imag) > 1e-10:  # plot non zero values
            color = 'blue' if imag > 0 else 'darkblue'
            ax.bar3d(x - width/2, 1, 0, width, 0.5, imag, 
                    color=color, alpha=0.8, label='Imaginary' if i == 0 else '')
    
    # labels and title
    ax.set_xlabel('Basis State (Big-Endian)', fontsize=12, labelpad=10)
    ax.set_ylabel('Component', fontsize=12, labelpad=10)
    ax.set_zlabel('Amplitude', fontsize=12, labelpad=10)
    ax.set_title(title, fontsize=14, weight='bold', pad=20)
    
    # x axis ticks with state labels
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=9)
    
    # y axis ticks
    ax.set_yticks([0.25, 1.25])
    ax.set_yticklabels(['Real', 'Imag'], fontsize=10)
    ax.view_init(elev=25, azim=45)
    
    # grid
    ax.grid(True, alpha=0.3)
    
    #legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='red', alpha=0.8, label='Real (positive)'),
        Patch(facecolor='darkred', alpha=0.8, label='Real (negative)'),
        Patch(facecolor='blue', alpha=0.8, label='Imaginary (positive)'),
        Patch(facecolor='darkblue', alpha=0.8, label='Imaginary (negative)')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=9)
    
    plt.tight_layout()
    
    return fig
