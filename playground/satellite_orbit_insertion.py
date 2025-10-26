"""
人工衛星の軌道投入シミュレーション

種子島宇宙センター（北緯30.4度）から打ち上げられる人工衛星が、
2段階の噴射により目標の円軌道に投入される様子をシミュレートします。

物理モデル:
- 2次元平面（地球中心座標系）
- 万有引力のみ考慮（空気抵抗なし）
- 第1噴射: 楕円軌道への投入
- 第2噴射: 遠地点での円軌道化
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
from matplotlib import patches

# フォント設定
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

# 物理定数
G = 6.674e-11  # 万有引力定数 [m^3/kg/s^2]
M_EARTH = 5.972e24  # 地球の質量 [kg]
R_EARTH = 6.371e6  # 地球の半径 [m]
GM = G * M_EARTH  # 重力定数 [m^3/s^2]

# シミュレーション設定
TANEGASHIMA_LAT = 30.4  # 種子島の緯度 [度]
INITIAL_ALTITUDE = 100e3  # 初期高度 [m]（地表+100km）
TARGET_ALTITUDE = 400e3  # 目標軌道高度 [m]（地表+400km）
DT = 10.0  # タイムステップ [秒]

class SatelliteSimulation:
    """人工衛星の軌道シミュレーションクラス"""
    
    def __init__(self):
        # 初期位置（種子島の緯度、高度100km）
        r0 = R_EARTH + INITIAL_ALTITUDE
        lat_rad = np.radians(TANEGASHIMA_LAT)
        
        # 初期位置ベクトル（2D: x-y平面）
        self.x = r0 * np.cos(lat_rad)
        self.y = r0 * np.sin(lat_rad)
        
        # 地球の自転速度を初速度に追加
        omega_earth = 2 * np.pi / 86400  # 地球の角速度 [rad/s]
        v_rotation = omega_earth * r0 * np.cos(lat_rad)
        
        # 初期速度（地球の自転による速度のみ）
        self.vx = -v_rotation * np.sin(lat_rad)
        self.vy = v_rotation * np.cos(lat_rad)
        
        # 軌道パラメータ
        self.r_target = R_EARTH + TARGET_ALTITUDE
        self.r_initial = r0
        
        # 履歴保存
        self.trajectory_x = [self.x]
        self.trajectory_y = [self.y]
        self.time = [0.0]
        
        # フェーズ管理
        self.phase = 0  # 0: 打ち上げ前, 1: 楕円軌道, 2: 円軌道
        self.apogee_reached = False
        
    def calculate_delta_v_1(self):
        """第1噴射のΔvを計算（楕円軌道投入）"""
        # 楕円軌道の近地点速度
        a = (self.r_initial + self.r_target) / 2  # 半長軸
        v_perigee = np.sqrt(GM * (2 / self.r_initial - 1 / a))
        
        # 現在の速度の大きさ
        v_current = np.sqrt(self.vx**2 + self.vy**2)
        
        # 必要なΔv（軌道接線方向に加速）
        delta_v = v_perigee - v_current
        
        return delta_v
    
    def calculate_delta_v_2(self):
        """第2噴射のΔvを計算（円軌道化）"""
        # 円軌道速度
        v_circular = np.sqrt(GM / self.r_target)
        
        # 楕円軌道の遠地点速度
        a = (self.r_initial + self.r_target) / 2
        v_apogee = np.sqrt(GM * (2 / self.r_target - 1 / a))
        
        # 必要なΔv
        delta_v = v_circular - v_apogee
        
        return delta_v
    
    def apply_burn_1(self):
        """第1噴射を実行"""
        # 速度ベクトルの方向（接線方向）
        vx, vy = self.vx, self.vy
        v_mag = np.sqrt(vx**2 + vy**2)
        
        if v_mag > 0:
            # 接線方向の単位ベクトル
            v_unit_x = vx / v_mag
            v_unit_y = vy / v_mag
            
            # Δvを計算して速度に追加
            delta_v = self.calculate_delta_v_1()
            self.vx += delta_v * v_unit_x
            self.vy += delta_v * v_unit_y
            
            self.phase = 1
            print(f"第1噴射完了: Δv = {delta_v:.2f} m/s")
    
    def apply_burn_2(self):
        """第2噴射を実行"""
        # 速度ベクトルの方向
        vx, vy = self.vx, self.vy
        v_mag = np.sqrt(vx**2 + vy**2)
        
        if v_mag > 0:
            # 接線方向の単位ベクトル
            v_unit_x = vx / v_mag
            v_unit_y = vy / v_mag
            
            # Δvを計算して速度に追加
            delta_v = self.calculate_delta_v_2()
            self.vx += delta_v * v_unit_x
            self.vy += delta_v * v_unit_y
            
            self.phase = 2
            print(f"第2噴射完了: Δv = {delta_v:.2f} m/s")
    
    def step(self, t):
        """1ステップの時間発展"""
        # 現在の位置からの距離
        r = np.sqrt(self.x**2 + self.y**2)
        
        # 重力加速度
        ax = -GM * self.x / r**3
        ay = -GM * self.y / r**3
        
        # 速度と位置を更新（Euler法）
        self.vx += ax * DT
        self.vy += ay * DT
        self.x += self.vx * DT
        self.y += self.vy * DT
        
        # 履歴を保存
        self.trajectory_x.append(self.x)
        self.trajectory_y.append(self.y)
        self.time.append(t)
        
        # フェーズ管理
        if self.phase == 1 and not self.apogee_reached:
            # 遠地点到達判定（速度の半径方向成分が負→正に変わる）
            r_vec_x, r_vec_y = self.x, self.y
            v_radial = (r_vec_x * self.vx + r_vec_y * self.vy) / r
            
            if r > self.r_target * 0.98 and v_radial > 0:
                self.apogee_reached = True
                self.apply_burn_2()

def create_animation(sim, max_time=10000):
    """アニメーションを作成"""
    fig, ax = plt.subplots(figsize=(12, 12))
    
    # Draw Earth
    earth = Circle((0, 0), R_EARTH, color='blue', alpha=0.7, label='Earth')
    ax.add_patch(earth)
    
    # Draw target orbit
    target_orbit = Circle((0, 0), sim.r_target, fill=False,
                          color='green', linestyle='--', linewidth=2,
                          label=f'Target Orbit ({TARGET_ALTITUDE/1000:.0f} km)')
    ax.add_patch(target_orbit)
    
    # Tanegashima location
    lat_rad = np.radians(TANEGASHIMA_LAT)
    tanegashima_x = R_EARTH * np.cos(lat_rad)
    tanegashima_y = R_EARTH * np.sin(lat_rad)
    ax.plot(tanegashima_x, tanegashima_y, 'r*', markersize=15, label='Tanegashima')
    
    # Trajectory and satellite
    trajectory_line, = ax.plot([], [], 'r-', linewidth=1, alpha=0.6, label='Trajectory')
    satellite, = ax.plot([], [], 'ro', markersize=8, label='Satellite')
    
    # テキスト表示
    info_text = ax.text(0.02, 0.98, '', transform=ax.transAxes,
                       verticalalignment='top', fontsize=12,
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # 軸の設定
    limit = sim.r_target * 1.3
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('X [m]', fontsize=12)
    ax.set_ylabel('Y [m]', fontsize=12)
    ax.set_title('Satellite Orbit Insertion Simulation', fontsize=16, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    
    # シミュレーション実行
    t = 0
    step_count = 0
    
    # 第1噴射
    sim.apply_burn_1()
    
    def init():
        trajectory_line.set_data([], [])
        satellite.set_data([], [])
        info_text.set_text('')
        return trajectory_line, satellite, info_text
    
    def animate(frame):
        nonlocal t, step_count
        
        # シミュレーションを進める
        for _ in range(5):  # 1フレームで5ステップ進める
            if t < max_time:
                sim.step(t)
                t += DT
                step_count += 1
        
        # 描画更新
        trajectory_line.set_data(sim.trajectory_x, sim.trajectory_y)
        satellite.set_data([sim.x], [sim.y])
        
        # 情報テキスト
        r = np.sqrt(sim.x**2 + sim.y**2)
        altitude = (r - R_EARTH) / 1000  # km
        v = np.sqrt(sim.vx**2 + sim.vy**2)
        
        phase_name = ['Launch Ready', 'Elliptical Orbit', 'Circular Orbit'][sim.phase]
        
        info = f'Time: {t:.0f} sec ({t/60:.1f} min)\n'
        info += f'Altitude: {altitude:.1f} km\n'
        info += f'Velocity: {v:.1f} m/s\n'
        info += f'Phase: {phase_name}'
        info_text.set_text(info)
        
        return trajectory_line, satellite, info_text
    
    # アニメーション作成
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                  frames=400, interval=50, blit=True)
    
    return fig, anim

def main():
    """メイン実行関数"""
    print("=" * 60)
    print("人工衛星軌道投入シミュレーション")
    print("=" * 60)
    print(f"打ち上げ地点: 種子島宇宙センター（北緯{TANEGASHIMA_LAT}度）")
    print(f"初期高度: {INITIAL_ALTITUDE/1000:.0f} km")
    print(f"目標軌道高度: {TARGET_ALTITUDE/1000:.0f} km")
    print(f"タイムステップ: {DT:.1f} 秒")
    print("=" * 60)
    
    # シミュレーション実行
    sim = SatelliteSimulation()
    
    # 理論値の計算
    print("\n理論値:")
    print(f"第1噴射 Δv: {sim.calculate_delta_v_1():.2f} m/s")
    print(f"第2噴射 Δv: {sim.calculate_delta_v_2():.2f} m/s")
    
    v_circular = np.sqrt(GM / sim.r_target)
    orbital_period = 2 * np.pi * sim.r_target / v_circular
    print(f"目標円軌道速度: {v_circular:.2f} m/s")
    print(f"軌道周期: {orbital_period/60:.1f} 分")
    print("\n" + "=" * 60)
    
    # アニメーション作成
    print("\nアニメーションを作成中...")
    fig, anim = create_animation(sim, max_time=orbital_period * 1.5)
    
    # HTMLファイルとして保存（WSL対応）
    html_output = 'satellite_orbit_insertion.html'
    print(f"\nアニメーションを {html_output} に保存中...")
    
    from matplotlib.animation import HTMLWriter
    writer = HTMLWriter(fps=20, embed_frames=True, default_mode='loop')
    anim.save(html_output, writer=writer, dpi=100)
    
    # Add UTF-8 encoding to HTML file
    with open(html_output, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Add meta tag for UTF-8
    if '<head>' in html_content and 'charset' not in html_content:
        html_content = html_content.replace('<head>', '<head>\n    <meta charset="UTF-8">')
    
    with open(html_output, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ {html_output} に保存しました（UTF-8エンコーディング）")
    print(f"ブラウザで {html_output} を開いてアニメーションを確認してください")
    
    print("\n" + "=" * 60)
    print("シミュレーション完了")
    print("=" * 60)

if __name__ == "__main__":
    main()