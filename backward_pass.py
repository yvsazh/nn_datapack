from GLOBAL import *

file_name = "backward_pass"

bp_cmds = [tellraw_layer_section("Backward Pass")]
# Проходимо від передостаннього прихованого шару до першого прихованого
# L - індекс шару, для якого обчислюємо dz[L]
# dz для вихідного шару вже обчислено
for L in range(LAYERS - 2, 0, -1): # L = (N-2) ... 1.  (N-1 is output, 0 is input)
    layer_idx_curr = L      # Шар, для якого обчислюємо dz (напр. L2, L1)
    layer_idx_next = L + 1  # Шар, з якого беремо dz (напр. L3, L2)
    num_neurons_curr = ARCH[layer_idx_curr]
    num_neurons_next = ARCH[layer_idx_next]

    for k in range(num_neurons_curr): # Нейрон 'k' в поточному шарі (layer_idx_curr)
        # dz[L][k] = sum(dz[L+1][m] * w[L][m][k]) * relu_derivative(z[L][k])
        # w[L][m][k] - вага від k (шар L) до m (шар L+1)
        # Всі dz, w масштабовані на S.
        # sum_term_scaled = sum( (dz_next_scaled * w_scaled) / S )
        bp_cmds.append(f"scoreboard players set sum_weighted_deltas {OBJ_TEMP} 0") # Обнуляємо суму

        for m in range(num_neurons_next): # Нейрон 'm' в наступному шарі (layer_idx_next)
            # term = dz[L+1][m] * w[L][m][k] (S*S)
            bp_cmds.append(f"scoreboard players operation temp_bp_term {OBJ_TEMP} = dz{layer_idx_next}_{m} {OBJ_GRADIENTS}")
            bp_cmds.append(f"scoreboard players operation temp_bp_term {OBJ_TEMP} *= w{L}_{m}_{k} {OBJ_PARAMS}") # w{L}_{m}_{k} - вага від k(L) до m(L+1)
            # term_scaled = term / S (S)
            bp_cmds.append(f"scoreboard players operation temp_bp_term {OBJ_TEMP} /= SCALER {OBJ_CONSTS}")
            # sum_weighted_deltas += term_scaled
            bp_cmds.append(f"scoreboard players operation sum_weighted_deltas {OBJ_TEMP} += temp_bp_term {OBJ_TEMP}")
            # bp_cmds.append(tellraw_param(f"      After dz{layer_idx_next}_{m}*w{L}_{m}_{k}/S, sum_weighted_deltas", "sum_weighted_deltas", OBJ_TEMP))

        # relu_derivative_val = relu_derivative(z[L][k]) (результат 0 або S)
        bp_cmds.append(f"scoreboard players operation val_in {OBJ_TEMP} = z{layer_idx_curr}_{k} {OBJ_ACTIVATIONS}")
        bp_cmds.append(f"function {NAMESPACE}:relu_derivative") # val_out OBJ_TEMP містить 0 або S
        bp_cmds.append(f"scoreboard players operation relu_deriv_val {OBJ_TEMP} = val_out {OBJ_TEMP}")

        # dz[L][k] = sum_weighted_deltas * relu_deriv_val (S * S -> S*S)
        bp_cmds.append(f"scoreboard players operation dz_curr_final {OBJ_TEMP} = sum_weighted_deltas {OBJ_TEMP}")
        bp_cmds.append(f"scoreboard players operation dz_curr_final {OBJ_TEMP} *= relu_deriv_val {OBJ_TEMP}")
        # dz[L][k]_scaled = dz[L][k] / S (S)
        bp_cmds.append(f"scoreboard players operation dz_curr_final {OBJ_TEMP} /= SCALER {OBJ_CONSTS}")
        bp_cmds.append(f"scoreboard players operation dz{layer_idx_curr}_{k} {OBJ_GRADIENTS} = dz_curr_final {OBJ_TEMP}")
    
create_file(file_name, bp_cmds)