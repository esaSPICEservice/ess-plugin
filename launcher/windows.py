import subprocess
import os

def execute_windows(root_scenario_path, session_file_path):
    print('Launcher!!!')

    working_dir = os.path.join(
        os.path.dirname(__file__)
    )
    cmd = os.path.join(
        working_dir,
        'OSVE_APP.exe'
    )

    process = subprocess.Popen([cmd, '-r', root_scenario_path, '-s', session_file_path],
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE,
                        cwd=working_dir)
    stdout, stderr = process.communicate()
    print(stdout.decode())

    return process.returncode