# astropyから必要な定数と単位をインポート
from astropy import constants as const
from astropy import units as u

def calculate_schwarzschild_radius(mass):
    """
    与えられた質量からシュバルツシルト半径を計算します。

    シュバルツシルト半径 Rs は、Rs = 2GM / c^2 で計算されます。
    G: 万有引力定数, M: 質量, c: 光速

    Parameters
    ----------
    mass : astropy.units.Quantity
        対象となる天体の質量。

    Returns
    -------
    radius : astropy.units.Quantity
        計算されたシュバルツシルト半径（メートル単位）。
    """
    # astropy.constantsを使って計算。単位は自動的に処理される。
    radius = (2 * const.G * mass) / (const.c ** 2)
    
    # 結果をメートル単位に変換して返す
    return radius.to(u.m)

# --- このスクリプトを直接実行した場合の例題 ---
if __name__ == "__main__":
    print("--- シュバルツシルト半径の計算例題 ---")

    # --- 例題1: 太陽がブラックホールになった場合の半径 ---
    mass_sun = const.M_sun
    radius_sun_actual = const.R_sun  # 実際の太陽の半径
    
    # 計算実行
    radius_sun_schwarzschild = calculate_schwarzschild_radius(mass_sun)
    
    # 圧縮率を計算
    compression_ratio_sun = radius_sun_actual / radius_sun_schwarzschild

    print("\n[例題1: 太陽のシュバルツシルト半径]")
    print(f"  - 質量: 太陽質量 ({mass_sun.value:.2e} kg)")
    print(f"  - 実際の半径: {radius_sun_actual.to(u.km):,.0f}")
    print(f"  - 計算されたシュバルツシルト半径: {radius_sun_schwarzschild.to(u.km):.2f}")
    print(f"  => 圧縮率: 実際の半径を 約{compression_ratio_sun.value:,.0f} 分の1にする必要あり")

    # --- 例題2: 地球がブラックホールになった場合の半径 ---
    mass_earth = const.M_earth
    radius_earth_actual = const.R_earth # 実際の地球の半径

    # 計算実行
    radius_earth_schwarzschild = calculate_schwarzschild_radius(mass_earth)

    # 圧縮率を計算
    compression_ratio_earth = radius_earth_actual / radius_earth_schwarzschild

    print("\n[例題2: 地球のシュバルツシルト半径]")
    print(f"  - 質量: 地球質量 ({mass_earth.value:.2e} kg)")
    print(f"  - 実際の半径: {radius_earth_actual.to(u.km):,.0f}")
    print(f"  - 計算されたシュバルツシルト半径: {radius_earth_schwarzschild.to(u.mm):.2f}") # 小さすぎるのでmm単位で表示
    print(f"  => 圧縮率: 実際の半径を 約{compression_ratio_earth.value:,.0f} 分の1にする必要あり")

    # --- 例題3: 天の川銀河中心の超大質量ブラックホール(いて座A*) ---
    # これは既にブラックホールなので、「圧縮」の概念は適用されない
    mass_sgra = 4.31e6 * u.solMass
    
    # 計算実行
    radius_sgra = calculate_schwarzschild_radius(mass_sgra)
    
    print("\n[例題3: いて座A* のシュバルツシルト半径]")
    print(f"  - 質量: 太陽の約431万倍 ({mass_sgra.to(u.kg).value:.2e} kg)")
    print(f"  - 計算されたシュバルツシルト半径: {radius_sgra.to(u.km):,.0f}")
    print(f"  - (参考) au換算: {radius_sgra.to(u.au):.4f} (天文単位)")
    print("  => これは既にブラックホールのため、計算された半径が実際のサイズ（事象の地平面の半径）です。")