Introduction
------------
This is a command-line version of [750 Words](http://750words.com/). I really like the idea of writing 750 words daily, but I don't like the idea of having all of my words on someone else's server. I also wanted to write my 750 words in Vim, with Git version control.

Therefore, I wrote this script. You get all the benefits of writing 750 words daily, within the comfort of your preferred text editor. You also get the peace-of-mind that comes with having your words as tangible plain-text files on your on machine, tracked with Git. You don't (yet) get the cool analysis features that are on the 750 words website, but this is something that I would like to improve.

Installation
------------
Clone the repository, and execute:
	
	$ sudo python setup.py install

Or whatever you do to install Python scripts on your machine.

If you want version control with Git, you're going to want to install that as well.

Configuration
-------------
There's only two things that need to be configured: which editor to use, and where to store your words.

Usage
-----
Every day, type `750words` and type at least 750 words. You'll experience major improvements in creativity and perhaps a reduction in stress, as well.

There are some other things you can do as well:

	usage: 750words [-h] {wc,log,edit,cat,path,analyze,config} ...

	positional arguments:
	  {wc,log,edit,cat,path,analyze,config}
	    analyze             view analysis
	    cat                 cat the text
	    config              modify or view configuration
	    edit                edit the text
	    log                 print the git log
	    path                get the path to the text file
	    wc                  view word count

	optional arguments:
	  -h, --help            show this help message and exit

Have fun!
