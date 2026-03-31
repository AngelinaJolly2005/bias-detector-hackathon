import pandas as pd

def calculate_bank_fairness(df, target_col, protected_col):
    # Calculate approval rates (percentage of 1s in the target column)
    group_stats = df.groupby(protected_col)[target_col].mean()
    
    max_rate = group_stats.max()
    min_rate = group_stats.min()
    
    # The 80% Rule (Disparate Impact)
    impact_ratio = min_rate / max_rate if max_rate > 0 else 1.0
    is_biased = impact_ratio < 0.8
    
    return {
        "impact_ratio": impact_ratio,
        "is_biased": is_biased,
        "group_rates": group_stats,
        "gap": max_rate - min_rate
    }