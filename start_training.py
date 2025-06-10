from GLOBAL import *

file_name = "start_training"

start_training_cmds = [
    tellraw_info("================ LEARNING STARTED ================", "yellow"),
    f"scoreboard players add current_epoch {OBJ_STATUS} 1",
    f"scoreboard players set current_sample_idx {OBJ_STATUS} 0",
    f"scoreboard players set current_epoch_loss_sum {OBJ_STATUS} 0",
    tellraw_info(f"Epoch #"),
    f"tellraw @a [{{\"score\":{{\"name\":\"current_epoch\",\"objective\":\"{OBJ_STATUS}\"}}}}, {{\"text\":\" / \"}}, {{\"score\":{{\"name\":\"total_epochs\",\"objective\":\"{OBJ_STATUS}\"}}}}] ",
    f"function {NAMESPACE}:process_next_sample"
]

create_file(file_name, start_training_cmds)