#!/bin/bash

echo "###############################################################"
echo "Check that we have the speedtest cli utility"
if [[ ! -f speedtest-cli ]]
then
    echo "  speedtest-cli does not exist; fetching..."
    #https://github.com/sivel/speedtest-cli
    wget -O speedtest-cli https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py
    chmod +x speedtest-cli 
else
    echo "  speedtest-cli exists OK"
fi

echo "###############################################################"
echo "Setup files and directory names"
dataDir=./data
mkdir -p ${dataDir}
base_name=${dataDir}/data_file

thedate=$(date "+%Y%m%d")
thetime=$(date "+%H%M%S")
file_name=speedtest_${thedate}_${thetime}

data_name=${dataDir}/${file_name}.csv
temp_file=${dataDir}/${file_name}.tmp

echo "  Output file_name : ${data_name}"
echo "  Temp file name   : ${temp_file}"

echo "###############################################################"
echo "Running speedtest-cli"
./speedtest-cli > ${temp_file}
echo "  Done"

echo "###############################################################"
echo "Converting to output to csv"
echo "---------------------------------------------------------------"
cat  ${temp_file}
python3 speedtest_parser.py ${temp_file} ${thedate} ${thetime} > ${data_name}
echo "---------------------------------------------------------------"
cat ${data_name}

echo "###############################################################"
export PGHOST=192.168.72.140
export PGPORT=5432
export PGDATABASE=internetstats
export PGUSER=postgres
export PGPASSWORD=password

echo "Loading to Database"

#CREATE DATABASE internetstats;
#CREATE TABLE speedtest (speedtestdate INTEGER NOT NULL, speedtestime INTEGER NOT NULL, servername CHARACTER VARYING(256) NOT NULL, pingms NUMERIC(16,4), download numeric(16,4), upload numeric(16,4));
#CREATE VIEW V_SPEEDTEST AS ( select speedtestdate || '-' || lpad(speedtestime::text,6, '0') as datetime, servername ,pingms ,download ,upload from speedtest );

psql -c "select count(*) as before from speedtest;"
psql -c "\copy speedtest from '${data_name}' DELIMITER '|'"  
psql -c "select count(*) as after from speedtest;"
psql -c "select * from V_SPEEDTEST order by datetime desc limit 10;"

echo "###############################################################"
echo "Removing files ${data_name} ${temp_file}"
rm ${data_name} ${temp_file}

echo "###############################################################"
echo "Createing png chart"
python3 graphit.py
ls -al *.png

echo "Done Done"