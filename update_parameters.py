from GLOBAL import *

file_name = "update_parameters"

up_cmds = [tellraw_layer_section("Update Parameters")]
for L in range(LAYERS - 1): # L - індекс шару, З ЯКОГО йдуть ваги (0, 1, ...)
    layer_idx_prev_activs = L       # Шар попередніх активацій a[L]
    layer_idx_curr_deltas = L + 1   # Шар поточних дельт dz[L+1]
    num_neurons_in = ARCH[layer_idx_prev_activs]
    num_neurons_out = ARCH[layer_idx_curr_deltas]

    for i in range(num_neurons_out): # Нейрон 'i' в шарі dz[L+1]
        # Оновлення зміщення b[L][i]
        # db[L][i]_scaled = dz[L+1][i]_scaled (масштаб S)
        # delta_b_scaled_change = (LEARNING_RATE_NUM * db_scaled) / S
        # b_new_scaled = b_old_scaled - delta_b_scaled_change
        up_cmds.append(f"scoreboard players operation grad_b_scaled {OBJ_TEMP} = dz{layer_idx_curr_deltas}_{i} {OBJ_GRADIENTS}") # Це db_scaled

        up_cmds.append(f"scoreboard players operation change_b_scaled {OBJ_TEMP} = LEARNING_RATE {OBJ_CONSTS}")
        up_cmds.append(f"scoreboard players operation change_b_scaled {OBJ_TEMP} *= grad_b_scaled {OBJ_TEMP}") # LR_NUM * db_scaled (int * S)
        # up_cmds.append(f"scoreboard players operation change_b_scaled {OBJ_TEMP} /= SCALER {OBJ_CONSTS}") # (LR_NUM * db_scaled) / S

        up_cmds.append(f"scoreboard players operation b{L}_{i} {OBJ_PARAMS} -= change_b_scaled {OBJ_TEMP}")

        # Оновлення ваг w[L][i][j]
        for j in range(num_neurons_in): # Нейрон 'j' в шарі a[L]
            # dw[L][i][j]_scaled = (dz[L+1][i]_scaled * a[L][j]_scaled) / S (масштаб S)
            up_cmds.append(f"scoreboard players operation grad_w_scaled {OBJ_TEMP} = dz{layer_idx_curr_deltas}_{i} {OBJ_GRADIENTS}")
            up_cmds.append(f"scoreboard players operation grad_w_scaled {OBJ_TEMP} *= a{layer_idx_prev_activs}_{j} {OBJ_ACTIVATIONS}") # (S*S)
            up_cmds.append(f"scoreboard players operation grad_w_scaled {OBJ_TEMP} /= SCALER {OBJ_CONSTS}") # (S)

            # delta_w_scaled_change = (LEARNING_RATE_NUM * dw_scaled) / S
            up_cmds.append(f"scoreboard players operation change_w_scaled {OBJ_TEMP} = LEARNING_RATE {OBJ_CONSTS}")
            up_cmds.append(f"scoreboard players operation change_w_scaled {OBJ_TEMP} *= grad_w_scaled {OBJ_TEMP}") # (int * S)
            # up_cmds.append(f"scoreboard players operation change_w_scaled {OBJ_TEMP} /= SCALER {OBJ_CONSTS}") # (int * S) / S
            up_cmds.append(f"scoreboard players operation w{L}_{i}_{j} {OBJ_PARAMS} -= change_w_scaled {OBJ_TEMP}")

create_file(file_name, up_cmds)