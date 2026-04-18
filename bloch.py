import numpy as np
import qutip as qt

def bloch_from_dm(rho):
    """从密度矩阵提取Bloch向量"""
    rx = qt.expect(qt.sigmax(), rho)
    ry = qt.expect(qt.sigmay(), rho)
    rz = qt.expect(qt.sigmaz(), rho)
    return np.array([rx, ry, rz])


def dm_from_bloch(rx, ry, rz):
    """从Bloch向量构建密度矩阵"""
    rho = 0.5 * (
        qt.qeye(2)
        + rx * qt.sigmax()
        + ry * qt.sigmay()
        + rz * qt.sigmaz()
    )
    return rho

# 定义态
states = {
    "|0>": qt.basis(2, 0),
    "|1>": qt.basis(2, 1),
    "|+>": (qt.basis(2,0) + qt.basis(2,1)).unit(),
    "|->": (qt.basis(2,0) - qt.basis(2,1)).unit(),
    "|i>": (qt.basis(2,0) + 1j*qt.basis(2,1)).unit(),
    "|-i>": (qt.basis(2,0) - 1j*qt.basis(2,1)).unit(),
    "mixed": qt.qeye(2)/2
}

for name, psi in states.items():
    rho = psi if psi.isoper else qt.ket2dm(psi)
    r = bloch_from_dm(rho)
    rho_reconstructed = dm_from_bloch(*r)

    print(f"{name}: r = {r}")
    print("reconstruction error:",
          (rho - rho_reconstructed).norm())
    print()

from qutip import Bloch

b = Bloch()

for name, psi in states.items():
    rho = psi if psi.isoper else qt.ket2dm(psi)
    r = bloch_from_dm(rho)
    b.add_points(r)

b.show()