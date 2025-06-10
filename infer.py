from GLOBAL import *

file_name = "infer"

infer_cmds = [
    tellraw_info("--- Price prediction ---", "gold"),
    tellraw_info("Please set the input values in the scoreboard (multiply them by 100):"),
    tellraw_info(f"  inp_0 ({INPUT_FEATURES[0]}) [{OBJ_INPUTS}]"),
    tellraw_info(f"  inp_1 ({INPUT_FEATURES[1]}) [{OBJ_INPUTS}]"),
    tellraw_info(f"  inp_2 ({INPUT_FEATURES[2]}) [{OBJ_INPUTS}]"),
    tellraw_info(f"  inp_3 ({INPUT_FEATURES[3]}) [{OBJ_INPUTS}]"),
    tellraw_info("Example: /scoreboard players set inp_0 price_nn_inputs 300 (for 3 rooms, assuming scale = 100)"),
    tellraw_info("After setting the input values, call: /function price_nn:run_inference_step again to perform the prediction."),
]

create_file(file_name, infer_cmds)