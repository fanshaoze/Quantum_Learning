import numpy as np
from scipy.linalg import expm

# 1. 定义系统参数
Delta = 10.0  # Z方向的主能级差 (大)
g = 0.5       # X方向的微扰耦合 (小)

# 定义泡利矩阵
sz = np.array([[1, 0], [0, -1]])
sx = np.array([[0, 1], [1, 0]])

# 2. 构建原始哈密顿量 H = H0 + V
H0 = (Delta / 2) * sz
V = g * sx
H = H0 + V

# 3. 计算 Schrieffer-Wolff 生成元 S
# 满足 [S, H0] = -V
S = (g / Delta) * np.array([[0, 1], [-1, 0]])

# 计算幺正变换矩阵 U = exp(S)
U = expm(S)

# 4. 执行变换
# (A) 精确的幺正变换：H_exact_trans = U * H * U^\dagger (因为 S 是反埃尔米特，exp(-S) 就是 U^\dagger)
H_exact_trans = U @ H @ expm(-S)

# (B) 二阶 SWT 近似有效哈密顿量：H_eff = H0 + 0.5 * [S, V]
commutator_SV = S @ V - V @ S
H_eff_approx = H0 + 0.5 * commutator_SV

# 5. 证明等效性（对比本征值能量）
# 计算原始系统的精确本征值
eigvals_original = np.sort(np.linalg.eigvals(H).real)

# 计算解析解 (理论上 2x2 矩阵的精确特征值是 \pm 0.5 * sqrt(Delta^2 + 4g^2))
eigvals_analytical = np.array([-0.5 * np.sqrt(Delta**2 + 4*g**2), 
                                0.5 * np.sqrt(Delta**2 + 4*g**2)])

print("="*50)
print("哈密顿量矩阵展示：\n")
print(f"原始哈密顿量 H:\n{H}\n")
print(f"幺正变换后的精确哈密顿量 (应趋于对角化):\n{np.round(H_exact_trans, 5)}\n")
print(f"SWT 二阶近似有效哈密顿量 H_eff_approx:\n{H_eff_approx}\n")

print("="*50)
print("等效性证明 (能量谱对比)：\n")
print(f"1. 原始哈密顿量的精确能级    : {eigvals_original}")
print(f"2. 解析公式计算的精确能级    : {eigvals_analytical}")
print(f"3. 幺正变换后矩阵的对角元素  : {np.sort(np.diag(H_exact_trans).real)}")
print(f"4. SWT 二阶近似矩阵的对角元素: {np.sort(np.diag(H_eff_approx).real)}")
print("="*50)