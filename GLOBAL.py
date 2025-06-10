SCALER = 100 # тобто замість 0.1 - 10 і так всюди

NAMESPACE = "nn"

ARCH = [4, 8, 1]
INPUT_FEATURES = ["rooms", "area", "location_score", "age"]
TARGET_FEATURE = "price"
LAYERS = len(ARCH)
EPOCHS = 20
LEARNING_RATE = 1 # 0.01
RAND_INIT_MAX = SCALER//10
NUM_SAMPLES = 100

OBJ_PARAMS = f"{NAMESPACE}_params"    # Ваги (w), зміщення (b)
OBJ_ACTIVATIONS = f"{NAMESPACE}_activs" # Перед-активації (z), активації (a)
OBJ_GRADIENTS = f"{NAMESPACE}_grads"   # Градієнти (dz, dw, db)
OBJ_INPUTS = f"{NAMESPACE}_inputs"     # Вхідні дані для поточного прикладу
OBJ_CONSTS = f"{NAMESPACE}_consts"     # Константи (SCALER, etc.)
OBJ_STATUS = f"{NAMESPACE}_status"     # Лічильники (епоха, індекс прикладу, поточна втрата)
OBJ_TEMP = f"{NAMESPACE}_temp"         # Тимчасові розрахунки

def tellraw_info(message, color="gray"):
    return f'tellraw @a [{{"text":"[NN Info] ","color":"blue"}},{{"text":"{message}","color":"{color}"}}]'

def tellraw_debug(message, color="dark_gray"):
     return f'tellraw @a [{{"text":"[NN Debug] ","color":"dark_purple"}},{{"text":"{message}","color":"{color}"}}]'

def tellraw_error(message):
    return f'tellraw @a [{{"text":"[NN ERROR] ","color":"red"}},{{"text":"{message}","color":"red","bold":true}}]'

def tellraw_param(param_name_str, score_holder, objective, prefix="", suffix=""):
    return f'tellraw @a [{{"text":"{prefix}{param_name_str}: ","color":"gold"}}, {{"score":{{"name":"{score_holder}","objective":"{objective}"}}}}, {{"text":" {suffix}","color":"gold"}}]'

def tellraw_layer_section(layer_name):
    return f'tellraw @a {{"text":"--- {layer_name} ---","color":"light_purple","bold":true}}'

def create_file(file_name, cmds):
    with open(f'../generated_files/{file_name}.mcfunction', 'w') as f:
        f.write("\n".join(cmds))