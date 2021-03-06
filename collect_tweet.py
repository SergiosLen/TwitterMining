#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sample script that collects tweets matching a string.

'''Collect tweets matching a text pattern and store them
continuously in JSON-formatted lines of a local file.'''

__author__ = 'Giorgos Keramidas <gkeramidas@gmail.com>'
__moderator__ = 'sergioslenis@gmail.com'

import argparse
import errno
import json
import os
import sys
import twitter 
import ast
import time
import pickle


FROM_DATE=None#'2015-01-15' '2008-02-28'
MAX_ID=None

def load_login_cred(args):#.auth,args.auth_dict):
    '''Loads the credentials for Twitter api from a file if exists or create a new file'''
    credentials=dict()
    if args.auth!=None:
        f=open(args.auth)
        for li in f:
            li=li.strip()
            lil=li.split(' , ')
            credentials[lil[0]]=lil[1]
        f.close()
    elif args.auth_dict!=None:
        f=open(args.auth_dict)
        credentials=pickle.load(f)
        f.close()


    else:
        print 'Go to http://twitter.com/apps/new to create an app and get these items.'
        'Consumer key, Consumer secret, Access token, Access token secret'
        credentials['CONSUMER_KEY']=raw_input('Give me the Consumer key: ')
        credentials['CONSUMER_SECRET']=raw_input('Give me the Consumer secret: ')
        credentials['OAUTH_TOKEN']=raw_input('Give me the Access token: ')
        credentials['OAUTH_TOKEN_SECRET']=raw_input('Give me the Access token secret: ')
        f=open('auth_cred.txt','w')
        for i in credentials:

            f.write(i+' , '+str(credentials[i])+'\n')
        f.close()
    return credentials


def login(credentials):

    auth = twitter.Api(consumer_key=credentials['CONSUMER_KEY'], \
        consumer_secret=credentials['CONSUMER_SECRET'], \
        access_token_key=credentials['OAUTH_TOKEN'],\
         access_token_secret=credentials['OAUTH_TOKEN_SECRET'])

    return auth

def search(text,args, max_pages=10, results_per_page=100,sin_id=None):#,args.auth,args.auth_dict):
    """Generator for searching 'text' in Twitter content

Search the public Twitter timeline for tweets matching a 'text' string,
which can also be a hash tag, and yield a batch of matched tweets every
time we have some results.

Args:
text str, the text to search for in Twitter. This can
be a plain text string or a '#hashtag' to look
for tweets of this topic only.
max_pages int, maximum number of result 'pages' to obtain
from Twitter's backlog of archived tweets. When
not specified, default to 10 pages.
results_per_page int, maximum number of results per page to fetch
from Twitter's backlog of archived tweets. When
not specified, default to 100 tweets per page.

Returns:
An array of dicts. Every dict in the returned array is a 'result' from
twitter.Twitter.search and represents a single tweet.
"""
    credentials=load_login_cred(args)#.auth,args.auth_dict)
    if 'CONSUMER_KEY' in credentials:
        auth=login(credentials)
    else:
        credentials=credentials[credentials.keys()[0]]
        auth=login(credentials)

    while True:

        for page in range(1, max_pages + 1):
            print MAX_ID,'================'
            yield auth.GetSearch(term=text,until=sin_id,count=results_per_page,max_id=MAX_ID)

def preload_tweets(filename):
    """Preload previously seen tweets from a text file.

Args:
filename str, Name of the file where we preload tweets from.

Returns:
A set() containing all the numeric 'id' attributes of tweets we have
already seen.
"""
    # print filename[:-4]
    # import glob
    # json_files = glob.glob('*.json')
    # print json_files
    import fnmatch
    import os
    # print os.listdir(filename.split('/')[0])
    json_files=[]
    for files in os.listdir(filename.split('/')[0]):
        if fnmatch.fnmatch(files, '*.json'):
            json_files.append(os.path.join('%s' % filedir,files))
    print json_files
    # print aaaa
    # if len(json_files) == 0:
    # raise RuntimeError('No json files to convert.')
    if not os.path.isfile(filename):
        print '1'
        # if not os.path.isfile(filename[:-4]):
        if len(json_files) == 0:
        
            print '2'
            # print aaaaaaaa
            return set()
        else:
            print '3'
            filename_i=open(filename,'a+')
            seen = set()

            for filenm in json_files:
                try:
                    # print filename,'bbb'
                    filename_o=open(filenm)
                    # print filename
                    for k in filename_o:
                        # print k
                        try:
                            # kk=json.loads(ast.literal_eval(k))
                            kk=json.loads(k)
                            # print type(kki)
                            # kk=json.loads(kki)
                            # print kk.keys()
                            # print type(kk)
                            # for key, value in kk.items():

                            #     if key=='id':
                            #         # print key
                            #         iid=value

                            seen.add(kk['id'])
                            print >> filename_i, json.dumps(kk['id'])
                        except Exception, e:
                            print e,'st'
                            print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
                            continue
                        
                except Exception, e:
                    seen = set() # Avoid returning partial results on error
                    print len(seen),e,'st'
                    print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
                filename_o.close()
        # filename_i=open(filename)
        # filename_o.close()
        # return set()
    # if not filename
    # print 'hdhhhhh'
    else:
        print '4'
        try:
            seen = set()
            # print filename,'bbb'
            filename_o=open(filename)
            # print filename
            for k in filename_o:
                # print k
                try:
                    # kk=json.loads(ast.literal_eval(k))
                    kk=json.loads(k)

                    
                    # for key, value in kk.items():

                    #     if key=='id':
                    #         # print key
                    #         iid=value

                    seen.add(kk)
                except Exception, e:
                    print e
                    print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
                    continue
                
        except Exception, e:
            seen = set() # Avoid returning partial results on error
            print len(seen),e
            print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
    # print len(seen)
    # print filename
    filename_o.close()
    # print aaa
    return seen

