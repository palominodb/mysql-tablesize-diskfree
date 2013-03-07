    Usage: check_mysql_tablesize_diskfree.py [options]

    Options:
      -d PARTITION, --partition=PARTITION
                            Disk partition to check for free space.
      -P PORT, --port=PORT  The port to be used
      -u USER, --user=USER  Database user
      -p PASSWORD, --password=PASSWORD
                            Database password
      -v, --verbose
      -H HOSTNAME, --hostname=HOSTNAME
      -w WARNING, --warning=WARNING
                            largest table size warning multiplier. For example, if
                            value is 4, WARNING will be returned if 4 * largest
                            table size >= partition free space.
      -c CRITICAL, --critical=CRITICAL
                            largest table size critial multiplier. For example, if
                            value is 2, CRITICAL will be returned if 2 * largest
                            table size >= partition free space.
      -t TIMEOUT, --timeout=TIMEOUT
      -h, --help            show this help message and exit
