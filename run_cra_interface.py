try:
    import sys

    from aux.jobs import Job
    """
    Interface for running run_cra from php
    """


    command_string = "python run_cra.py"

    """
    for a in sys.argv[1:]:
        command_string += " " + a

    print command_string + "\n"

    job = Job(command_string)
    job.run(wait=True, output="interface_test_out", error="interface_test_err")
    """

    print "done"
except Exception:
    print "ono"