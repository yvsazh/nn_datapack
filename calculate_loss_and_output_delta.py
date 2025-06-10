from GLOBAL import *

file_name = "calculate_loss_and_output_delta"

calc_loss_cmds = [tellraw_layer_section("Calculate Loss & Output Delta")]
output_layer_idx = LAYERS - 1
output_neuron_idx = 0

calc_loss_cmds.extend([
    tellraw_debug(f"  Prediction (a{output_layer_idx}_{output_neuron_idx}):"),
    f"tellraw @a [{{\"score\":{{\"name\":\"a{output_layer_idx}_{output_neuron_idx}\",\"objective\":\"{OBJ_ACTIVATIONS}\"}}}}] ",
    tellraw_debug(f"  Target (target_price):"),
    f"tellraw @a [{{\"score\":{{\"name\":\"target_price\",\"objective\":\"{OBJ_INPUTS}\"}}}}] ",

    # error_scaled = prediction_scaled - target_scaled
    f"scoreboard players operation error_scaled {OBJ_TEMP} = a{output_layer_idx}_{output_neuron_idx} {OBJ_ACTIVATIONS}",
    f"scoreboard players operation error_scaled {OBJ_TEMP} -= target_price {OBJ_INPUTS}",

    # Для MSE, dL/d_out = (prediction - target). Якщо лінійна активація на виході, d_out/dz_out = 1.
    # Отже, dz_output_scaled = error_scaled
    f"scoreboard players operation dz{output_layer_idx}_{output_neuron_idx} {OBJ_GRADIENTS} = error_scaled {OBJ_TEMP}",

    # Обчислення втрат (MSE = (error^2) / 2)
    # current_sample_loss_scaled = (error_scaled * error_scaled / S) / 2
    # error_scaled * error_scaled -> S*S
    f"scoreboard players operation current_sample_loss_term {OBJ_TEMP} = error_scaled {OBJ_TEMP}",
    f"scoreboard players operation current_sample_loss_term {OBJ_TEMP} *= error_scaled {OBJ_TEMP}",
    # / S -> S
    f"scoreboard players operation current_sample_loss_term {OBJ_TEMP} /= SCALER {OBJ_CONSTS}",
    # / 2 (для MSE)
    f"scoreboard players operation current_sample_loss_term {OBJ_TEMP} /= TWO {OBJ_CONSTS}",

    # Додаємо до суми втрат за епоху
    f"scoreboard players operation current_epoch_loss_sum_scaled {OBJ_STATUS} += current_sample_loss_term {OBJ_TEMP}",
    tellraw_debug(f"  Loss (current_epoch_loss_sum_scaled):"),
    f"tellraw @a [{{\"score\":{{\"name\":\"current_epoch_loss_sum_scaled\",\"objective\":\"{OBJ_STATUS}\"}}}}] ",
])

create_file(file_name, calc_loss_cmds)