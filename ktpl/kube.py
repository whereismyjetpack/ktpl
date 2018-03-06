import os
from subprocess import call, check_call, Popen, PIPE

def run_kube_command(stdin, kube_method, retry=True):
    proc = Popen(["kubectl", kube_method, "-f", "-"], stdin=PIPE, stderr=PIPE, stdout=PIPE)
    proc.stdin.write(stdin.encode('utf-8'))
    stdout, stderr = proc.communicate()
    if stderr and retry:
        run_kube_command(stdin, kube_method, retry=False)
    if stderr and not retry:
        print(stderr)
