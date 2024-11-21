import subprocess
import psutil

def kill_process_tree(pid):
    try:
        parent = psutil.Process(pid)
        for child in parent.children(recursive=True):
            child.kill()
        parent.kill()
    except psutil.NoSuchProcess:
        pass

def execute_command(command, timeout=None):
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            output, error = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            kill_process_tree(process.pid)
            return "Timeout"
        
        if process.returncode != 0:
            if error:
                return error.decode("utf-8")
            if output:
                return output.decode("utf-8")
            assert False, "Command failed with no output"
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        return e.output.decode("utf-8")