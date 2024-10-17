# src/csv_integration.py
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List
from matplotlib.colors import Normalize
from config import CSV_DIR
import numpy as np  # Import NumPy library



def generate_heatmap(dataframes: List[pd.DataFrame], csv_dir: str):
    if not dataframes:
        return
    
    combined_df = pd.concat(dataframes, axis=1)
    combined_df.fillna(0, inplace=True)  # 欠損値を0で埋める
    correlation_matrix = combined_df.corr()  # 相関行列を計算

    # 相関行列をヒートマップとして可視化
    plt.figure(figsize=(12, 10))
    ax = sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0,
                     annot_kws={'size': 6})  # 注釈のフォントサイズ設定
    plt.title('Correlation Matrix of Monthly Returns')

    # ticksを明示的に設定
    x_ticks = np.arange(len(combined_df.columns)) + 0.5
    y_ticks = np.arange(len(combined_df.columns)) + 0.5
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)

    ax.set_xticklabels(combined_df.columns, fontsize=7, rotation=45, ha='right')
    ax.set_yticklabels(combined_df.columns, fontsize=7)

    plt.tight_layout()
    plt.savefig(os.path.join(csv_dir, 'correlation_heatmap.png'))
    plt.close()

    combined_df.to_csv(os.path.join(csv_dir, 'combined_returns.csv'))
