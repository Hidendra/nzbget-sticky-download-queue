# nzbget-sticky-download-queue

StickyDownloadQueue extension script for NZBGet.

This script will change the priority for an in-progress NZB download to FORCE
(or another configured priority) so that it continues to download until
completion.

The motivation for this is when using a completed directory that is quite
small, NZBGet can fill up the disk easily as files are added (with a high
priority) or the queue is sorted (e.g. using the QueueSort script). Once an NZB
starts downloading, it will continue to download to completion without being
interrupted.

This uses the `FILE_DOWNLOADED` event from NZBget which keeps implementation
simple -- at this point it will have downloaded ~50-100 MB which is acceptable
lag time to adjust the priority to keep it downloading.

