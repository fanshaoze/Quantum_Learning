import numpy as np
import matplotlib.pyplot as plt
from qutip import *

# --- 参数设置 ---
N = 5                # 截断维度
alpha = -2 * np.pi * 0.250  # 非谐性 
tg = 20              # 脉冲总时长 (ns)
times = np.linspace(0, tg, 500)

# 算符
a = destroy(N)
n_op = num(N)
H0 = (alpha / 2) * a.dag() * a.dag() * a * a  

# --- 脉冲波形定义 (高斯脉冲) ---
def pulse_shape(t, args):
    sigma = args['tg'] / 4
    t0 = args['tg'] / 2
    # 归一化高斯包络
    return np.exp(-(t - t0)**2 / (2 * sigma**2))

# 驱动项算符
H_drive = (a + a.dag())

# --- 求解 Pi 脉冲幅度 ---
# 为了实现翻转，需要积分强度满足 \int \Omega(t) dt = \pi
# 对于高斯脉冲 \int exp(-t^2/2sigma^2) dt = sigma * sqrt(2*pi)
sigma_val = tg / 4
amplitude = np.pi / (sigma_val * np.sqrt(2 * np.pi))

# 总 Hamiltonian: [H0, [H_drive, pulse_shape_func]]
H = [H0, [H_drive, pulse_shape]]

# --- 演化 ---
psi0 = basis(N, 0)


result = mesolve(H, psi0, times, [], args={'tg': tg})

# --- 结果分析 ---
p0 = expect(basis(N, 0).proj(), result.states)
p1 = expect(basis(N, 1).proj(), result.states)
p2 = expect(basis(N, 2).proj(), result.states)

# 可视化
plt.figure(figsize=(8, 5))
plt.plot(times, p0, label='State 0')
plt.plot(times, p1, label='State 1')
plt.plot(times, p2, label='State 2 (Leakage)')
plt.title("Kerr Oscillator $\pi$-Pulse Evolution")
plt.xlabel("Time (ns)")
plt.ylabel("Population")
plt.legend()
plt.grid(True)
plt.savefig("kerr_oscillator_pi_pulse.png")

print(f"Final Population in |1>: {p1[-1]:.4f}")