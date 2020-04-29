import psycopg2
import pygal
import math
import os
from pygal.style import DefaultStyle

try:
    conn = psycopg2.connect(  "dbname="      + os.environ['PGDATABASE']  \
                            +  " user='"     + os.environ['PGUSER']      \
                            + "' host='"     + os.environ['PGHOST']      \
                            + "' password='" + os.environ['PGPASSWORD'] + "'")
except:
    print ("Unable to connect to the database: " + os.environ['PGDATABASE'])
print ("Connected to " + os.environ['PGDATABASE'])

print ("Fetching records")
cur = conn.cursor()
cur.execute("select * from V_SPEEDTEST where to_timestamp(datetime, 'YYYYMMDD-hh24miss') > now() - interval '30 Day' order by datetime asc")
rows = cur.fetchall()

date_time    = ()
ping_ms      = []
download     = []
upload       = []
lastUpdated  = ""

for row in rows:
    lastUpdated = row[0]
    date_time = date_time + (row[0],)
    ping_ms.append(float(row[2]))
    download.append(float(row[3]))
    upload.append(float(row[4]))

print ("Calculating chart scale")
max_ping = max(ping_ms)
max_download = max(download)
print ("  max ping    : " + str(max_ping))
print ("  max download:" + str(max_download))

min_x = -10
max_primary = (int(math.ceil(max_download / 10.0)) * 10) + 10
max_secondary = max_primary
max_scale = (max_primary / 10 ) + 1
lastUpdated = lastUpdated[0:4] + "." + lastUpdated[4:6] + "."  + lastUpdated[6:8] + " " + lastUpdated[9:11] + ":" + lastUpdated[11:13] + ":" + lastUpdated[13:15]
print ("  latest row  : " + lastUpdated)

print ("Making chart")
print ("  Rows : " + str(len(rows)))
labelInterval= len(rows) % 20
if labelInterval < 20:
    labelInterval = 1

line_chart = pygal.Line(style=DefaultStyle,width=1920, height=1080, x_label_rotation=90, x_labels_major_every=labelInterval, show_minor_x_labels=False, min_scale=max_scale, max_scale=max_scale, range=(min_x, max_primary), secondary_range=(min_x, max_primary))
line_chart.title = 'Internet Speed test : Last updated : ' + lastUpdated
line_chart.x_labels = date_time
line_chart.add('download', download)
line_chart.add('upload', upload)
line_chart.add('ping_ms', ping_ms, secondary=True)
line_chart.render_to_png('speedtestchart.png')

print ("Done")
