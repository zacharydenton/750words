#!/usr/bin/env python
# 750words on the command line.
import os
import sys
import subprocess
import tempfile
import shutil
import argparse
import datetime
import ConfigParser

def write_today(editor):
    """Opens up an editor so that you can write the day's words.
    
    Keyword arguments:
      editor: Name of the editor to use. Should be executable from the user's
              working directory.

    Returns the path to today's writing if it contains at least 750 words; False if not.
    """ 
    
    temp_dir = tempfile.mkdtemp()
    out_dir = os.path.expanduser('~/.750words/')
    file_format = "txt"
    today = datetime.datetime.today()
    path = os.path.join(out_dir, "%4i-%2i-%2i" % (today.year, today.month, today.day) + '.' + file_format) 
    if not os.path.exists(path):
        os.mkdir(os.path.dirname(path))
        open(path, 'w').close() # touch the file
    create_time = os.stat(path).st_mtime
    subprocess.call([editor, path])
    word_count = int(subprocess.Popen('wc -w < ' + path, shell=True, stdout=subprocess.PIPE).communicate()[0])
    print 'You have written %i out of 750 words so far.' % word_count
    if word_count < 750:
        return False
    else:
        return path

def cat_today():
    out_dir = os.path.expanduser('~/.750words/')
    file_format = "txt"
    today = datetime.datetime.today()
    path = os.path.join(out_dir, "%4i-%2i-%2i" % (today.year, today.month, today.day) + '.' + file_format) 
    if not os.path.exists(path):
        sys.stdout.write('')
    else:
        sys.stdout.write(open(path, 'r').read())

def stats_today():
    pass

def main():
    actions = ('cat', 'edit', 'stats')

    parser = argparse.ArgumentParser()
    parser.add_argument('action', nargs='?', default='edit', choices=actions)
    parser.add_argument('--editor', help="The editor you wish to use to write your words.", default='vim')
    args = parser.parse_args()

    if args.action == 'edit':
        write_today(args.editor)
    elif args.action == 'cat':
        cat_today()
    elif args.action == 'stats':
        stats_today()

if __name__ == "__main__":
    main()
