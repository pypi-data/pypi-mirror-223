from subprocess import PIPE, Popen


def run_simple_command(cmd: str):
    # cmd = cmd.split(" ")
    with Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE) as prc:
        stdout, stderr = prc.communicate()
        if stdout:
            stdout = stdout.decode("utf-8")
        if stderr:
            stderr = stderr.decode("utf-8")
        prc.terminate()
    return stdout, stderr
