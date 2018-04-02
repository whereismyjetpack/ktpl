import os
from subprocess import call, check_call, Popen, PIPE
from tempfile import NamedTemporaryFile


def run_kube_command(stdin, kube_method, retry=True):
    f = NamedTemporaryFile(delete=False)
    f.write(stdin.encode())
    f.close()
    proc = Popen(["kubectl", kube_method, "-f", f.name], stdin=PIPE, stderr=PIPE, stdout=PIPE)
    stdout, stderr = proc.communicate()
    os.unlink(f.name)
    if stderr and retry:
        run_kube_command(stdin, kube_method, retry=False)
    if stderr and not retry:
        print(stderr)
    if stdout:
        print(stdout.decode())
