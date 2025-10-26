# なぜ、連星間距離と公転周期で質量を導出できるのか？
#
# 一言でいうと、「重いものほど、お互いを強く引きつけ、その引力に逆らって
# 飛び去らないようにするためには、より速く回る必要があるから」です。
#
# 安定して回る連星では、2つの力が釣り合っています。
# 1. 万有引力（内側へ引く力）:
#    - 星の質量が大きいほど強くなります。
# 2. 遠心力（外側へ向かう力）:
#    - 速く回るほど（公転周期が短いほど）強くなります。
#
# この釣り合いを考えると、以下の関係が見えてきます。
#
# - もし合計質量が大きければ...
#   引力が強くなるため、釣り合うためには速く回る（周期が短くなる）必要がある。
#
# - もし距離が遠ければ...
#   引力が弱くなるため、釣り合うためにはゆっくり回る（周期が長くなる）必要がある。
#
# このように、「合計質量」「距離」「周期」は万有引力の法則で固く結びついており、
# 2つが分かれば残りの1つを計算できるのです。

import astropy.units as u

def calculate_total_mass(a, P):
    """
    ケプラーの第3法則（ハーモニック則）を用いて、連星系の合計質量を計算します。
    
    この法則は、P(年), a(au)の単位で使うと、質量が太陽質量単位で求まるというものです。
    m1 + m2 = a^3 / P^2

    Parameters
    ----------
    a : astropy.units.Quantity
        連星間距離（軌道長半径）[au]
    P : astropy.units.Quantity
        公転周期 [年]

    Returns
    -------
    total_mass : astropy.units.Quantity
        合計質量 [太陽質量]
    """
    # 値の単位をそれぞれ au, year に変換してから計算
    # .value をつけて単位なしの数値として計算を行う
    a_au = a.to(u.au).value
    P_year = P.to(u.year).value
    
    # ハーモニック則: m1 + m2 = a^3 / P^2
    total_mass_value = (a_au ** 3) / (P_year ** 2)
    
    # 結果を太陽質量の単位(solMass)として返す
    return total_mass_value * u.solMass

# --- このスクリプトを直接実行した場合のサンプル計算 ---
if __name__ == "__main__":
    # 例：連星間距離が10au、公転周期が20年の場合
    example_a = 10 * u.au
    example_P = 20 * u.year

    # 合計質量を計算
    total_mass_result = calculate_total_mass(example_a, example_P)

    print("--- ケプラーの第3法則による連星系の質量計算 ---")
    print(f"入力値:")
    print(f"  - 連星間距離 (a): {example_a}")
    print(f"  - 公転周期 (P): {example_P}")
    print("-" * 30)
    print(f"計算式: m1 + m2 = a^3 / P^2")
    print(f"         = {example_a.value}^3 / {example_P.value}^2")
    print(f"         = {example_a.value**3} / {example_P.value**2}")
    print("-" * 30)
    print(f"計算結果:")
    print(f"  - 合計質量 (m1 + m2): {total_mass_result:.2f}")

    # 参考：Astropyの機能でkgに変換して表示
    total_mass_kg = total_mass_result.to(u.kg)
    print(f"  - 合計質量 (kg換算): {total_mass_kg:.2e}")