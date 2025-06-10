from GLOBAL import *
import pandas as pd

try:
    df = pd.read_csv("../house_prices_dataset.csv")
except FileNotFoundError:
    print(f"ПОМИЛКА: Файл '../house_prices_dataset.csv' не знайдено. Будь ласка, переконайтеся, що він існує.")
    exit()

if df.empty:
    print(f"ПОМИЛКА: Файл даних порожній.")
    exit()

feature_stats = {}
for feature_name in INPUT_FEATURES:
    min_val = df[feature_name].min()
    max_val = df[feature_name].max()
    feature_stats[feature_name] = {"min": min_val, "max": max_val, "range": max_val - min_val}

min_target = df[TARGET_FEATURE].min()
max_target = df[TARGET_FEATURE].max()
target_range = max_target - min_target

for i, row in df.iterrows():
    file_name = f"train_sample_{i}"
    sample_cmds = [
    ]
    for idx, feature_name in enumerate(INPUT_FEATURES):
        original_val = row[feature_name]
        stats = feature_stats[feature_name]
        
        normalized_val = 0.0  
        if stats["range"] != 0:
            normalized_val = (original_val - stats["min"]) / stats["range"]
        val = int(normalized_val * SCALER)
        sample_cmds.append(f"scoreboard players set inp_{idx} {OBJ_INPUTS} {val}")

    original_target_val = row[TARGET_FEATURE]
    
    normalized_target_val = 0.0 
    if target_range != 0:
        normalized_target_val = (original_target_val - min_target) / target_range
    
    target_val = int(normalized_target_val * SCALER)
    sample_cmds.append(f"scoreboard players set target_price {OBJ_INPUTS} {target_val}")
    
    sample_cmds.extend([
        f"function {NAMESPACE}:forward_pass",
        f"function {NAMESPACE}:calculate_loss_and_output_delta",
        f"function {NAMESPACE}:backward_pass",
        f"function {NAMESPACE}:update_parameters",
        f"function {NAMESPACE}:handle_next_iteration"
    ])
    create_file(file_name, sample_cmds)
