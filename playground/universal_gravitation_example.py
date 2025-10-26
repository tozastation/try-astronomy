from astropy import constants as const
from astropy import units as u

def calculate_gravitational_force(mass1, mass2, distance):
    """
    ニュートンの万有引力の法則に基づき、2つの物体間に働く引力の大きさを計算します。

    計算式: F = G * (m1 * m2) / r^2
    G: 万有引力定数
    m1, m2: 2つの物体の質量
    r: 物体間の距離

    Parameters
    ----------
    mass1 : astropy.units.Quantity
        物体1の質量。
    mass2 : astropy.units.Quantity
        物体2の質量。
    distance : astropy.units.Quantity
        2つの物体間の距離。

    Returns
    -------
    force : astropy.units.Quantity
        計算された万有引力の大きさ（ニュートン単位）。
    """
    # astropyの定数と単位を使って計算
    force = (const.G * mass1 * mass2) / (distance ** 2)
    
    # 結果をニュートン(N)単位に変換して返す
    return force.to(u.N)

# --- このスクリプトを直接実行した場合の例題 ---
if __name__ == "__main__":
    print("--- 万有引力の法則の計算例題 ---")

    # --- 例題: 地球と月の間に働く引力 ---
    
    # 入力値
    m1 = const.M_earth  # 地球の質量
    # astropy.constantsに月の質量M_moonは直接定義されていないため、手動で値を設定
    m2 = 7.342e22 * u.kg # 月の質量
    r = 384400 * u.km   # 地球と月の平均距離

    # 計算実行
    F = calculate_gravitational_force(m1, m2, r)

    print("\n[例題: 地球と月の間に働く万有引力]")
    print("入力値:")
    print(f"  - 物体1の質量 (地球): {m1:.2e}")
    print(f"  - 物体2の質量 (月): {m2:.2e}")
    print(f"  - 物体間の距離: {r.to(u.km):,.0f}")
    print("-" * 30)
    print("計算式: F = G * (m1 * m2) / r^2")
    print("-" * 30)
    print("計算結果:")
    print(f"  - 万有引力の大きさ (F): {F:.3e}")
    print("\n(約 2.0 x 10^20 ニュートン。これは、ジャンボジェット機約20兆機分の重さに相当します)")
