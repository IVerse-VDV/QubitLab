"""
gates.py
Defines quantum gate operations and circuit building functions.
Supports 1, 2, and 3 qubit circuits with various gate operations.
"""

from qiskit import QuantumCircuit







def apply_pauli_x(circuit, qubit):
    circuit.x(qubit)


def apply_pauli_y(circuit, qubit):
    circuit.y(qubit)


def apply_pauli_z(circuit, qubit):
    circuit.z(qubit)


def apply_hadamard(circuit, qubit):
    circuit.h(qubit)


def apply_cnot(circuit, control, target):
    circuit.cx(control, target)


def apply_toffoli(circuit, control1, control2, target):
    circuit.ccx(control1, control2, target)


def apply_swap(circuit, qubit1, qubit2):
    circuit.swap(qubit1, qubit2)


def apply_s_gate(circuit, qubit):
    circuit.s(qubit)


def apply_t_gate(circuit, qubit):
    circuit.t(qubit)









# gate availability based on qubit count (defined before create_circuit)
AVAILABLE_GATES = {
    1: ['H', 'X', 'Y', 'Z', 'S', 'T'],
    2: ['H', 'X', 'Y', 'Z', 'S', 'T', 'CNOT', 'SWAP'],
    3: ['H', 'X', 'Y', 'Z', 'S', 'T', 'CNOT', 'SWAP', 'Toffoli']
}





def create_circuit(num_qubits, gate_sequence):
    # create circuit with specified qubits
    circuit = QuantumCircuit(num_qubits)
    
    # apply each gate in the sequence
    for gate_info in gate_sequence:
        gate_name = gate_info[0]
        
        if gate_name == 'H':
            apply_hadamard(circuit, gate_info[1])
        elif gate_name == 'X':
            apply_pauli_x(circuit, gate_info[1])
        elif gate_name == 'Y':
            apply_pauli_y(circuit, gate_info[1])
        elif gate_name == 'Z':
            apply_pauli_z(circuit, gate_info[1])
        elif gate_name == 'S':
            apply_s_gate(circuit, gate_info[1])
        elif gate_name == 'T':
            apply_t_gate(circuit, gate_info[1])
        elif gate_name == 'CNOT' and num_qubits >= 2:
            control, target = gate_info[1]
            apply_cnot(circuit, control, target)
        elif gate_name == 'SWAP' and num_qubits >= 2:
            qubit1, qubit2 = gate_info[1]
            apply_swap(circuit, qubit1, qubit2)
        elif gate_name == 'Toffoli' and num_qubits >= 3:
            control1, control2, target = gate_info[1]
            apply_toffoli(circuit, control1, control2, target)
    
    # sv
    circuit.save_statevector()
    
    return circuit





def get_gate_description(gate_name):
    descriptions = {
        'H': 'Hadamard - Creates superposition',
        'X': 'Pauli-X - Bit flip (NOT gate)',
        'Y': 'Pauli-Y - Bit and phase flip',
        'Z': 'Pauli-Z - Phase flip',
        'S': 'S Gate - Phase gate (√Z)',
        'T': 'T Gate - π/8 phase gate',
        'CNOT': 'CNOT - Controlled-NOT gate',
        'SWAP': 'SWAP - Exchange two qubits',
        'Toffoli': 'Toffoli - Controlled-Controlled-NOT (CCNOT)'
    }
    return descriptions.get(gate_name, 'Unknown gate')