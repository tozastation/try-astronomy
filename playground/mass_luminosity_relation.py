# --- 質量光度関係についての解説 ---
#
# 主系列星の光度(Luminosity)は、その質量(Mass)と強い相関関係があり、
# おおよそ以下の式で表されます。
#
#   L ∝ M^α  (光度は質量のα乗に比例する)
#
# この関係は「質量光度関係」と呼ばれます。
# 指数αの値は、星の質量によって異なり、一般的に以下のようになります。
# - 太陽のような中質量の星: α ≈ 3.5 - 4.0
# - 太陽より重い星: α ≈ 3.0
# - 太陽より軽い星: α ≈ 2.3
#
# この問題では、α = 3.5 という一般的な値を使って計算します。
#
# 太陽の光度(L_sun)と質量(M_sun)を基準にすると、ある星の光度(L_star)と
# 質量(M_star)の関係は、以下の比の式で表せます。
#
#   (L_star / L_sun) = (M_star / M_sun) ** 3.5
#
# この式を使って、太陽の0.5倍の質量の星の光度を計算します。

def calculate_luminosity_ratio(mass_ratio, exponent=3.5):
    """
    質量光度関係を用いて、恒星の光度を太陽の光度との比で計算します。

    Parameters
    ----------
    mass_ratio : float
        計算したい星の、太陽に対する質量比 (M_star / M_sun)。
    exponent : float, optional
        質量光度関係の指数α。デフォルトは3.5。

    Returns
    -------
    luminosity_ratio : float
        計算された光度の、太陽に対する比 (L_star / L_sun)。
    """
    luminosity_ratio = mass_ratio ** exponent
    return luminosity_ratio

# --- このスクリプトを直接実行した場合の計算 ---
if __name__ == "__main__":
    # --- 問題の条件 ---
    # 太陽の質量の0.5倍の星
    mass_ratio_star = 0.5
    exponent_alpha = 3.5

    # 光度の比を計算
    lum_ratio = calculate_luminosity_ratio(mass_ratio_star, exponent_alpha)

    print("--- 質量光度関係による光度の計算 ---")
    print(f"入力値:")
    print(f"  - 星の質量: 太陽の {mass_ratio_star} 倍")
    print(f"  - 質量光度関係の指数 (α): {exponent_alpha}")
    print("-" * 30)
    print("計算式: (L_star / L_sun) = (M_star / M_sun) ** α")
    print(f"      = {mass_ratio_star} ** {exponent_alpha}")
    print("-" * 30)
    print("計算結果:")
    print(f"  => この星の光度は、太陽のおよそ {lum_ratio:.3f} 倍になります。")
