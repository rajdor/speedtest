# SpeedTest

This is a simple project that combines some shell scripting, python, postgres and charts.

It is a wrapper for speedtest-cli (https://github.com/sivel/speedtest-cli) that formats the output for loading to a database.

```
./speedtest.sh 
###############################################################
Check that we have the speedtest cli utility
  speedtest-cli exists OK
###############################################################
Setup files and directory names
  Output file_name : ./data/speedtest_20200429_210504.csv
  Temp file name   : ./data/speedtest_20200429_210504.tmp
###############################################################
Running speedtest-cli
  Done
###############################################################
Converting to output to csv
---------------------------------------------------------------
Retrieving speedtest.net configuration...
Testing from Telstra Internet (120.147.18.197)...
Retrieving speedtest.net server list...
Selecting best server based on ping...
Hosted by Telstra (Melbourne) [1.24 km]: 20.466 ms
Testing download speed................................................................................
Download: 76.77 Mbit/s
Testing upload speed................................................................................................
Upload: 27.45 Mbit/s
---------------------------------------------------------------
20200429|210504|Telstra (Melbourne) [1.24 km]|20.466|76.77|27.45
###############################################################
Loading to Database
 before 
--------
      6
(1 row)

COPY 1
 after 
-------
     7
(1 row)

    datetime     |                 servername                 | pingms  | download | upload  
-----------------+--------------------------------------------+---------+----------+---------
 20200429-210504 | Telstra (Melbourne) [1.24 km]              | 20.4660 |  76.7700 | 27.4500
 20200429-204212 | Telstra (Melbourne) [1.24 km]              | 18.2680 |  76.3900 | 26.3700
 20200429-203906 | Telstra (Melbourne) [1.24 km]              | 19.5030 |  59.2900 | 25.2600
 20200429-203647 | Vocus Communications (Melbourne) [1.24 km] | 19.3120 |  70.3800 | 31.0200
 20200429-203422 | Vocus Communications (Melbourne) [1.24 km] | 20.3440 |  61.0600 | 32.9700
 20200429-202141 | Vocus Communications (Melbourne) [1.24 km] | 18.6640 |  50.3300 | 28.9600
 20200429-201951 | Vocus Communications (Melbourne) [1.24 km] | 17.6800 |  51.4300 | 31.6200
(7 rows)

###############################################################
Removing files ./data/speedtest_20200429_210504.csv ./data/speedtest_20200429_210504.tmp
###############################################################
Createing png chart
Connected to internetstats
Fetching records
Calculating chart scale
  max ping    : 20.466
  max download:76.77
  latest row  : 2020.04.29 21:05:04
Making chart
  Rows : 7
Done
-rw-r--r-- 1 jarrod jarrod 52134 Apr 29 21:05 speedtestchart.png
Done Done
```
