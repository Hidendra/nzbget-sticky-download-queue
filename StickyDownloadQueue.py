#!/usr/bin/env python

#
# Sticky download queue for NZBGet
#
# Copyright (C) 2021 Tyler Blair <tyler@viru.ca>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

##############################################################################
### NZBGET QUEUE SCRIPT                                                    ###

# NZBs that begin downloading will change priority to continue downloading
# until completion.
#
# Once an NZB begins downloading the priority for it will be changed to
# FORCE (or the configured priority).
#
# This will cause downloads to be done in a predictable order where queue
# sorting or newly added nzbs (with a lower priority) won't interrupt and
# stop an already running download.
#
# This is useful for limited storage situations where it is desirable to
# always finish a download once it is started before moving onto a different
# NZB.
#
# Script version: 1.0.0
#
# NOTE: This script requires Python 2 or 3 installed on your system.

##############################################################################
### OPTIONS                                                                ###

# The priority in-progress NZBs will be set to.
# force = 900; very high = 100; high = 50; normal = 0
#DownloadPriority=900

### NZBGET QUEUE SCRIPT                                                    ###
##############################################################################

import os
import sys

try:
    # Python 3.x
    from xmlrpc.client import ServerProxy
except ImportError:
    # Python 2.x
    from xmlrpclib import ServerProxy


PP_SUCCESS=93
PP_ERROR=94


def nzbget_connect_xml_rpc():
    host = os.environ['NZBOP_CONTROLIP']
    port = os.environ['NZBOP_CONTROLPORT']
    username = os.environ['NZBOP_CONTROLUSERNAME']
    password = os.environ['NZBOP_CONTROLPASSWORD']
    
    if host == '0.0.0.0':
        host = '127.0.0.1'

    rpc_url = 'http://%s:%s@%s:%s/xmlrpc' % (username, password, host, port);

    return ServerProxy(rpc_url)


def main():
    if os.environ.get('NZBNA_EVENT') not in ['FILE_DOWNLOADED']:
        return 0

    download_priority = os.environ.get('NZBPO_DOWNLOADPRIORITY', None)

    if not download_priority:
        print('DownloadPriority is missing from the script configuration.')
        return PP_ERROR

    # The ID of the NZB being downloaded.
    # The priority for this will be changed to the configured priority.
    # Not much validation is done here as this is triggered off of the
    # FILE_DOWNLOADED event so it can be safely assumed that this is being
    # actively downloaded.
    downloading_nzb_id = int(os.environ.get('NZBNA_NZBID'))

    current_priority = os.environ.get('NZBNA_PRIORITY')

    # Priority doesn't need to change!
    if current_priority == download_priority:
        return PP_SUCCESS

    print('[INFO] Setting priority for NZB ID %d to %s' % (downloading_nzb_id, download_priority))

    nzbget = nzbget_connect_xml_rpc()
    nzbget.editqueue('GroupSetPriority', str(download_priority), [downloading_nzb_id])
 
    return PP_SUCCESS
    

if __name__ == '__main__':
    sys.exit(main())

