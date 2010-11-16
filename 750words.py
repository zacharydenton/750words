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

def cat(date):
    path = get_path(date)
    if not os.path.exists(path):
        return ''
    else:
        return open(path, 'r').read()

def edit(date, editor):
    """Opens up an editor so that you can write the day's words.
    
    Keyword arguments:
      editor: Name of the editor to use. Should be executable from the user's
              working directory.

    Returns the path to today's writing if it contains at least 750 words; False if not.
    """ 
    
    path = get_path(date)
    if not os.path.exists(path):
        try:
            os.mkdir(os.path.dirname(path))
        except OSError:
            pass
        open(path, 'w').close() # touch the file
    create_time = os.stat(path).st_mtime
    subprocess.call([editor, path])
    word_count = wc(date)
    print 'You have written %i out of 750 words so far.' % word_count
    if word_count < 750:
        return False
    else:
        return path

def stats(date):
    try:
        path = get_path(date)
        style = subprocess.Popen(['style', path], stdout=subprocess.PIPE).communicate()[0]
    except:
        style = "You must install the 'style' program. Try sudo apt-get install diction."
    return style

def wc(date):
    try:
        path = get_path(date)
        word_count = int(subprocess.Popen('wc -w < ' + path, shell=True, stdout=subprocess.PIPE).communicate()[0])
    except:
        word_count = 0
    return word_count

def get_path(date):
        out_dir = os.path.expanduser('~/.750words/')
        file_format = "txt"
        path = os.path.join(out_dir, "%04i-%02i-%02i" % (date.year, date.month, date.day) + '.' + file_format) 
        return path

def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def parse_date(date):
    '''parses a natural language date'''
    if is_number(date):
        date = int(date)
        return datetime.datetime.today() + (datetime.timedelta(days=1) * date)

    elif isinstance(date, str):
        if date.lower().strip() == 'today':
            return datetime.datetime.today()
        elif date.lower().strip() == 'yesterday':
            return datetime.datetime.today() - datetime.timedelta(days=1)
    return datetime.datetime.today()

def main():
    actions = ('cat', 'edit', 'stats', 'wc')

    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=actions, help="the action you wish to perform")
    parser.add_argument('date', nargs='?', default='today', help="the day on which to perform the action")
    parser.add_argument('--editor', help="the text editor you wish to use", default='vim')
    args = parser.parse_args()

    date = parse_date(args.date)

    if args.action == 'edit':
        edit(date, args.editor)
    elif args.action == 'cat':
        sys.stdout.write(cat(date))
    elif args.action == 'stats':
        print stats(date)
    elif args.action == 'wc':
        print wc(date)

if __name__ == "__main__":
    main()
