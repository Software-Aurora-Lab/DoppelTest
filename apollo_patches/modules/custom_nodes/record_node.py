import os
import sys
import subprocess

if __name__ == '__main__':
    # bazel run //modules/custom_nodes:record_node start test
    # /apollo/bazel-bin/modules/custom_nodes/record_node start test
    mode = sys.argv[1] if len(sys.argv) > 2 else ''
    TEMP_OUTPUT_PATH = "/apollo/records"

    if mode == "start":
        cyber_recorder = "/apollo/bazel-bin/cyber/tools/cyber_recorder/cyber_recorder"
        start_record_cmd = f'{cyber_recorder} record -i 600 -o {TEMP_OUTPUT_PATH}/{sys.argv[2]} -a &'

        subprocess.Popen(start_record_cmd,
                         shell=True,
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
    else:
        cmd = "python3 /apollo/scripts/record_bag.py --stop --stop_signal SIGINT"
        subprocess.run(cmd.split(), stdout=subprocess.DEVNULL,
                       stdin=subprocess.DEVNULL)
