# --- Ve = Isp * g0 の関係式の導出 ---
#
# この関係は、物理量「力積」と「比推力」の定義から導かれます。
#
# 1. 推力 (Thrust, F) と噴射速度 (Ve)
#    ロケットの推力Fは、単位時間あたりに噴射する質量(ṁ)と噴射速度Veの積で表されます。
#    F = ṁ * Ve  (ṁは質量流量 [kg/s])
#
# 2. 全力積 (Total Impulse)
#    燃焼時間(t)全体で得られる力積は、推力Fと燃焼時間tの積です。
#    Total Impulse = F * t
#
# 3. 比推力 (Specific Impulse, Isp) の定義
#    比推力Ispは、「消費した推進剤の『重量』あたりに得られる力積」と定義されます。
#    Isp = (Total Impulse) / (推進剤の重量)
#        = (F * t) / (推進剤の質量 * g0)
#
# 4. 式の結合と整理
#    - Fを「1.」の式で置き換えます。
#      Isp = (ṁ * Ve * t) / (推進剤の質量 * g0)
#
#    - 「推進剤の質量」は「単位時間あたりの質量(ṁ) * 燃焼時間(t)」なので、
#      推進剤の質量 = ṁ * t
#
#    - これを代入します。
#      Isp = (ṁ * Ve * t) / (ṁ * t * g0)
#
#    - 分子と分母にある (ṁ * t) が打ち消し合います。
#      Isp = Ve / g0
#
#    - したがって、これをVeについて解くと以下の関係式が得られます。
#      Ve = Isp * g0
#

def calculate_exhaust_velocity(specific_impulse, gravity):
    """
    比推力（秒）と重力加速度から、燃焼ガスの噴射速度を計算します。

    計算式: 噴射速度 (Ve) = 比推力 (Isp) * 重力加速度 (g0)

    Parameters
    ----------
    specific_impulse : float or int
        比推力 [秒]
    gravity : float or int
        重力加速度 [m/s^2]

    Returns
    -------
    exhaust_velocity : float
        燃焼ガスの噴射速度 [m/s]
    """
    exhaust_velocity = specific_impulse * gravity
    return exhaust_velocity

# --- このスクリプトを直接実行した場合の計算 ---
if __name__ == "__main__":
    # --- 問題の条件 ---
    Isp = 500  # 比推力 (秒)
    g0 = 10    # 重力加速度 (m/s^2) ※問題で指定された値

    # 噴射速度を計算
    Ve = calculate_exhaust_velocity(Isp, g0)

    print("--- 比推力から噴射速度を計算 ---")
    print(f"入力値:")
    print(f"  - 比推力 (Isp): {Isp} s")
    print(f"  - 重力加速度 (g0): {g0} m/s^2")
    print("-" * 30)
    print("計算式: Ve = Isp * g0")
    print(f"      = {Isp} * {g0}")
    print("-" * 30)
    print("計算結果:")
    print(f"  - 燃焼ガスの噴射速度 (Ve): {Ve} m/s")

    # 参考としてkm/sにも変換して表示
    Ve_km_s = Ve / 1000
    print(f"  - (参考) km/s 換算: {Ve_km_s} km/s")