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

def word_count(path):
    try:
        word_count = int(subprocess.Popen('wc -w < ' + path, shell=True, stdout=subprocess.PIPE).communicate()[0])
    except:
        word_count = 0
    return word_count

class SevenFiftyWords:
    def __init__(self):
        self.directory = os.path.expanduser("~/.750words/")
        if not os.path.exists(self.directory):
            os.mkdir(self.directory)
        # set up configuration
        self.configfile = self.directory + "config"
        self.configuration = ConfigParser.SafeConfigParser()
        try:
            # make sure the configuration file exists
      	    open(self.configfile, 'r')
            self.configuration.read(self.configfile)
        except:
            # set defaults
            self.configuration.add_section('Editor')
            self.configuration.set('Editor', 'command', 'vim')
        finally:
            with open(self.configfile, 'wb') as cfile:
                self.configuration.write(cfile)
                cfile.close()
            self.configuration.read(self.configfile)
    
    def cat(self, args):
        path = self.get_path(args.date)
        if not os.path.exists(path):
            sys.stdout.write('')
        else:
            sys.stdout.write(open(path, 'r').read())
    
    def config(self, args):
        if args.editor:
            self.configuration.set('Editor', 'command', args.editor)
            with open(self.configfile, 'wb') as cfile:
                self.configuration.write(cfile)
                cfile.close()

        for section in self.configuration.sections():
            print section + ":"
            print self.configuration.items(section)
    
    def edit(self, args):
        """Opens up an editor so that you can write the day's words.
        
        Keyword arguments:
          editor: Name of the editor to use. Should be executable from the user's
                  working directory.
    
        Returns the path to today's writing if it contains at least 750 words; False if not.
        """ 
        
        date = args.date
        editor = self.configuration.get('Editor', 'command')
        path = self.get_path(date)
        subprocess.call([editor, path])
        if os.path.exists(path):
            words = word_count(path)
            print 'You have written %i out of 750 words so far.' % words
            if words < 750:
                return False
            else:
                return path
    
    def path(self, args):
        print self.get_path(args.date)
    
    def stats(self, args):
        date = args.date
        try:
            path = self.get_path(date)
            style = subprocess.Popen(['style', path], stdout=subprocess.PIPE).communicate()[0]
        except OSError:
            style = "You must install the 'style' program. Try sudo apt-get install diction."
        sys.stdout.write(style)
    
    def wc(self, args):
        date = args.date
        try:
            path = self.get_path(date)
            words = word_count(path)
        except OSError:
            words = 0
        print words
    
    def get_path(self, date):
        out_dir = os.path.expanduser(self.directory)
        if not os.path.exists(out_dir):
            os.mkdir(os.path.dirname(path))
        file_format = "txt"
        path = os.path.join(out_dir, "%04i-%02i-%02i" % (date.year, date.month, date.day) + '.' + file_format) 
        return path
    
    def main(self):
        # set up argparsers
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()
    
        # cat parser
        cat_parser = subparsers.add_parser('cat', help='cat the text')
        cat_parser.add_argument('date', help="the date of the text", default=parse_date("today"), type=parse_date, nargs='?')
        cat_parser.set_defaults(func=self.cat)
    
        # config parser
        config_parser = subparsers.add_parser('config', help='modify or view configuration')
        config_parser.add_argument('--editor', help="the text editor you wish to use")
        config_parser.set_defaults(func=self.config)
    
        # edit parser
        edit_parser = subparsers.add_parser('edit', help='edit the text')
        edit_parser.add_argument('date', help="the date of the text", default=parse_date("today"), type=parse_date, nargs='?')
        edit_parser.set_defaults(func=self.edit)
    
        # path parser
        path_parser = subparsers.add_parser('path', help='get the path to the text file')
        path_parser.add_argument('date', help="the date of the text", default=parse_date("today"), type=parse_date, nargs='?')
        path_parser.set_defaults(func=self.path)
    
        # stats parser
        stats_parser = subparsers.add_parser('stats', help='view stats')
        stats_parser.add_argument('date', help="the date of the text", default=parse_date("today"), type=parse_date, nargs='?')
        stats_parser.set_defaults(func=self.stats)
    
        # wc parser
        wc_parser = subparsers.add_parser('wc', help='view word count')
        wc_parser.add_argument('date', help="the date of the text", default=parse_date("today"), type=parse_date, nargs='?')
        wc_parser.set_defaults(func=self.wc)
    
        args = parser.parse_args()
    
        # call the specified function
        args.func(args)
    
if __name__ == "__main__":
    sevenfiftywords = SevenFiftyWords()
    sevenfiftywords.main()
