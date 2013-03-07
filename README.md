check_mysql_tablesize_diskfree.py
=================================

*Purpose: Alerts when copying the largest table will fill the disk.*

Install Requirements
--------------------
`pip install -r requirements.txt`

###Usage:
check_mysql_tablesize_diskfree.py \[-h\] \[-d PARTITION\] \[-P PORT\] \[-u USER\] \[-p PASSWORD\] \[-H HOSTNAME\] \[-w WARNING\] \[-c CRITICAL\] \[-t TIMEOUT\] \[-v\]

###Sample Usage:
`check_mysql_tablesize_diskfree.py -H localhost -u root -w 4 -c 2`

###Allowed arguments:
    -h, --help                              show this help message and exit
    -d PARTITION, --partition=PARTITION     Disk partition to check for free space. (default: /)
    -P PORT, --port=PORT                    The port to be used. (default: 3306)
    -u USER, --user=USER                    Database user. (default: )
    -p PASSWORD, --password=PASSWORD        Database password. (default: )
    -H HOSTNAME, --hostname=HOSTNAME        Database host. (default: )
    -w WARNING, --warning=WARNING           largest table size warning multiplier. For example, if
                                            value is 4, WARNING will be returned if 4 * largest
                                            table size >= partition free space. (default: 1)
    -c CRITICAL, --critical=CRITICAL        largest table size critial multiplier. For example, if
                                            value is 2, CRITICAL will be returned if 2 * largest
                                            table size >= partition free space. (default: 1)
    -t TIMEOUT, --timeout=TIMEOUT           Timeout value. (default: )
    -v, --verbose

