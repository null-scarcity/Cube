import os
import numpy as np
import pandas as pd


def cosine_similarity(v1, v2):
    """计算两个中心化向量的余弦相似度 (值在 -1 到 1 之间，越接近 1 越契合)"""
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    if norm_v1 == 0 or norm_v2 == 0:
        return -1.0  # 避免分母为0
    return dot_product / (norm_v1 * norm_v2)


def calculate_relationships_v2(file_path, output_path=None):
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    df.columns = [col.strip() for col in df.columns]
    player_col = df.columns[0]
    dimensions = [
        "Trust",
        "Emotion",
        "Morality",
        "Decision",
        "Social",
        "Risk",
        "Info",
        "Value",
    ]

    print("正在使用[中心化向量夹角算法]进行降噪，精准提纯宿命关系...")

    results = []

    for idx, row in df.iterrows():
        current_player = row[player_col]
        v_orig = row[dimensions].values.astype(float)

        # 1. 核心去噪：进行【中心化】处理，减去5分基准线，将区间映射到 -4 到 +4
        # 这一步让中庸的5分变成0（噪音），让极端的1和9变成 -4 和 +4（强烈特质）
        v_centered = v_orig - 5.0

        # 2. 构建“最契合”的理论目标向量 (在中心化空间下计算)
        # T(0), E(1), M(2), R(5), V(7) 保持特质相同
        # D(3), S(4), I(6) 乘以 -1 达到完全相反的手段效果
        v_comp_theoretical = np.copy(v_centered)
        v_comp_theoretical[3] *= -1.0
        v_comp_theoretical[4] *= -1.0
        v_comp_theoretical[6] *= -1.0

        closest_player = None
        closest_dist = float("inf")  # 相似度用欧氏距离算（看谁最像）

        compatible_player = None
        compatible_max_sim = -2.0  # 契合度改用余弦相似度（看谁最对盘，初始值设为极小）

        # 遍历其他所有人
        for idx2, row2 in df.iterrows():
            other_player = row2[player_col]
            if other_player == current_player:
                continue

            v_other = row2[dimensions].values.astype(float)
            v_other_centered = v_other - 5.0

            # 【相似度】：依然使用经典的欧氏距离（看绝对数值的远近）
            d_self = np.linalg.norm(v_orig - v_other)
            if d_self < closest_dist:
                closest_dist = d_self
                closest_player = other_player

            # 【契合度】：升级为中心化余弦相似度，彻底解决均值霸榜问题
            sim_comp = cosine_similarity(v_comp_theoretical, v_other_centered)
            if sim_comp > compatible_max_sim:
                compatible_max_sim = sim_comp
                compatible_player = other_player

        # 归一化得分展示：为了让前端好展示，把余弦值(-1到1)转化为100分制
        # 距离分依然保留原始欧氏距离分
        comp_score_100 = round((compatible_max_sim + 1) * 50, 1)

        results.append(
            {
                player_col: current_player,
                "离得最近_姓名": closest_player,
                "离得最近_距离分": round(closest_dist, 2),
                "最契合_姓名": compatible_player,
                "最契合_指数分": comp_score_100,
            }
        )

    res_df = pd.DataFrame(results)
    final_df = pd.merge(df, res_df, on=player_col, how="left")

    if not output_path:
        base, ext = os.path.splitext(file_path)
        output_path = f"{base}_processed{ext}"

    if output_path.endswith(".csv"):
        final_df.to_csv(output_path, index=False, encoding="utf-8-sig")
    else:
        final_df.to_excel(output_path, index=False)

    print(f"🎉 算法升级成功！新关系库已导出至: {output_path}")
    return final_df


if __name__ == "__main__":
    input_file = "维度得分.xlsx"
    processed_df = calculate_relationships_v2(input_file)

    print("\n💡 升级算法后的精纯数据预览：")
    preview_cols = [
        "Player",
        "离得最近_姓名",
        "离得最近_距离分",
        "最契合_姓名",
        "最契合_指数分",
    ]
    print(processed_df[preview_cols].to_string(index=False))