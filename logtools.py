def clear_log(log_file):
    open(log_file, "w").close()

def add_to_log(step_name, log_file, command=None, description = None):
    with open(log_file, "a") as lfil:
        lfil.write("------------------------------------\n")
        lfil.write("Step: " + step_name + " START\n")
        lfil.write("------------------------------------\n")
        if command is not None:
            lfil.write("CMD:" + command + "\n")
        if description is not None:
            lfil.write(description + "\n")
        lfil.write("\n")

def start_new_log(file_name, email, log_file):
    clear_log(log_file)
    with open(log_file, "a") as lfil:
        lfil.write("====================================\n")
        lfil.write("Sewage Token: " + file_name + "\n")
        lfil.write("Email:" + email + "\n")
        lfil.write("====================================\n")
