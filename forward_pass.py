from GLOBAL import *

file_name = "forward_pass"

fp_cmds = [tellraw_layer_section("Forward Pass")]

# inputs
for j in range(ARCH[0]):
    fp_cmds.append(f"scoreboard players operation a0_{j} {OBJ_ACTIVATIONS} = inp_{j} {OBJ_INPUTS}")

for L in range(LAYERS - 1): # L - індекс шару, З ЯКОГО йдуть ваги (0, 1, ...)
    layer_idx_curr = L      # індекс поточного шару активацій (a_L_j)
    layer_idx_next = L + 1  # індекс наступного шару (z_{L+1}_i, a_{L+1}_i)
    num_neurons_in = ARCH[layer_idx_curr]
    num_neurons_out = ARCH[layer_idx_next]

    for i in range(num_neurons_out): # Нейрон 'i' в наступному шарі (layer_idx_next)
        # z[L+1][i] = sum(a[L][j] * w[L][i][j]) + b[L][i]
        # Всі значення масштабовані на LR_SCALE (S)
        # z_scaled = sum( (a_scaled * w_scaled) / S ) + b_scaled
        # Починаємо з bias: z = b
        fp_cmds.append(f"scoreboard players operation z{layer_idx_next}_{i} {OBJ_ACTIVATIONS} = b{L}_{i} {OBJ_PARAMS}")

        for j in range(num_neurons_in): # Нейрон 'j' в поточному шарі (layer_idx_curr)
            # term = a[L][j] * w[L][i][j] (обидва S -> результат S*S)
            fp_cmds.append(f"scoreboard players operation temp_mult_term {OBJ_TEMP} = a{layer_idx_curr}_{j} {OBJ_ACTIVATIONS}")
            fp_cmds.append(f"scoreboard players operation temp_mult_term {OBJ_TEMP} *= w{L}_{i}_{j} {OBJ_PARAMS}")
            # ! term_scaled = term / S (результат S) А ЧИ ТРЕБА ЦЕ?
            fp_cmds.append(f"scoreboard players operation temp_mult_term {OBJ_TEMP} /= SCALER {OBJ_CONSTS}")
            # z[L+1][i] += term_scaled
            fp_cmds.append(f"scoreboard players operation z{layer_idx_next}_{i} {OBJ_ACTIVATIONS} += temp_mult_term {OBJ_TEMP}")

        # Функція активації
        if layer_idx_next < LAYERS - 1: # Прихований шар, використовуємо ReLU
            fp_cmds.append(f"scoreboard players operation val_in {OBJ_TEMP} = z{layer_idx_next}_{i} {OBJ_ACTIVATIONS}")
            fp_cmds.append(f"function {NAMESPACE}:relu")
            fp_cmds.append(f"scoreboard players operation a{layer_idx_next}_{i} {OBJ_ACTIVATIONS} = val_out {OBJ_TEMP}")
        else: # Вихідний шар, лінійна активація
            fp_cmds.append(f"scoreboard players operation a{layer_idx_next}_{i} {OBJ_ACTIVATIONS} = z{layer_idx_next}_{i} {OBJ_ACTIVATIONS}")

create_file(file_name, fp_cmds)