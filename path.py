import math
import random

# 1. 完整人物模型数据
characters = [
    { "name": "李佑川", "radius_factor": 1.0, "scores": { "Trust": 1.00, "Emotion": 9.00, "Morality": 1.19, "Decision": 3.84, "Social": 1.00, "Risk": 9.00, "Info": 7.31, "Value": 9.00 } },
    { "name": "庄宇光", "radius_factor": 0.9, "scores": { "Trust": 1.84, "Emotion": 8.54, "Morality": 1.92, "Decision": 2.54, "Social": 4.29, "Risk": 9.00, "Info": 9.00, "Value": 9.00 } },
    { "name": "刘依悦", "radius_factor": 1.3, "scores": { "Trust": 9.00, "Emotion": 8.54, "Morality": 9.00, "Decision": 1.78, "Social": 6.06, "Risk": 1.22, "Info": 1.00, "Value": 3.05 } },
    { "name": "蔡锦昕", "radius_factor": 0.9, "scores": { "Trust": 2.06, "Emotion": 1.00, "Morality": 2.45, "Decision": 6.91, "Social": 3.21, "Risk": 2.87, "Info": 2.48, "Value": 5.41 } },
    { "name": "林可雯", "radius_factor": 1.0, "scores": { "Trust": 1.52, "Emotion": 3.43, "Morality": 1.00, "Decision": 8.15, "Social": 1.43, "Risk": 7.01, "Info": 4.26, "Value": 9.00 } },
    { "name": "吴蕙岑", "radius_factor": 1.0, "scores": { "Trust": 8.41, "Emotion": 5.55, "Morality": 8.51, "Decision": 1.23, "Social": 9.00, "Risk": 1.00, "Info": 1.03, "Value": 4.49 } },
    { "name": "曾耀晖", "radius_factor": 0.8, "scores": { "Trust": 3.33, "Emotion": 3.21, "Morality": 1.43, "Decision": 1.00, "Social": 6.35, "Risk": 6.65, "Info": 2.95, "Value": 1.00 } },
    { "name": "孙博文", "radius_factor": 1.2, "scores": { "Trust": 7.27, "Emotion": 4.44, "Morality": 6.48, "Decision": 2.09, "Social": 5.06, "Risk": 2.85, "Info": 1.76, "Value": 4.54 } },
    { "name": "郑方一", "radius_factor": 1.2, "scores": { "Trust": 6.98, "Emotion": 7.58, "Morality": 7.27, "Decision": 7.85, "Social": 5.26, "Risk": 2.85, "Info": 1.56, "Value": 4.93 } },
    { "name": "马柏全", "radius_factor": 1.3, "scores": { "Trust": 9.00, "Emotion": 8.32, "Morality": 8.00, "Decision": 1.14, "Social": 4.21, "Risk": 1.00, "Info": 1.00, "Value": 3.05 } },
    { "name": "文艺宏", "radius_factor": 1.3, "scores": { "Trust": 8.02, "Emotion": 8.22, "Morality": 8.26, "Decision": 2.34, "Social": 4.21, "Risk": 1.00, "Info": 1.00, "Value": 2.98 } },
    { "name": "孟羽童", "radius_factor": 1.4, "scores": { "Trust": 6.52, "Emotion": 7.83, "Morality": 5.78, "Decision": 3.96, "Social": 4.76, "Risk": 4.10, "Info": 3.14, "Value": 6.02 } },
    { "name": "林鹰谷", "radius_factor": 1.0, "scores": { "Trust": 5.98, "Emotion": 6.48, "Morality": 5.23, "Decision": 9.00, "Social": 5.69, "Risk": 5.00, "Info": 4.12, "Value": 6.59 } },
    { "name": "欧阳东", "radius_factor": 1.2, "scores": { "Trust": 8.34, "Emotion": 7.58, "Morality": 7.59, "Decision": 4.58, "Social": 6.09, "Risk": 6.35, "Info": 3.68, "Value": 5.12 } },
    { "name": "朱宸皓", "radius_factor": 1.0, "scores": { "Trust": 8.09, "Emotion": 6.79, "Morality": 7.97, "Decision": 3.23, "Social": 8.01, "Risk": 3.16, "Info": 2.01, "Value": 3.15 } },
    { "name": "叶筱玮", "radius_factor": 1.0, "scores": { "Trust": 8.53, "Emotion": 8.10, "Morality": 8.23, "Decision": 3.10, "Social": 6.21, "Risk": 5.98, "Info": 1.78, "Value": 1.00 } },
    { "name": "张慧鑫", "radius_factor": 1.0, "scores": { "Trust": 8.53, "Emotion": 5.00, "Morality": 8.00, "Decision": 3.59, "Social": 6.21, "Risk": 5.00, "Info": 1.68, "Value": 2.03 } },
    { "name": "李孝谦", "radius_factor": 1.0, "scores": { "Trust": 5.73, "Emotion": 7.63, "Morality": 7.52, "Decision": 5.62, "Social": 7.21, "Risk": 6.12, "Info": 5.00, "Value": 7.23 } }
]

