from GLOBAL import *

file_name = "end_epoch"

end_epoch_cmds = [
    tellraw_info(f"=============== EPOCH FINISHED ===============", "yellow"),
    f"tellraw @a [{{\"text\":\"Epoch #\"}},{{\"score\":{{\"name\":\"current_epoch\",\"objective\":\"{OBJ_STATUS}\"}}}}, {{\"text\":\" завершена.\"}}]",
    tellraw_param("Loss sum (scaled)", "current_epoch_loss_sum_scaled", OBJ_STATUS),
    # Обчислення середньої втрати за епоху (MSE_scaled = SumLoss_scaled / NumSamples)
    f"scoreboard players operation avg_epoch_loss_scaled {OBJ_STATUS} = current_epoch_loss_sum_scaled {OBJ_STATUS}",
    f"scoreboard players operation avg_epoch_loss_scaled {OBJ_STATUS} /= NUM_SAMPLES {OBJ_CONSTS}",
    tellraw_param("Average loss (scaled, ~MSE * S)", "avg_epoch_loss_scaled", OBJ_STATUS),
    # Намагаємося отримати щось схоже на реальний MSE (MSE_approx = MSE_scaled / S)
    f"scoreboard players operation mse_approx {OBJ_TEMP} = avg_epoch_loss_scaled {OBJ_STATUS}",
    f"scoreboard players operation mse_approx {OBJ_TEMP} /= SCALER {OBJ_CONSTS}",
    tellraw_param("Approximate loss", "mse_approx", OBJ_TEMP),
    # Перевірка, чи потрібно продовжувати навчання
    f"execute if score current_epoch {OBJ_STATUS} < total_epochs {OBJ_STATUS} run function {NAMESPACE}:start_training", # Запускає наступну епоху
    f"execute if score current_epoch {OBJ_STATUS} >= total_epochs {OBJ_STATUS} run tellraw @a {{\"text\":\"Learning finished!\",\"color\":\"green\",\"bold\":true}}"
]

create_file(file_name, end_epoch_cmds)