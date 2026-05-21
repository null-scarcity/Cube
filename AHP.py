import numpy as np

# 1. 初始化选手名单
players = ["李佑川", "庄宇光", "刘依悦", "蔡锦昕", "林可雯", "吴蕙岑", "曾耀晖", "孙博文", "郑方一"]
n = len(players)

# 2. 建立标准的 9x9 矩阵
A = np.ones((n, n))

# 3. 填入你在图片中打好的下三角矩阵数据 (A[i, j] 表示 行i 相比 列j 的强弱)
# 庄宇光 (Row 2)
A[1, 0] = 2

# 刘依悦 (Row 3)
A[2, 0] = 5
A[2, 1] = 4

# 蔡锦昕 (Row 4)
A[3, 0] = 2
A[3, 1] = 1
A[3, 2] = 0.25

# 林可雯 (Row 5)
A[4, 0] = 2
A[4, 1] = 1
A[4, 2] = 0.25
A[4, 3] = 0.5

# 吴蕙岑 (Row 6)
A[5, 0] = 5
A[5, 1] = 4
A[5, 2] = 1
A[5, 3] = 4
A[5, 4] = 5

# 曾耀晖 (Row 7)
A[6, 0] = 3
A[6, 1] = 2
A[6, 2] = 0.33
A[6, 3] = 2
A[6, 4] = 3
A[6, 5] = 0.33

# 孙博文 (Row 8)
A[7, 0] = 4
A[7, 1] = 3
A[7, 2] = 1
A[7, 3] = 3
A[7, 4] = 3
A[7, 5] = 1
A[7, 6] = 3

# 郑方一 (Row 9)
A[8, 0] = 4
A[8, 1] = 3
A[8, 2] = 0.5
A[8, 3] = 3
A[8, 4] = 4
A[8, 5] = 1
A[8, 6] = 3
A[8, 7] = 1

# 4. 根据倒数对称性，自动补全上三角矩阵
for i in range(n):
    for j in range(n):
        if i > j:
            A[j, i] = 1.0 / A[i, j]

# 5. AHP 核心特征值算法求解
eig_vals, eig_vecs = np.linalg.eig(A)
max_idx = np.argmax(np.real(eig_vals))
max_eig_val = np.real(eig_vals[max_idx])
weights = np.real(eig_vecs[:, max_idx])
weights = weights / np.sum(weights)  # 归一化得到原始权重

# 6. 一致性检验 (CR 计算)
RI_dict = {1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
CI = (max_eig_val - n) / (n - 1)
RI = RI_dict[n]
CR = CI / RI

print("=" * 50)
print(f"📊 矩阵一致性检验结果：")
print(f"最大特征值 (λ_max): {max_eig_val:.4f}")
print(f"一致性比率 (CR): {CR:.4f}  " + ("(通过检验, 逻辑非常严密! ✅)" if CR < 0.1 else "(不通过 ❌)"))
print("=" * 50)

# 7. 将原始相对权重线性映射到 1 ~ 9 分标尺
min_w = np.min(weights)
max_w = np.max(weights)
scores_1_to_9 = 1 + 8 * (weights - min_w) / (max_w - min_w)

# 8. 排序并输出结果
results = list(zip(players, weights, scores_1_to_9))
results.sort(key=lambda x: x[2], reverse=True)  # 按得分从高到低排序

print("\n🏆 【信任倾向(T)】玩家最终测试标尺得分（从轻信到多疑）：")
for name, w, score in results:
    print(f"🔹 {name:<4} : AHP权重 = {w:.4f} --> 网页标准得分 = {score:.2f}")
print("=" * 50)