# 2. 题目增量矩阵
questionScores = [
    [{"Emotion": -1.5, "Value": -1.0}, {"Emotion": 1.5, "Decision": 0.5}, {"Emotion": -1.0, "Value": -1.0, "Morality": -0.5}],
    [{"Decision": -0.5, "Risk": 1.0}, {"Risk": -1.5, "Decision": 0.5}, {"Risk": -1.0, "Decision": 0.5}],
    [{"Trust": 1.0, "Social": 1.5}, {"Trust": -1.0, "Social": -0.5}, {"Morality": -1.0, "Info": 1.0}],
    [{"Trust": 1.0, "Social": 1.0}, {"Decision": 1.0, "Social": -0.2}, {"Trust": -1.0, "Social": -0.2}],
    [{"Morality": 1.0, "Social": 1.0}, {"Morality": -1.0, "Info": 1.0}, {"Value": 1.0, "Info": 0.5}],
    [{"Risk": -1.0}, {"Risk": 1.0}, {"Value": -0.5, "Morality": -0.5}],
    [{"Emotion": -1.0, "Value": -1.0, "Morality": -1.0}, {"Emotion": 0.5, "Morality": 0.5}, {"Emotion": 1.0}],
    [{"Info": 1.0, "Morality": 0.5}, {"Risk": 0.2, "Info": 1.0}, {"Risk": 1.0, "Morality": -0.3}],
    [{"Morality": 0.5, "Social": 1.0}, {"Morality": 0.5, "Info": 0.5, "Value": 0.5}, {"Morality": -0.5}],
    [{"Social": 1.0, "Info": 0.5}, {"Social": -0.5}, {"Trust": -0.5, "Social": -1.0}],
    [{"Trust": 1.0, "Risk": -1.0}, {"Trust": -1.0, "Risk": 1.0}, {"Trust": -1.0, "Risk": -1.0}],
    [{"Decision": -1.0, "Risk": 0.5}, {"Risk": -1.0, "Decision": 1.0}, {"Morality": -1.0, "Info": 1.0}],
    [{"Morality": 1.0, "Social": 1.0}, {"Morality": -1.0, "Social": -1.0, "Value": 0.5}, {"Social": 1.0, "Info": 0.5}],
    [{"Decision": 1.0, "Emotion": 0.5, "Risk": 0.5}, {"Decision": -1.0, "Risk": -0.5}, {"Morality": -0.2, "Info": 0.7}],
    [{"Emotion": 1.0, "Trust": 0.5}, {"Trust": -1.0}, {"Emotion": -0.5}],
    [{"Info": -0.5, "Morality": -0.2, "Value": 0.5}, {"Morality": 1.0, "Info": -0.5}, {"Social": 0.5, "Info": 0.5, "Morality": -0.2, "Value": 0.2}],
    [{"Value": 1.5}, {"Value": -1.5}, {}],
    [{"Social": 2.0}, {"Social": -2.0}, {"Social": -1.0}]
]

keys = ["Trust", "Emotion", "Morality", "Decision", "Social", "Risk", "Info", "Value"]

# 3. 标准中心化余弦相似度
def getCenteredCosine(vecA, vecB):
    meanA = sum(vecA[k] for k in keys) / len(keys)
    meanB = sum(vecB[k] for k in keys) / len(keys)
    dotProduct, normA, normB = 0, 0, 0
    for k in keys:
        clrA = vecA[k] - meanA
        clrB = vecB[k] - meanB
        dotProduct += clrA * clrB
        normA += clrA * clrA
        normB += clrB * clrB
    if normA == 0 or normB == 0:
        return -1.0
    return dotProduct / (math.sqrt(normA) * math.sqrt(normB))

# 4. 双约束局部搜索优化器
def find_all_paths_with_min_sim(min_sim=0.80):
    mapping = {0: 'A', 1: 'B', 2: 'C'}
    results = {}
    
    for target_char in characters:
        target_name = target_char["name"]
        best_fitness = -float('inf')
        best_path = []
        best_raw = 0
        
        # 允许最大 15000 次重启以突破极限
        for attempt in range(15000):
            current_choices = [random.randint(0, 2) for _ in range(18)]
            improved = True
            
            while improved:
                improved = False
                for q_idx in range(18):
                    old_choice = current_choices[q_idx]
                    for next_choice in range(3):
                        if next_choice == old_choice: continue
                        current_choices[q_idx] = next_choice
                        
                        # 模拟答题得分
                        userScores = {k: 5.0 for k in keys}
                        for q, c in enumerate(current_choices):
                            for key, val in questionScores[q][c].items():
                                userScores[key] += val
                        for key in userScores:
                            userScores[key] = max(1.0, min(9.0, userScores[key]))
                        
                        # 计算全员排名
                        scores_dict = {}
                        raw_scores = {}
                        for ch in characters:
                            raw = getCenteredCosine(userScores, ch["scores"])
                            raw_scores[ch["name"]] = raw
                            scores_dict[ch["name"]] = raw * ch.get("radius_factor", 1.0)
                        
                        target_adj = scores_dict[target_name]
                        max_other_adj = max(v for k, v in scores_dict.items() if k != target_name)
                        target_raw = raw_scores[target_name]
                        
                        # 惩罚项设计：被截胡扣20分，相似度不达标扣10分
                        penalty_win = max(0, max_other_adj - target_adj)
                        penalty_sim = max(0, min_sim - target_raw)
                        fitness = target_raw - 20 * penalty_win - 10 * penalty_sim
                        
                        if fitness > best_fitness:
                            best_fitness = fitness
                            best_path = list(current_choices)
                            best_raw = target_raw
                            improved = True
                            break
                    if improved: break
                    current_choices[q_idx] = old_choice
            
            # 检查最终当前最佳路径是否完全合法
            if best_fitness > 0 and best_raw >= min_sim:
                break
                
        results[target_name] = {
            "path": [mapping[c] for c in best_path],
            "raw_sim": best_raw
        }
    return results

if __name__ == "__main__":
    print("⏳ 正在进行带有“相似度 $\ge$ 80%”硬性红线的逆向数据探寻...")
    path_report = find_all_paths_with_min_sim(0.80)
    print("\n📊 终极算法解析报告：")
    for name, data in path_report.items():
        print(f"【{name}】路径: {', '.join(data['path'])} | 原始相似度: {data['raw_sim']*100:.2f}%")