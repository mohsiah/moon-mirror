import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
data = {
    "site":       ["Moon", "Iceland", "Haughton Crater", "Dry Valleys", "Death Valley", "Atacama"],
    "temp_K":     [38,     233.45,    223.15,            207.45,        263.71,         263.15],
    "rain_mm":    [0,      450,       164.1,             100,           49.3,           15],
    "surface":    [1,      0.67,      0.33,              0.33,          0.33,           0],
    "abs_lat":    [87,     65.03,     75,                77.47,         36.5,           24.5],
    "ground_ice": [1,      0.5,       1,                 1,             0,              0.5],
}
df = pd.DataFrame(data).set_index("site")
traits = ["temp_K", "rain_mm", "surface", "abs_lat", "ground_ice"]

moon = df.loc["Moon"]
earth = df.drop("Moon")
#similarity
r = df[traits].max() - df[traits].min()       
similarity = 1 - (earth[traits] - moon[traits]).abs() / r

def rank_sites(weights):
    total = (similarity * pd.Series(weights)).sum(axis=1)
    return total.sort_values(ascending=False)

equal = {t: 1 / len(traits) for t in traits}
result = rank_sites(equal)

print("SIMILARITY PER TRAIT (1 = matches the Moon)")
print(similarity.round(2))
print("\nFINAL RANKING (equal weights)")
print(result.round(3))

print("\nWINNER WHEN ONE TRAIT COUNTS DOUBLE")
print(f"All equal: {result.index[0]} ({result.iloc[0]:.2f})")
for t in traits:
    w = {x: 1.0 for x in traits}
    w[t] = 2.0
    total_w = sum(w.values())
    w = {x: v / total_w for x, v in w.items()}   
    ranked = rank_sites(w)
    print(f"{t} x2: {ranked.index[0]} ({ranked.iloc[0]:.2f})")

fig, ax = plt.subplots(figsize=(8, 4))
result.sort_values().plot(kind="barh", ax=ax, color="#3b6ea5")
ax.set_xlabel("Similarity to Moon south pole (0 to 1)")
ax.set_title("Which Earth site is most Moon-like?")
plt.tight_layout()
plt.savefig("ranking.png", dpi=200)

result.rename("score").to_csv("ranking.csv")
similarity.to_csv("similarity_per_trait.csv")
print("\nSaved: ranking.png, ranking.csv, similarity_per_trait.csv")