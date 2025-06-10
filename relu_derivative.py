from GLOBAL import *

file_name = "relu_derivative"

relu_cmds = [
    f"scoreboard players set val_out {OBJ_TEMP} 0",
    f"execute if score val_in {OBJ_TEMP} > ZERO {OBJ_CONSTS} run scoreboard players operation val_out {OBJ_TEMP} = SCALER {OBJ_CONSTS}",
]
create_file(file_name, relu_cmds)