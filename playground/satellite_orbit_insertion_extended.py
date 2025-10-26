"""
人工衛星の軌道投入シミュレーション（拡張版）

様々な軌道タイプに対応:
- LEO (Low Earth Orbit): 低軌道
- SSO (Sun-Synchronous Orbit): 太陽同期軌道
- GTO (Geostationary Transfer Orbit): 静止トランスファ軌道
- MEO (Medium Earth Orbit): 中軌道

各軌道タイプに応じた打ち上げ条件と軌道要素を考慮します。
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta

# フォント設定
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

# 物理定数
G = 6.674e-11  # 万有引力定数 [m^3/kg/s^2]
M_EARTH = 5.972e24  # 地球の質量 [kg]
R_EARTH = 6.371e6  # 地球の半径 [m]
GM = G * M_EARTH  # 重力定数 [m^3/s^2]
J2 = 1.08263e-3  # 地球の扁平率係数（軌道傾斜角計算用）

# シミュレーション設定
TANEGASHIMA_LAT = 30.4  # 種子島の緯度 [度]
TANEGASHIMA_LON = 131.0  # 種子島の経度 [度]
INITIAL_ALTITUDE = 100e3  # 初期高度 [m]（地表+100km）
DT = 10.0  # タイムステップ [秒]

class OrbitType(Enum):
    """軌道タイプの列挙"""
    LEO = "Low Earth Orbit"
    SSO = "Sun-Synchronous Orbit"
    GTO = "Geostationary Transfer Orbit"
    MEO = "Medium Earth Orbit"

@dataclass
class OrbitParameters:
    """軌道パラメータ"""
    name: str
    target_altitude: float  # 目標高度 [m]
    inclination: float  # 軌道傾斜角 [度]
    apogee_altitude: float = None  # 遠地点高度（GTOなど）[m]
    launch_azimuth: float = None  # 打ち上げ方位角 [度]
    optimal_launch_time: str = None  # 最適打ち上げ時刻の説明
    
    def __post_init__(self):
        """初期化後の処理"""
        if self.apogee_altitude is None:
            self.apogee_altitude = self.target_altitude
        
        # 打ち上げ方位角の計算（軌道傾斜角から）
        if self.launch_azimuth is None:
            self.launch_azimuth = self._calculate_launch_azimuth()
    
    def _calculate_launch_azimuth(self):
        """打ち上げ方位角を計算"""
        # 簡易的な計算: sin(azimuth) = cos(inclination) / cos(latitude)
        lat_rad = np.radians(TANEGASHIMA_LAT)
        inc_rad = np.radians(self.inclination)
        
        cos_azimuth = np.cos(inc_rad) / np.cos(lat_rad)
        
        # 範囲チェック
        if abs(cos_azimuth) > 1.0:
            # 種子島からは到達不可能な軌道傾斜角
            if self.inclination < TANEGASHIMA_LAT:
                return 90.0  # 東向き
            else:
                return 90.0  # 可能な限り東向き
        
        azimuth = np.degrees(np.arcsin(cos_azimuth))
        
        # 逆行軌道の場合は西向き
        if self.inclination > 90:
            azimuth = 180.0 - azimuth
        
        return azimuth

def get_orbit_config(orbit_type: OrbitType) -> OrbitParameters:
    """軌道タイプに応じた設定を返す"""
    configs = {
        OrbitType.LEO: OrbitParameters(
            name="低軌道 (LEO)",
            target_altitude=400e3,  # 400km
            inclination=51.6,  # ISS相当
            optimal_launch_time="昼夜を問わず打ち上げ可能。ただし、ランデブーミッションの場合は目標軌道面通過時刻に合わせる"
        ),
        OrbitType.SSO: OrbitParameters(
            name="太陽同期軌道 (SSO)",
            target_altitude=800e3,  # 800km
            inclination=98.7,  # 太陽同期軌道の典型的な傾斜角
            optimal_launch_time="降交点または昇交点の地方太陽時を維持するため、目標の地方太陽時に合わせて打ち上げ。"
                              "観測衛星では午前10:30または午後13:30が多い"
        ),
        OrbitType.GTO: OrbitParameters(
            name="静止トランスファ軌道 (GTO)",
            target_altitude=35786e3,  # 静止軌道高度
            apogee_altitude=35786e3,
            inclination=28.5,  # ケープカナベラル相当、種子島では約30度
            optimal_launch_time="赤道通過時に遠地点が目標経度上空に来るよう、打ち上げ時刻を調整。"
                              "通常、複数の打ち上げウィンドウが1日に数回存在"
        ),
        OrbitType.MEO: OrbitParameters(
            name="中軌道 (MEO)",
            target_altitude=20200e3,  # GPS軌道相当
            inclination=55.0,  # GPS軌道傾斜角
            optimal_launch_time="目標軌道面通過時刻に合わせて打ち上げ。GPS等の測位衛星では軌道面が複数あり、"
                              "それぞれの軌道面への打ち上げウィンドウが存在"
        ),
    }
    return configs[orbit_type]

def calculate_sso_inclination(altitude):
    """太陽同期軌道の傾斜角を計算"""
    # 太陽同期軌道の条件: dΩ/dt = 360度/年 = 0.9856度/日
    # dΩ/dt = -3/2 * (R_earth/a)^2 * J2 * n * cos(i)
    # n: 平均運動 [rad/s]
    
    a = R_EARTH + altitude  # 軌道半径
    n = np.sqrt(GM / a**3)  # 平均運動
    
    # 0.9856度/日 = 1.991e-7 rad/s
    target_precession = np.radians(0.9856) / 86400
    
    # cos(i) = dΩ/dt / (-3/2 * (R_earth/a)^2 * J2 * n)
    cos_i = target_precession / (-1.5 * (R_EARTH/a)**2 * J2 * n)
    
    if abs(cos_i) > 1.0:
        return None  # この高度では太陽同期軌道は不可能
    
    inclination = np.degrees(np.arccos(cos_i))
    return inclination

class SatelliteSimulationExtended:
    """拡張版人工衛星シミュレーションクラス"""
    
    def __init__(self, orbit_params: OrbitParameters):
        self.orbit_params = orbit_params
        
        # 初期位置（種子島の緯度、高度100km）
        r0 = R_EARTH + INITIAL_ALTITUDE
        lat_rad = np.radians(TANEGASHIMA_LAT)
        
        # 打ち上げ方位角を考慮した初期位置と速度
        azimuth_rad = np.radians(orbit_params.launch_azimuth)
        
        # 初期位置ベクトル（2D平面に投影）
        self.x = r0 * np.cos(lat_rad)
        self.y = r0 * np.sin(lat_rad)
        
        # 地球の自転速度
        omega_earth = 2 * np.pi / 86400  # [rad/s]
        v_rotation = omega_earth * r0 * np.cos(lat_rad)
        
        # 打ち上げ方位角を考慮した初期速度
        # 簡略化: 2D平面での東向き成分のみ考慮
        self.vx = -v_rotation * np.sin(lat_rad)
        self.vy = v_rotation * np.cos(lat_rad)
        
        # 軌道パラメータ
        self.r_target = R_EARTH + orbit_params.target_altitude
        self.r_apogee = R_EARTH + orbit_params.apogee_altitude
        self.r_initial = r0
        
        # 履歴保存
        self.trajectory_x = [self.x]
        self.trajectory_y = [self.y]
        self.time = [0.0]
        
        # フェーズ管理
        self.phase = 0  # 0: 打ち上げ前, 1: トランスファ軌道, 2: 目標軌道
        self.apogee_reached = False
        
    def calculate_delta_v_1(self):
        """第1噴射のΔvを計算（トランスファ軌道投入）"""
        # 楕円軌道の近地点速度
        a = (self.r_initial + self.r_apogee) / 2  # 半長軸
        v_perigee = np.sqrt(GM * (2 / self.r_initial - 1 / a))
        
        # 現在の速度の大きさ
        v_current = np.sqrt(self.vx**2 + self.vy**2)
        
        # 必要なΔv
        delta_v = v_perigee - v_current
        
        return delta_v
    
    def calculate_delta_v_2(self):
        """第2噴射のΔvを計算（目標軌道化）"""
        # 目標軌道速度
        v_target = np.sqrt(GM / self.r_target)
        
        # トランスファ軌道の遠地点速度
        a = (self.r_initial + self.r_apogee) / 2
        v_apogee = np.sqrt(GM * (2 / self.r_apogee - 1 / a))
        
        # 必要なΔv
        delta_v = v_target - v_apogee
        
        return delta_v
    
    def apply_burn_1(self):
        """第1噴射を実行"""
        vx, vy = self.vx, self.vy
        v_mag = np.sqrt(vx**2 + vy**2)
        
        if v_mag > 0:
            v_unit_x = vx / v_mag
            v_unit_y = vy / v_mag
            
            delta_v = self.calculate_delta_v_1()
            self.vx += delta_v * v_unit_x
            self.vy += delta_v * v_unit_y
            
            self.phase = 1
            print(f"第1噴射完了: Δv = {delta_v:.2f} m/s")
    
    def apply_burn_2(self):
        """第2噴射を実行"""
        vx, vy = self.vx, self.vy
        v_mag = np.sqrt(vx**2 + vy**2)
        
        if v_mag > 0:
            v_unit_x = vx / v_mag
            v_unit_y = vy / v_mag
            
            delta_v = self.calculate_delta_v_2()
            self.vx += delta_v * v_unit_x
            self.vy += delta_v * v_unit_y
            
            self.phase = 2
            print(f"第2噴射完了: Δv = {delta_v:.2f} m/s")
    
    def step(self, t):
        """1ステップの時間発展"""
        r = np.sqrt(self.x**2 + self.y**2)
        
        # 重力加速度
        ax = -GM * self.x / r**3
        ay = -GM * self.y / r**3
        
        # 速度と位置を更新
        self.vx += ax * DT
        self.vy += ay * DT
        self.x += self.vx * DT
        self.y += self.vy * DT
        
        # 履歴を保存
        self.trajectory_x.append(self.x)
        self.trajectory_y.append(self.y)
        self.time.append(t)
        
        # 遠地点到達判定
        if self.phase == 1 and not self.apogee_reached:
            r_vec_x, r_vec_y = self.x, self.y
            v_radial = (r_vec_x * self.vx + r_vec_y * self.vy) / r
            
            if r > self.r_apogee * 0.98 and v_radial > 0:
                self.apogee_reached = True
                self.apply_burn_2()

def create_animation_extended(sim, max_time=10000):
    """拡張版アニメーション作成"""
    fig, ax = plt.subplots(figsize=(12, 12))
    
    # Draw Earth
    earth = Circle((0, 0), R_EARTH, color='blue', alpha=0.7, label='Earth')
    ax.add_patch(earth)
    
    # Draw target orbit
    target_orbit = Circle((0, 0), sim.r_target, fill=False,
                          color='green', linestyle='--', linewidth=2,
                          label=f'Target Orbit ({sim.orbit_params.target_altitude/1000:.0f} km)')
    ax.add_patch(target_orbit)
    
    # Transfer orbit apogee (for GTO)
    if sim.r_apogee != sim.r_target:
        apogee_orbit = Circle((0, 0), sim.r_apogee, fill=False,
                             color='orange', linestyle=':', linewidth=2,
                             label=f'Apogee ({sim.orbit_params.apogee_altitude/1000:.0f} km)')
        ax.add_patch(apogee_orbit)
    
    # Tanegashima location
    lat_rad = np.radians(TANEGASHIMA_LAT)
    tanegashima_x = R_EARTH * np.cos(lat_rad)
    tanegashima_y = R_EARTH * np.sin(lat_rad)
    ax.plot(tanegashima_x, tanegashima_y, 'r*', markersize=15, label='Tanegashima')
    
    # Trajectory and satellite
    trajectory_line, = ax.plot([], [], 'r-', linewidth=1, alpha=0.6, label='Trajectory')
    satellite, = ax.plot([], [], 'ro', markersize=8, label='Satellite')
    
    # Info text
    info_text = ax.text(0.02, 0.98, '', transform=ax.transAxes,
                       verticalalignment='top', fontsize=10,
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Axis settings
    limit = max(sim.r_target, sim.r_apogee) * 1.3
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('X [m]', fontsize=12)
    ax.set_ylabel('Y [m]', fontsize=12)
    ax.set_title(f'Satellite Orbit Insertion: {sim.orbit_params.name}',
                fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=9)
    
    # シミュレーション実行
    t = 0
    sim.apply_burn_1()
    
    def init():
        trajectory_line.set_data([], [])
        satellite.set_data([], [])
        info_text.set_text('')
        return trajectory_line, satellite, info_text
    
    def animate(frame):
        nonlocal t
        
        for _ in range(5):
            if t < max_time:
                sim.step(t)
                t += DT
        
        trajectory_line.set_data(sim.trajectory_x, sim.trajectory_y)
        satellite.set_data([sim.x], [sim.y])
        
        r = np.sqrt(sim.x**2 + sim.y**2)
        altitude = (r - R_EARTH) / 1000
        v = np.sqrt(sim.vx**2 + sim.vy**2)
        
        phase_names = ['Ready', 'Transfer Orbit', 'Target Orbit']
        
        info = f'Orbit Type: {sim.orbit_params.name}\n'
        info += f'Time: {t:.0f} sec ({t/60:.1f} min)\n'
        info += f'Altitude: {altitude:.1f} km\n'
        info += f'Velocity: {v:.1f} m/s\n'
        info += f'Inclination: {sim.orbit_params.inclination:.1f}°\n'
        info += f'Launch Azimuth: {sim.orbit_params.launch_azimuth:.1f}°\n'
        info += f'Phase: {phase_names[sim.phase]}'
        info_text.set_text(info)
        
        return trajectory_line, satellite, info_text
    
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                  frames=400, interval=50, blit=True)
    
    return fig, anim

def print_orbit_info(orbit_params: OrbitParameters):
    """軌道情報を表示"""
    print("=" * 70)
    print(f"軌道タイプ: {orbit_params.name}")
    print("=" * 70)
    print(f"目標高度: {orbit_params.target_altitude/1000:.0f} km")
    print(f"軌道傾斜角: {orbit_params.inclination:.1f}°")
    print(f"打ち上げ方位角: {orbit_params.launch_azimuth:.1f}°")
    
    if orbit_params.apogee_altitude != orbit_params.target_altitude:
        print(f"遠地点高度: {orbit_params.apogee_altitude/1000:.0f} km")
    
    print(f"\n最適打ち上げ条件:")
    print(f"  {orbit_params.optimal_launch_time}")
    
    # 軌道周期の計算
    a = R_EARTH + orbit_params.target_altitude
    v = np.sqrt(GM / a)
    period = 2 * np.pi * a / v
    print(f"\n目標軌道の周期: {period/60:.1f} 分 ({period/3600:.2f} 時間)")
    print(f"軌道速度: {v:.2f} m/s")
    
    # 太陽同期軌道の場合、計算値と比較
    if "太陽同期" in orbit_params.name:
        calculated_inc = calculate_sso_inclination(orbit_params.target_altitude)
        if calculated_inc:
            print(f"\n太陽同期軌道の理論傾斜角: {calculated_inc:.2f}°")
            print(f"設定値との差: {abs(calculated_inc - orbit_params.inclination):.2f}°")
    
    print("=" * 70)

def main():
    """メイン実行関数"""
    print("\n人工衛星軌道投入シミュレーション（拡張版）\n")
    
    # 利用可能な軌道タイプを表示
    print("利用可能な軌道タイプ:")
    for i, orbit_type in enumerate(OrbitType, 1):
        print(f"  {i}. {orbit_type.value}")
    
    print("\nデフォルトで全ての軌道タイプのシミュレーションを実行します")
    print("特定の軌道のみ実行する場合は、コード内で選択してください\n")
    
    # 各軌道タイプでシミュレーション
    orbit_types_to_simulate = [OrbitType.SSO, OrbitType.GTO]  # 例: SSOとGTOのみ
    # orbit_types_to_simulate = list(OrbitType)  # 全軌道タイプ
    
    for orbit_type in orbit_types_to_simulate:
        orbit_params = get_orbit_config(orbit_type)
        print_orbit_info(orbit_params)
        
        # シミュレーション実行
        sim = SatelliteSimulationExtended(orbit_params)
        
        print("\n理論的なΔv:")
        print(f"  第1噴射: {sim.calculate_delta_v_1():.2f} m/s")
        print(f"  第2噴射: {sim.calculate_delta_v_2():.2f} m/s")
        print(f"  合計Δv: {sim.calculate_delta_v_1() + sim.calculate_delta_v_2():.2f} m/s")
        
        # 軌道周期に応じたシミュレーション時間
        orbital_period = 2 * np.pi * sim.r_target / np.sqrt(GM / sim.r_target)
        max_time = min(orbital_period * 1.5, 20000)  # 最大20000秒
        
        print(f"\nアニメーション作成中...")
        fig, anim = create_animation_extended(sim, max_time=max_time)
        
        # HTMLファイルとして保存
        html_output = f'satellite_orbit_{orbit_type.name.lower()}.html'
        print(f"  {html_output} に保存中...")
        
        from matplotlib.animation import HTMLWriter
        writer = HTMLWriter(fps=20, embed_frames=True, default_mode='loop')
        anim.save(html_output, writer=writer, dpi=100)
        
        # UTF-8エンコーディング追加
        with open(html_output, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        if '<head>' in html_content and 'charset' not in html_content:
            html_content = html_content.replace('<head>', '<head>\n    <meta charset="UTF-8">')
        
        with open(html_output, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"  ✓ {html_output} に保存しました\n")
        plt.close(fig)
    
    print("=" * 70)
    print("全シミュレーション完了")
    print("=" * 70)

if __name__ == "__main__":
    main()