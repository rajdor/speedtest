import sys

infile = sys.argv[1]
date = sys.argv[2]
time = sys.argv[3]

ping     = "null"
server   = "null"
download = "null"
upload   = "null"

with open(infile, 'r') as f:

    for line in f:
        
        if "Hosted by " in line:
            server = line.replace("Hosted by ","")
            server = server.split(":")
            ping = server[1].strip()
            ping = ping.replace(" ms","")
            server = server[0].strip()

        if "Download: " in line:
            download = line.replace("Download: ","")
            download = download.replace(" Mbit/s","")
            download = download.strip()
            download = download.replace(" .","")
            if download.startswith("."):
                download = download[1:]
        if "Upload:" in line:
            upload = line.replace("Upload:","")
            upload = upload.replace(" Mbit/s","")
            upload = upload.strip()
            upload = upload.replace(" .","")
            if upload.startswith("."):
                upload = upload[1:]

    #Failed
    if ping != "null":
        if float(ping) >= 1800000.00:
            ping = "null"
    if upload != "null":
        if float(upload) <= 00.00:
            upload = "null"
    if download != "null":
        if float(download) <= 00.00:
            download = "null"

print (str(date) + "|" + str(time) + "|" + str(server) + "|" + str(ping) + "|" + str(download) + "|" + str(upload))