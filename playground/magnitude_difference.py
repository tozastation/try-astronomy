# astropyライブラリをインポートします。
# astropy.unitsは物理単位（メートル、秒、パーセクなど）を扱うためのモジュールで、「u」という別名で使うのが一般的です。
import astropy.units as u
# astropy.coordinates.Distanceは天体までの距離を表現し、関連する計算を行うためのクラスです。
from astropy.coordinates import Distance

# --- 問題の条件 ---
# 恒星Aと恒星Bの共通の見かけの等級（apparent magnitude）。
# 見かけの等級は、地球から観測したときの天体の明るさを示します。
# u.magとすることで、この値が等級であることをコード上で明示します。
m_app = 3.0 * u.mag

# 恒星Aまでの距離（distance）。100パーセク。
# パーセク（pc）は天文学で使われる距離の単位です。
# u.pcとすることで、この値がパーセク単位であることをコード上で明示します。
d_A = 100.0 * u.pc

# 恒星Bまでの距離。10パーセク。
d_B = 10.0 * u.pc

# --- 計算 ---
# 絶対等級（Absolute Magnitude, M）は、天体を特定の基準距離（10パーセク）から見たと仮定したときの明るさです。
# これにより、天体固有の「真の明るさ」を比較できます。
#
# 絶対等級Mは、見かけの等級mと距離d（パーセク単位）から以下の式で計算されます。
# M = m - 5 * log10(d / 10pc)
# この `5 * log10(d / 10pc)` の部分は「距離指数（distance modulus）」と呼ばれます。

# astropyのDistanceオブジェクトを作成します。これにより単位を意識した計算が容易になります。
dist_A = Distance(d_A)
dist_B = Distance(d_B)

# astropyのDistanceオブジェクトには、距離指数を計算する`.distmod`という便利なプロパティがあります。
# M = m - (距離指数) を使って、各恒星の絶対等級を計算します。
M_A = m_app - dist_A.distmod
M_B = m_app - dist_B.distmod

# 2つの恒星の絶対等級の差を計算します。
diff_M = M_B - M_A

# --- 結果の表示 ---
print("--- 恒星A ---")
print(f"  - 見かけの等級 (m): {m_app}")
print(f"  - 距離 (d): {d_A}")
print(f"  - 距離指数 (distmod): {dist_A.distmod:.2f}")
print(f"  - 計算過程: M = m - distmod = {m_app.value:.2f} - {dist_A.distmod.value:.2f}")
print(f"  - 絶対等級 (M_A): {M_A:.2f}")
print("-" * 30)
print("--- 恒星B ---")
print(f"  - 見かけの等級 (m): {m_app}")
print(f"  - 距離 (d): {d_B}")
print(f"  - 距離指数 (distmod): {dist_B.distmod:.2f}")
print(f"  - 計算過程: M = m - distmod = {m_app.value:.2f} - {dist_B.distmod.value:.2f}")
print(f"  - 絶対等級 (M_B): {M_B:.2f}")
print("-" * 30)
print("--- 等級差の計算 ---")
print(f"  - 計算過程: M_B - M_A = {M_B.value:.2f} - ({M_A.value:.2f})")
print(f"  - 2つの恒星の絶対等級の差: {diff_M:.2f}")

# --- 補足 ---
# 絶対等級の定義は「天体を10パーセクの距離から見たときの見かけの等級」です。
# 恒星Bはちょうど10パーセクの距離にあるため、その絶対等級は見かけの等級と一致するはずです。
# このスクリプトでもそのようになっているかを確認します。
print(f"\n(補足) 恒星Bは距離10pcのため、定義上、絶対等級は見かけの等級と一致します: {M_B == m_app}")