def streamsearch(ofile, text,args, max_pages=2000, results_per_page=200,from_date=FROM_DATE):
    """Stream the results of searching for 'text' to the 'ofile' output file

Args:
ofile str, the name of a file where we will write any tweets
we find. Tweets are written in JSON format, with every
tweet being stored in a separate line as a Python dict.
text str, the text to search for in Twitter. This can
be a plain text string or a '#hashtag' to look
for tweets of this topic only.
max_pages int, maximum number of result 'pages' to obtain
from Twitter's backlog of archived tweets. When
not specified, default to 10 pages.
results_per_page int, maximum number of results per page to fetch
from Twitter's backlog of archived tweets. When
not specified, default to 100 tweets per page.

Returns:
None
"""
    # Load the id of already seen tweets, if there are any.
    global MAX_ID
    ofilename = ofile or 'standard output'
    seen = ofile+'.ids' and preload_tweets(ofile+'.ids') or set()

    # from_date=FROM_DATE
    if seen:
        print '%d tweets preloaded from %s' %(len(seen), ofile+'.ids')
    try:
        ostream = ofile and file(ofile, 'a+') or sys.stdout
        fop=open( ofile+'.ids', 'a+')

        u=0
        for matches in search(text,args, max_pages=max_pages, sin_id=from_date,
                              results_per_page=results_per_page):#,args.auth,args.auth_dict):
            
            u+=1
            newmatches = 0
            uu=0
            for tweet in matches:
                # print uu
                uu+=1
            
                (tid, tuser, text, cr_at) = (tweet.GetId() ,tweet.GetUser(),
                                      tweet.GetText(), tweet.GetCreatedAt()) #['id'], ['from_user'] ['text']
                tweet=tweet.AsDict()
                # print tid,cr_at
                if not tid in seen:
                    newmatches += 1
                    seen.add(tid)
                    print >> ostream, json.dumps(tweet)
                    print >> fop, json.dumps(tid)
             
            if newmatches > 0:
                print '%d new tweets logged at %s' %(newmatches, ofilename)
            print u,len(matches),'aa',MAX_ID,cr_at
            MAX_ID=tid
            
        ostream.close()
        fop.close()    
    except IOError, e:
        if ostream and ostream != sys.stdout:
            ostream.close()
        print 'Error writing at file "%s". %s' %(ofilename, e)
        print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=(
        'Collect tweets matching a text pattern and store them'
    'continuously in JSON-formatted lines of a local file.'))
    parser.add_argument('-o', '--output',nargs='?', metavar='Output FILE', type=str,
        default='Out_json', help='output folder name')
    parser.add_argument('-s', '--search',nargs='?', metavar='Search term', type=str,
        default=None, help='Search term')

    parser.add_argument('-c', '--auth_dict',nargs='?', metavar='credentials dict', type=str,
        default=None, help='credentials dictionary file name') 
    parser.add_argument('-d', '--auth',nargs='?', metavar='credentials file', type=str,
        default=None, help='credentials file name') 
    argsr = parser.parse_args()
    # print argsr
    filedir=argsr.output
    try:
        os.stat(filedir)
    except:
        os.mkdir(filedir)
    filenam=argsr.search
    filename=''
    for l in filenam.split():
        filename+=l+'_'

    json_filename = filename[:-1]+'_dic.json' # Where to store matching tweets
    lookup_text = unicode(argsr.search,'utf-8')# Text to search for
    # ids_filename = filename[:-1]+'_ids'
    outfile_name = os.path.join('%s' % filedir,json_filename)
   
    while True:
        try:
            streamsearch(outfile_name, lookup_text,argsr)#,maid_id=maid)
        except twitter.TwitterError, e:
            print 'Skipping HTTP error %s [...]' %str(e).split('\n')[0]
            time.sleep(900)

            pass
