#!/usr/bin/env python
import sys
import os
import glob
import shutil
import getopt
import mc_bin_client

def usage(err=None):
    print >> sys.stderr, """
Usage: %s [--vacuum] [--backupto=<dest_dir>]
""" % os.path.basename(sys.argv[0])

    if err:
        print >> sys.stderr, err
    sys.exit(1)

def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], '', ['vacuum', 'backupto='])
    except getopt.GetoptError, e:
        usage(e.msg)

    if not opts:
        usage()

    cmd_dir = os.path.dirname(sys.argv[0])
    bin_dir = '/usr/local/bin'
    flushctl = os.path.join(cmd_dir, 'flushctl.py')
    sqlitebin = os.path.join(bin_dir, 'sqlite3')

    optdict = dict(opts)
    shouldVacuum = '--vacuum' in optdict

    dest_dir = optdict.get("--backupto")

    mc = mc_bin_client.MemcachedClient('127.0.0.1')
    db_path = mc.stats()['ep_dbname']
    db_files = glob.glob('%s*' % db_path)

    print 'Pausing persistence... ',
    os.system('"%s" 127.0.0.1:11211 stop' % flushctl)
    print 'paused.'
    try:
        for fn in db_files:

            if shouldVacuum and (fn == db_path or fn.endswith('.sqlite')):
                print "Vacuuming", fn
                os.system('"%s" "%s" vacuum' % (sqlitebin, fn))

            if dest_dir:
                dest_fn = os.path.join(dest_dir, os.path.basename(fn))
                print 'Copying %s to %s' % (fn, dest_fn)
                shutil.copyfile(fn, dest_fn)
    finally:
        print 'Unpausing persistence.'
        os.system('"%s" 127.0.0.1:11211 start' % flushctl)


if __name__ == '__main__':
    main()
