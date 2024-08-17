import subprocess
import sys

arg1 = sys.argv[1]

print("the parameter is")
print(arg1)

worker_script_path = "../worker/scripts/worker.sh"

subprocess.run([worker_script_path, arg1], capture_output=True, text=True)

print("------------Finish reloading the server-----------------------")
