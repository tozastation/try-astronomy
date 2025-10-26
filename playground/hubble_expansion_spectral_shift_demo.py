"""
hubble_expansion_spectral_shift_demo.py

宇宙膨張による吸収線シフトのデモンストレーション
ハッブル-ルメートルの法則を用いて、異なる観測者から見た
銀河のスペクトル線がどのように観測されるかを可視化する。

Author: Astronomy Student
Date: 2025-10-26
"""

import numpy as np
import matplotlib.pyplot as plt
from astropy import units as u
from astropy.cosmology import FlatLambdaCDM
from astropy import constants as const

# 日本語フォントの設定
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 宇宙論パラメータ（簡単のためハッブル定数のみ使用）
H0 = 70 * u.km / u.s / u.Mpc  # ハッブル定数

# 銀河の配置（単位距離Dを100 Mpcとする）
D = 100 * u.Mpc
distances = {
    'Milky Way': 0 * u.Mpc,
    'Galaxy A': D,
    'Galaxy B': 3 * D
}

# 静止波長（例：水素のHα線）
lambda_rest = 656.3 * u.nm

def calculate_redshift_velocity(distance, H0):
    """ハッブル-ルメートルの法則から後退速度を計算"""
    v = H0 * distance
    return v.to(u.km / u.s)

def doppler_shift(lambda_rest, velocity):
    """ドップラーシフトによる観測波長を計算（非相対論的近似）"""
    z = velocity / const.c.to(u.km / u.s)
    lambda_obs = lambda_rest * (1 + z)
    return lambda_obs

def plot_spectra_from_observer(observer_name, observer_distance, fig_num):
    """指定された観測者から見たスペクトルをプロット"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 各銀河のスペクトルを計算
    galaxy_names = ['Galaxy A', 'Milky Way', 'Galaxy B']
    colors = ['blue', 'green', 'red']
    
    for i, (name, color) in enumerate(zip(galaxy_names, colors)):
        # 観測者から対象銀河までの距離
        relative_distance = abs(distances[name] - observer_distance)
        
        # ハッブル-ルメートルの法則で後退速度を計算
        velocity = calculate_redshift_velocity(relative_distance, H0)
        
        # ドップラーシフト後の波長
        lambda_obs = doppler_shift(lambda_rest, velocity)
        
        # スペクトル線を描画（簡略化した吸収線）
        wavelengths = np.linspace(650, 670, 1000) * u.nm
        intensity = np.ones_like(wavelengths.value)
        
        # ガウス型の吸収線
        absorption_width = 0.5 * u.nm
        absorption = np.exp(-((wavelengths - lambda_obs)**2 / (2 * absorption_width**2)).value)
        intensity = intensity - 0.8 * absorption
        
        # プロット（縦にオフセット）
        offset = (2 - i) * 0.3
        ax.plot(wavelengths, intensity + offset, color=color, linewidth=1.5, label=name)
        ax.axvline(lambda_obs.value, color=color, linestyle='--', alpha=0.3, linewidth=2)
        
        # 情報表示
        print(f"\n{observer_name}から見た{name}:")
        print(f"  距離: {relative_distance:.1f}")
        print(f"  後退速度: {velocity:.1f}")
        print(f"  観測波長: {lambda_obs:.2f}")
        print(f"  赤方偏移: Δλ = {(lambda_obs - lambda_rest).to(u.nm):.2f}")
    
    # 静止波長の参照線
    ax.axvline(lambda_rest.value, color='black', linestyle=':', 
               linewidth=1, label=f'Rest wavelength ({lambda_rest:.1f})')
    
    ax.set_xlabel('Wavelength (nm)', fontsize=12)
    ax.set_ylabel('Relative Intensity (offset)', fontsize=12)
    ax.set_title(f'Observed Spectra from {observer_name}', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right')
    ax.set_ylim(0, 1.2)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

# 図2: 天の川銀河からの観測
print("="*60)
print("図2: 天の川銀河からの観測")
print("="*60)
fig2 = plot_spectra_from_observer('Milky Way', distances['Milky Way'], 2)

# 図③: 銀河Aからの観測
print("\n" + "="*60)
print("図③: 銀河Aからの観測")
print("="*60)
fig3 = plot_spectra_from_observer('Galaxy A', distances['Galaxy A'], 3)

# ハッブル図（距離-速度関係）を追加
fig4, ax4 = plt.subplots(figsize=(8, 6))

# 天の川銀河から見た場合
distances_mw = [0, D.value, 3*D.value]
velocities_mw = [calculate_redshift_velocity(d*u.Mpc, H0).value for d in distances_mw]
ax4.scatter(distances_mw, velocities_mw, s=100, color='green', 
           label='From Milky Way', zorder=3)

# 銀河Aから見た場合
distances_ga = [D.value, 0, 2*D.value]
velocities_ga = [calculate_redshift_velocity(d*u.Mpc, H0).value for d in distances_ga]
ax4.scatter(distances_ga, velocities_ga, s=100, color='blue', 
           marker='s', label='From Galaxy A', zorder=3)

# ハッブル則の直線
d_range = np.linspace(0, 350, 100)
v_range = (H0.value * d_range)
ax4.plot(d_range, v_range, 'k--', alpha=0.5, label=f'Hubble Law (H₀={H0.value} km/s/Mpc)')

ax4.set_xlabel('Distance (Mpc)', fontsize=12)
ax4.set_ylabel('Recession Velocity (km/s)', fontsize=12)
ax4.set_title('Hubble-Lemaitre Law: Distance vs Velocity', fontsize=14, fontweight='bold')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()

# 図を保存（WSL環境対応）
output_dir = "output"
import os
os.makedirs(output_dir, exist_ok=True)

fig2.savefig(f"{output_dir}/fig2_milky_way_observation.png", dpi=150, bbox_inches='tight')
fig3.savefig(f"{output_dir}/fig3_galaxy_a_observation.png", dpi=150, bbox_inches='tight')
fig4.savefig(f"{output_dir}/fig4_hubble_diagram.png", dpi=150, bbox_inches='tight')

print(f"\n図を '{output_dir}/' ディレクトリに保存しました:")
print(f"  - fig2_milky_way_observation.png")
print(f"  - fig3_galaxy_a_observation.png")
print(f"  - fig4_hubble_diagram.png")

# GUIが使える環境なら表示を試みる
try:
    plt.show()
except:
    print("\n(GUIディスプレイが利用できないため、ファイルのみ保存されました)")

print("\n" + "="*60)
print("重要なポイント:")
print("="*60)
print("1. ハッブル-ルメートルの法則: v = H₀ × d")
print("2. どの銀河から見ても、他の銀河は距離に比例して遠ざかる")
print("3. 観測者が変わると、各銀河までの距離が変わる")
print("4. 距離が変わると後退速度が変わり、吸収線の位置が変わる")