import os
from subprocess import call, check_call, Popen, PIPE

def run_kube_command(stdin, kube_method):
    proc = Popen(["kubectl", kube_method, "-f", "-"], stdin=PIPE)
    # print(stdin)
    proc.stdin.write(stdin.encode('utf-8'))
    stdout, stderr = proc.communicate()