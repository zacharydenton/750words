Introduction
------------

This is a command-line version of [750 Words][]. I really like the idea
of writing 750 words daily, but I don't like the idea of having all of
my words on someone else's server. I also wanted to write my 750 words
in Vim, with Git version control.

Therefore, I wrote this script. You get all the benefits of writing 750
words daily, within the comfort of your preferred text editor. You also
get the peace-of-mind that comes with having your words as tangible
plain-text files on your on machine, tracked with Git. You don't (yet)
get the cool analysis features that are on the 750 words website, but
this is something that I would like to improve.

Installation
------------

Clone the repository, and execute:

    $ sudo python setup.py install

Or whatever you do to install Python scripts on your machine.

If you want version control with Git, you're going to want to install
that as well.

Configuration
-------------

There are three things to configure: which editor to use, where to store
your words, and what file extension to use. Edit the configuration file
`~/.750words/config` to suit your needs:

    [750words]
    editor = vim
    extension = .md
    directory = /home/zach/docs/journal

Usage
-----

Every day, type `750words` and type at least 750 words. You'll
experience major improvements in creativity and a clear mind.

Here's the full output of `750words -h`:

    usage: 750words [-h] [-p] [--config CONFIG] [dates [dates ...]]

    positional arguments:
      dates            the date of the text

    optional arguments:
      -h, --help       show this help message and exit
      -p, --path       print out path for use with external scripts
      --config CONFIG  the location of the configuration file

Have fun!

Examples
--------

Write the day's words:

```bash
$ 750words
```

To see how much you wrote in August 2011:

```bash
$ wc $(dirname $(750words -p))/2011-08-*
```

  [750 Words]: http://750words.com/
