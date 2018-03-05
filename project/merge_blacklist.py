import subprocess


shell_cmd = 'python .\get_blacklist\\malwaredomains.py'
p = subprocess.Popen(shell_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
while p.poll() is None:
    line = p.stdout.readline()
    line = line.strip()
    if line:
        print('Subprogram output: [{}]'.format(line))
if p.returncode == 0:
    print('Subprogram success')
else:
    print('Subprogram failed')