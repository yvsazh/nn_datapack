from GLOBAL import *

file_name = "process_next_sample"

process_next_sample_cmds = [
    tellraw_info(f"Example #"),
    f"tellraw @a [{{\"score\":{{\"name\":\"current_sample_idx\",\"objective\":\"{OBJ_STATUS}\"}}}}, {{\"text\":\" / \"}}, {{\"score\":{{\"name\":\"NUM_SAMPLES\",\"objective\":\"{OBJ_CONSTS}\"}}}}] ",
]
for i in range(NUM_SAMPLES):
    process_next_sample_cmds.append(f'execute if score current_sample_idx {OBJ_STATUS} matches {i} run function {NAMESPACE}:train_sample_{i}')

create_file(file_name, process_next_sample_cmds)