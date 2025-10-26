# 恒星の光度、半径、表面温度の関係を計算するスクリプト

import astropy.units as u
from astropy.constants import sigma_sb

# --- 前提条件 ---
# 2つの恒星 A, B の光度は等しい (L_A = L_B)
# 恒星Aの表面温度 T_A = 4000 K
# 恒星Bの表面温度 T_B = 20000 K

# --- 物理法則: シュテファン＝ボルツマンの法則 ---
# 恒星の光度Lは、その半径をR、表面温度をTとすると、以下の式で表される。
# L = 4 * π * R^2 * σ * T^4
# (σはシュテファン＝ボルツマン定数)

# --- 式の変形 ---
# L_A = L_B なので、
# 4 * π * R_A^2 * σ * T_A^4 = 4 * π * R_B^2 * σ * T_B^4
#
# 両辺の共通項 (4 * π * σ) を消去すると、
# R_A^2 * T_A^4 = R_B^2 * T_B^4
#
# 半径の比 R_A / R_B を求めるために式を整理すると、
# (R_A / R_B)^2 = T_B^4 / T_A^4 = (T_B / T_A)^4
#
# 両辺の平方根をとると、
# R_A / R_B = (T_B / T_A)^2

# --- astropy を用いた計算 ---

# 恒星の表面温度を astropy.units を使って定義
T_A = 4000 * u.K
T_B = 20000 * u.K
print(f"恒星Aの表面温度 T_A: {T_A}")
print(f"恒星Bの表面温度 T_B: {T_B}")

print("\n--- 数式の導出過程 ---")
print("1. シュテファン＝ボルツマンの法則: L = 4 * π * R^2 * σ * T^4")
print("2. 光度が等しい (L_A = L_B) ため、両辺に法則を適用します。")
print("   4 * π * R_A^2 * σ * T_A^4 = 4 * π * R_B^2 * σ * T_B^4")
print("3. 両辺の共通項 (4 * π * σ) を消去します。")
print("   R_A^2 * T_A^4 = R_B^2 * T_B^4")
print("4. 半径の比 (R_A / R_B) を求めるために、式を整理します。")
print("   R_A^2 / R_B^2 = T_B^4 / T_A^4")
print("5. 式をまとめます。")
print("   (R_A / R_B)^2 = (T_B / T_A)^4")
print("6. 両辺の平方根をとり、最終的な関係式を得ます。")
print("   R_A / R_B = (T_B / T_A)^2")

print("\n--- 計算過程 ---")

# 1. 温度の比を計算
temp_ratio = T_B / T_A
print(f"1. 温度比を計算します: T_B / T_A = {T_B} / {T_A} = {temp_ratio.value:.0f}")

# 2. 半径の比を計算 (R_A / R_B) = (T_B / T_A)^2
radius_ratio = temp_ratio**2
print(f"2. 半径比を計算します: (温度比)^2 = ({temp_ratio.value:.0f})^2 = {radius_ratio.value:.0f}")

# --- 結果の表示 ---
print("\n--- 最終結果 ---")
# .value を使って単位なしの数値を取り出す
print(f"恒星Aの半径は恒星Bの {radius_ratio.value:.0f} 倍です。")
