"""
VirtlogdConf - file ``/etc/libvirt/virtlogd.conf``
==================================================

The VirtlogdConf class parses the file ``/etc/libvirt/virtlogd.conf``.
"""
from .. import LegacyItemAccess, Parser, parser
from insights.parsers import split_kv_pairs, get_active_lines
from insights.specs import Specs


@parser(Specs.virtlogd_conf)
class VirtlogdConf(LegacyItemAccess, Parser):
    """Parse content of ``/etc/libvirt/virtlogd.conf``. The virtlogd.conf
    is in the standard ``conf`` file format and is read by the base parser
    class ``LegacyItemAccess``.

    Sample ``/etc/libvirt/virtlogd.conf`` file::

        # Master virtlogd daemon configuration file
        #

        #################################################################
        #
        # Logging controls
        #

        # Logging level: 4 errors, 3 warnings, 2 information, 1 debug
        # basically 1 will log everything possible
        #log_level = 3

        # Logging filters:
        # A filter allows to select a different logging level for a given category
        # of logs
        # The format for a filter is one of:
        #    x:name
        #    x:+name
        #      where name is a string which is matched against source file name,
        #      e.g., "remote", "qemu", or "util/json", the optional "+" prefix
        #      tells libvirt to log stack trace for each message matching name,
        #      and x is the minimal level where matching messages should be logged:
        #    1: DEBUG
        #    2: INFO
        #    3: WARNING
        #    4: ERROR
        #
        # Multiple filter can be defined in a single @filters, they just need to be
        # separated by spaces.
        #
        # e.g. to only get warning or errors from the remote layer and only errors
        # from the event layer:
        #log_filters="3:remote 4:event"

        # Logging outputs:
        # An output is one of the places to save logging information
        # The format for an output can be:
        #    x:stderr
        #      output goes to stderr
        #    x:syslog:name
        #      use syslog for the output and use the given name as the ident
        #    x:file:file_path
        #      output to a file, with the given filepath
        #    x:journald
        #      ouput to the systemd journal
        # In all case the x prefix is the minimal level, acting as a filter
        #    1: DEBUG
        #    2: INFO
        #    3: WARNING
        #    4: ERROR
        #
        # Multiple output can be defined, they just need to be separated by spaces.
        # e.g. to log all warnings and errors to syslog under the virtlogd ident:
        #log_outputs="3:syslog:virtlogd"
        #

        # The maximum number of concurrent client connections to allow
        # over all sockets combined.
        #max_clients = 1024


        # Maximum file size before rolling over. Defaults to 2 MB
        #max_size = 2097152

        # Maximum number of backup files to keep. Defaults to 3,
        # not including the primary active file
        max_backups = 3


    Examples:
        >>> conf.get('max_backups')
        '3'

    Attributes:
        data (dict): Ex: ``{'max_backups': '3'}``
    """
    def parse_content(self, content):
        self.data = split_kv_pairs(get_active_lines(content))
