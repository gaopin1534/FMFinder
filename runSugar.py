import subprocess
#target csp file
csp_file = ""
#command to run sugar
cmd = "sugar " + csp_file
#output file
result_file = ""
#do while product exists
while True:
    ret  =  subprocess.Popen( cmd.strip(),shell=True,stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout = ret.stdout
    index = 0;
    resultstr = ""
    additional_condition = "(!(&&"
    line = stdout.readline ()
    tmp = line.strip().split(" ")
    if tmp[1].strip() != "SATISFIABLE":
        print "unsatisfiable"
        break
    while True:
        line = stdout.readline ()
        if not line:
          break
        tmp = line.strip().split(" ")
        if(len(tmp)==2):
            result = tmp[1].split("\t")
            print result
            additional_condition += "(= " + result[0] + " " + result[1] + ") "
            if(int(result[1]) == 1):
                resultstr += result[0] + " "
    additional_condition += "))"
    with open(result_file, mode = 'a') as fh:
        fh.write(resultstr + "\n")
    with open(csp_file, mode = 'a') as csp:
        csp.write(additional_condition + "\n")
    print resultstr
    print additional_condition