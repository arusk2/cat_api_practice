import os

output = os.popen('flask --app api_final --debug run')
while True:
    line = output.readline()
    if line:
        print(line, end='')
    else:
        break
output.close()