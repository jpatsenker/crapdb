import time

CONTACT_EMAIL = "<contact-email>"

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

def add_big_description(description, log_file):
    with open(log_file, "a") as lfil:
        lfil.write("\n***\nDescription:\n***\n" + description + "\n***\n")

def start_new_log(file_name, email, log_file):
    clear_log(log_file)
    with open(log_file, "a") as lfil:
        lfil.write("====================================\n")
        lfil.write("Job File: " + file_name + "\n")
        lfil.write("Email:" + email + "\n")
        lfil.write("====================================\n")

def add_start(log_file):
    with open(log_file, "a") as lfil:
        lfil.write("Start time: " + str(time.clock()) + "\n")

def add_end(log_file):
    with open(log_file, "a") as lfil:
        lfil.write("End time: " + str(time.clock()) + "\n")

def add_line_to_log(log_file, line):
    with open(log_file, "a") as lfil:
        lfil.write(str(line) + "\n")

def add_fatal_error(log_file, error):
    with open(log_file, "a") as lfil:
        lfil.write("!!!!!!!FATAL ERROR\n")
        lfil.write("!!!!!!!" + error + "\n")
        lfil.write("!!!!!!!FATAL ERROR\n")
        lfil.write("Please contact " + CONTACT_EMAIL + " for support\n")

def end_log(log_file):
    with open(log_file, "a") as lfil:
        lfil.write("====================================\n")
        lfil.write("FINISHED PROCESSING JOB, TIME: " + str(time.clock()) + "\n")
        lfil.write("SENDING EMAIL WITH RESULTS!!!\n")
        lfil.write("====================================\n")