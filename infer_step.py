from GLOBAL import *

file_name = "infer_step"

run_infer_step_cmds = [
    tellraw_info("Start thinking...", "aqua"),
    f"function {NAMESPACE}:forward_pass",
    "",
    # tellraw_info("Prediction (scaled):", "green"),
    # # Припускаємо один вихідний нейрон a{NUM_LAYERS-1}_0
    # f"tellraw @a [{{\"text\":\"Predicted_Price_Scaled = \"}}, {{\"score\":{{\"name\":\"a{NUM_LAYERS-1}_0\",\"objective\":\"{OBJ_ACTIVATIONS}\"}}}}, {{\"text\":\" (Розділіть на {LR_SCALE}, щоб отримати приблизну реальну ціну)\"}}]",
    # # Додатково, спробуємо де-масштабувати
    f"scoreboard players operation predicted_price_approx {OBJ_TEMP} = a{LAYERS-1}_0 {OBJ_ACTIVATIONS}",
    f"scoreboard players operation predicted_price_approx {OBJ_TEMP} /= SCALER {OBJ_CONSTS}",
    tellraw_param("Approximate prediction", "predicted_price_approx", OBJ_TEMP, suffix=f"k $")
]

create_file(file_name, run_infer_step_cmds)