#!/usr/bin/env python
"""
Flush control for ep-engine.

Copyright (c) 2010  Dustin Sallings <dustin@spy.net>
"""
import time

import clitool

def stop(mc):
    mc.stop_persistence()
    stopped = False
    while not stopped:
        time.sleep(0.5)
        try:
            stats = mc.stats()
            success = True
        except:
            if success:
                # XXX: Need some way to force a reconnect.
                # mc = mc_bin_client.MemcachedClient(host, port)
                raise
            else:
                raise
            success = False
            if stats['ep_flusher_state'] == 'paused':
                stopped = True

if __name__ == '__main__':

    c = clitool.CliTool("""Available params:
    min_data_age   - minimum data age before flushing data"
    queue_age_cap  - maximum queue age before flushing data"
    max_txn_size   - maximum number of items in a flusher transaction
    bg_fetch_delay - delay before executing a bg fetch (test feature)
    max_size       - max memory used by the server""")

    c.addCommand('stop', stop)
    c.addCommand('start', 'start_persistence')
    c.addCommand('set', 'set_flush_param', 'set param value')
    c.addCommand('evict', 'evict_key', "evict key")

    c.execute()
