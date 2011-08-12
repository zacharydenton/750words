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

import analysis

def which(program):
    import os
    def is_exe(fpath):
        return os.path.exists(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

def is_number(string):
   try:
       float(string)
       return True
   except ValueError:
       return False

def parse_date(date):
    '''parses a natural language date'''
    day = datetime.timedelta(days=1)
    if is_number(date):
        date = int(date)
        return datetime.datetime.today() + (day * date)

    elif isinstance(date, str):
        if date.lower().strip() == 'today':
            return datetime.datetime.today()
        elif date.lower().strip() == 'yesterday':
            return datetime.datetime.today() - day
        elif date.lower().strip() == 'tomorrow':
            return datetime.datetime.today() + day
    return datetime.datetime.today()

GIT_INSTALLED = which('git')

def git_init(path):
    if not os.path.isdir(os.path.join(path, ".git")):
        return subprocess.Popen(['git', 'init', path], stdout=subprocess.PIPE).communicate()[0]

def git_commit(filename, message='edit'):
    os.chdir(os.path.dirname(filename))
    subprocess.call(['git', 'add', os.path.basename(filename)])
    return subprocess.Popen(['git', 'commit', '-m', message], stdout=subprocess.PIPE).communicate()[0]

def git_log(path):
    os.chdir(path)
    subprocess.call(['git', 'log'])

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
            self.configuration.set('Editor', 'command', 'editor')
            self.configuration.add_section('Output')
            self.configuration.set('Output', 'directory', os.path.join(self.directory, 'text'))
        finally:
            with open(self.configfile, 'wb') as cfile:
                self.configuration.write(cfile)
                cfile.close()
            self.configuration.read(self.configfile)
            self.output_dir = self.configuration.get('Output', 'directory')
            if not os.path.exists(self.output_dir):
                os.mkdir(self.output_dir)


    def analyze(self, args):
        from pprint import pprint
        for date in args.date:
            path = self.get_path(date)
            pprint(analysis.analyze(path))
    
    def cat(self, args):
        results = ''
        for date in args.date:
            path = self.get_path(date)
            if not os.path.exists(path):
                output = ''
            else:
                output = open(path, 'r').read()
            sys.stdout.write(output)
            results += output
        return results
    
    def config(self, args):
        if args.editor:
            self.configuration.set('Editor', 'command', args.editor)
            with open(self.configfile, 'wb') as cfile:
                self.configuration.write(cfile)
                cfile.close()
        if args.output:
            output_dir = os.path.expanduser(args.output)
            if os.path.exists(output_dir):
                self.configuration.set('Output', 'directory', output_dir)
                self.update_path(output_dir)
                with open(self.configfile, 'wb') as cfile:
                    self.configuration.write(cfile)
                    cfile.close()
            else:
                print "The path specified,", args.output + ", does not exist."

        for section in self.configuration.sections():
            print section + ":"
            print self.configuration.items(section)

        return [self.configuration.items(section) for section in self.configuration.sections()]
    
    def edit(self, args):
        """Opens up an editor so that you can write the day's words.
        
        Keyword arguments:
          editor: Name of the editor to use. Should be executable from the user's
                  working directory.
    
        Returns the path to today's writing if it contains at least 750 words; False if not.
        """ 
        
        for date in args.date:
            editor = self.configuration.get('Editor', 'command')
            path = self.get_path(date)
            old_wordcount = analysis.word_count(path)
            subprocess.call([editor, path])
            wordcount = analysis.word_count(path)
            difference = wordcount - old_wordcount
            if GIT_INSTALLED:
                message = 'added %i words to %s for a total of %i' % \
                        (difference, os.path.basename(path), wordcount)
                git_commit(path, message)

            if wordcount < 750:
                print 'You have written %i out of 750 words so far.' % wordcount
            else:
                print 'You wrote %i words today. Great job!' % wordcount
    
    def log(self, args):
        git_log(self.output_dir)

    def path(self, args):
        for date in args.date:
            print self.get_path(date)
  
    def wc(self, args):
        for date in args.date:
            path = self.get_path(date)
            wordcount = analysis.word_count(path)
            print wordcount
    
    def get_path(self, date=None):
        if date is None:
            date = datetime.datetime.today()
        file_format = "txt"
        path = os.path.join(self.output_dir, "%04i-%02i-%02i" % (date.year, date.month, date.day) + '.' + file_format) 
        return path

    def update_path(self, path):
        if path == self.output_dir:
            return
        files = os.listdir(self.output_dir)
        for textfile in files:
            if textfile.endswith('.txt'):
                original = os.path.join(self.output_dir, textfile)
                output = os.path.join(path, textfile)
                shutil.move(original, output)
        self.output_dir = path
        if GIT_INSTALLED:
            git_init(self.output_dir)
        return path
    
    def main(self):
        # set up argparsers
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()
    
        # analyze parser
        analyze_parser = subparsers.add_parser('analyze', help='view analysis')
        analyze_parser.add_argument('date', help="the date of the text", default=[parse_date("today")], type=parse_date, nargs='*')
        analyze_parser.set_defaults(func=self.analyze)
    
        # cat parser
        cat_parser = subparsers.add_parser('cat', help='cat the text')
        cat_parser.add_argument('date', help="the date of the text", default=[parse_date("today")], type=parse_date, nargs='*')
        cat_parser.set_defaults(func=self.cat)
    
        # config parser
        config_parser = subparsers.add_parser('config', help='modify or view configuration')
        config_parser.add_argument('-e', '--editor', help="the text editor you wish to use")
        config_parser.add_argument('-o', '--output', help="the directory in which to store your texts")
        config_parser.set_defaults(func=self.config)
    
        # edit parser
        edit_parser = subparsers.add_parser('edit', help='edit the text')
        edit_parser.add_argument('date', help="the date of the text", default=[parse_date("today")], type=parse_date, nargs='*')
        edit_parser.set_defaults(func=self.edit)
    
        # log parser
        if GIT_INSTALLED:
            log_parser = subparsers.add_parser('log', help='print the git log')
            log_parser.set_defaults(func=self.log)

        # path parser
        path_parser = subparsers.add_parser('path', help='get the path to the text file')
        path_parser.add_argument('date', help="the date of the text", default=[parse_date("today")], type=parse_date, nargs='*')
        path_parser.set_defaults(func=self.path)
    
        # wc parser
        wc_parser = subparsers.add_parser('wc', help='view word count')
        wc_parser.add_argument('date', help="the date of the text", default=[parse_date("today")], type=parse_date, nargs='*')
        wc_parser.set_defaults(func=self.wc)
    
        if len(sys.argv) == 1:
            # default when no command is specified
            args = parser.parse_args(['edit'])
        else:
            # call the specified function
            args = parser.parse_args()
        args.func(args)
    
if __name__ == "__main__":
    sevenfiftywords = SevenFiftyWords()
    sevenfiftywords.main()
