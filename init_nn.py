from GLOBAL import *

file_name = "init_nn"

init_cmds = [
    tellraw_info("Initialize neural net..."),
    # clear last initialization
    f"scoreboard objectives remove {OBJ_PARAMS}",
    f"scoreboard objectives remove {OBJ_ACTIVATIONS}",
    f"scoreboard objectives remove {OBJ_GRADIENTS}",
    f"scoreboard objectives remove {OBJ_INPUTS}",
    f"scoreboard objectives remove {OBJ_CONSTS}",
    f"scoreboard objectives remove {OBJ_STATUS}",
    f"scoreboard objectives remove {OBJ_TEMP}",

    f"scoreboard objectives add {OBJ_PARAMS} dummy",
    f"scoreboard objectives add {OBJ_ACTIVATIONS} dummy",
    f"scoreboard objectives add {OBJ_GRADIENTS} dummy",
    f"scoreboard objectives add {OBJ_INPUTS} dummy",
    f"scoreboard objectives add {OBJ_CONSTS} dummy",
    f"scoreboard objectives add {OBJ_STATUS} dummy",
    f"scoreboard objectives add {OBJ_TEMP} dummy",
    "",
    f"scoreboard players set SCALER {OBJ_CONSTS} {SCALER}",
    f"scoreboard players set LEARNING_RATE {OBJ_CONSTS} {LEARNING_RATE}",
    f"scoreboard players set NUM_SAMPLES {OBJ_CONSTS} {NUM_SAMPLES}",
    f"scoreboard players set ZERO {OBJ_CONSTS} 0",
    f"scoreboard players set ONE {OBJ_CONSTS} 1", # Для інкрементів
    f"scoreboard players set TWO {OBJ_CONSTS} 2", # Для ділення втрат на 2
    f"scoreboard players set RAND_INIT_MAX_VAL {OBJ_CONSTS} {RAND_INIT_MAX}",
    "",
]

# ваги та зміщення
for layer in range(LAYERS-1):
    num_neurons_in = ARCH[layer]
    num_neurons_out = ARCH[layer+1]
    for i in range(num_neurons_out):
        init_cmds.append(f"scoreboard players set b_{layer}_{i} {OBJ_PARAMS} 0");
        for j in range(num_neurons_in):
            init_cmds.extend([
                f"execute store result score temp_rand {OBJ_TEMP} run random roll 0..{RAND_INIT_MAX * 2}",
                f"scoreboard players operation temp_rand {OBJ_TEMP} -= RAND_INIT_MAX_VAL {OBJ_CONSTS}",
                f"scoreboard players set w{layer}_{i}_{j} {OBJ_PARAMS} 0",
                f"scoreboard players operation w{layer}_{i}_{j} {OBJ_PARAMS} = temp_rand {OBJ_TEMP}",
            ])

init_cmds.extend([
    "",
    f"scoreboard players set current_epoch {OBJ_STATUS} 0", # Почнемо з 1-ї епохи у start_training
    f"scoreboard players set current_sample_idx {OBJ_STATUS} 0",
    f"scoreboard players set total_epochs {OBJ_STATUS} {EPOCHS}",
    f"scoreboard players set current_epoch_loss_sum_scaled {OBJ_STATUS} 0",
    "",
    tellraw_info(f"Initialized successfully. Use /function {NAMESPACE}:start_training to start training.", "green")
])

create_file(file_name, init_cmds)