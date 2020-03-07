def csvwrite(filename,*vartuple):
    import csv,io,sys
    ot='w'; nl=''
    if sys.version_info < (3, 0): ot='wb'; nl=None
    try:
        with io.open(filename, ot, newline=nl) as csvfile:
            delimiter=","
            w=csv.writer(csvfile,delimiter=delimiter)
            w.writerow(list(vartuple))
    except Exception as e:
        pass

def ipsubject(type="number"):
    import socket
    name=socket.gethostname()
    ipp=socket.gethostbyname(name)
    ipa=ipp.split(".")
    if type=="name":
        return name
    else: 
        return int(ipa[3])