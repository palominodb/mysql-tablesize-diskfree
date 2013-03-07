#!/usr/bin/env python

import os

import MySQLdb
import pynagios
from pynagios import Plugin, Response, make_option
import sys


def get_freespace(p):
    """Returns the number of free kilobytes on the drive that p is on."""
    s = os.statvfs(p)
    return s.f_bsize * s.f_bavail / 1024


class CheckMysqlTableSizeDiskFree(Plugin):
    """Diskspace check to alert when running pt-osc will run out of space."""

    port = make_option(
        '-P', '--port', dest='port', type='int', default=3306,
        help='The port to be used')
    user = make_option(
        '-u', '--user', dest='user', default='', help='Database user')
    password = make_option(
        '-p', '--password', dest='password', default='',
        help='Database password')
    partition = make_option(
        '-d', '--partition', dest='partition', default='/',
        help='Disk partition to check for free space.')

    def __init__(self, args=sys.argv):
        # add help for warning and critical options
        try:
            for option in self._options:
                if option.dest == 'warning':
                    option.help = (
                        'largest table size warning multiplier. '
                        'For example, if value is 4, '
                        'WARNING will be returned if '
                        '4 * largest table size >= partition free space.')
                elif option.dest == 'critical':
                    option.help = (
                        'largest table size critial multiplier. '
                        'For example, if value is 2, '
                        'CRITICAL will be returned if '
                        '2 * largest table size >= partition free space.')
        except Exception, e:
            # Fail silently
            pass

        super(CheckMysqlTableSizeDiskFree, self).__init__(args)

    def check(self):
        try:
            host = self.options.hostname if self.options.hostname else ''

            conn = MySQLdb.connect(
                host=host, port=self.options.port,
                user=self.options.user, passwd=self.options.password)
            with conn:
                cursor = conn.cursor()

                query = """
                    SELECT
                        CONCAT(table_schema, '.', table_name),
                        CONCAT(ROUND(( data_length + index_length ) / ( 1024 ))) nagios_check_total_size
                    FROM
                        information_schema.TABLES
                    ORDER BY data_length + index_length DESC
                    LIMIT  1
                    """

                cursor.execute(query)

                row = cursor.fetchone()

                table_name = row[0]
                table_size = row[1]

                msg = 'largest table: {0} - {1}kB; '.format(table_name,
                    table_size)
                critical_multiplier = (
                    float(self.options.critical.__str__())
                    if self.options.critical else 1.0)
                warning_multiplier = (
                    float(self.options.warning.__str__())
                    if self.options.warning else 1.0)

                partition_freespace = get_freespace(self.options.partition)
                msg += 'free space on {0}: {1}kB; '.format(
                    self.options.partition, partition_freespace)

                critical_level = float(table_size) * critical_multiplier
                warning_level = float(table_size) * warning_multiplier

                if partition_freespace <= critical_level:
                    status = pynagios.CRITICAL
                elif partition_freespace <= warning_level:
                    status = pynagios.WARNING
                else:
                    status = pynagios.OK

                cursor.close()

            return Response(status, msg)

        except Exception, e:
            return Response(pynagios.UNKNOWN, 'ERROR: {0}'.format(e))

if __name__ == "__main__":
    # Instantiate the plugin, check it, and then exit
    CheckMysqlTableSizeDiskFree().check().exit()
