from GLOBAL import *

file_name = "relu"

relu_cmds = [
    f"scoreboard players operation val_out {OBJ_TEMP} = val_in {OBJ_TEMP}",
    f"execute if score val_out {OBJ_TEMP} < ZERO {OBJ_CONSTS} run scoreboard players set val_out {OBJ_TEMP} 0",
]
create_file(file_name, relu_cmds)