from GLOBAL import *

file_name = "handle_next_iteration"

next_iter_cmds = [
    tellraw_info("This example is done", "green"),
    f"scoreboard players add current_sample_idx {OBJ_STATUS} 1",
    f"execute if score current_sample_idx {OBJ_STATUS} < NUM_SAMPLES {OBJ_CONSTS} run function {NAMESPACE}:process_next_sample",
    f"execute if score current_sample_idx {OBJ_STATUS} >= NUM_SAMPLES {OBJ_CONSTS} run function {NAMESPACE}:end_epoch"
]

create_file(file_name, next_iter_cmds)