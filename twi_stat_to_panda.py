# -*- coding: utf-8 -*-
import httplib
from urlparse import urlparse
import json

class TweetToPandas(object):
    """docstring for TweetToPandas"""
    def __init__(self, dici,r_or_p):
        super(TweetToPandas, self).__init__()
        # self.arg = arg

        self.hashtags=set()
        self.photo=0
        self.video=[]
        self.canttell=[]
        self.coordinates=''
        self.bbox=None
        self.screen_name=None
        self.user_id=None
        self.followers_count=None
        self.friends_count=None
        self.statuses_count=None
        self.mentions=None
        self.mention_count=0
        useus=dici.get('user',None)
        self.text=dici['text'].encode('utf-8')
        if r_or_p=='ruby':

            entities=dici.get('entities',None)
            if entities!=None:
                hashtags=entities.get('hashtags',None)
                if hashtags!=None:
                    for ht in hashtags:
                        self.hashtags.add(ht['text'].lower().encode('utf-8'))
                if 'user_mentions' in entities:
                    men_set=set()
                    for mention in entities['user_mentions']:
                        men_set.add((mention['id'],mention['screen_name'].encode('utf-8')))
                    self.mention_count=len(men_set)
                    self.mentions=list(men_set)
                    # print type(entities['user_mentions']),entities['user_mentions']
                    # print len(entities['user_mentions'])
                    # print len(men_set)

                    # print dici['text'].encode('utf-8')
                    # print aaa
                if 'urls' in entities:
                    # with httplib.HTTPConnection(url.hostname, url.port) as conn:
                        for ur in entities['urls']:
                            if 'media' in ur:
                                if ur.get('type',None) == 'photo':
                                    self.photo+=1
                            else:
                                if 'http://t.co/' in ur['expanded_url']:
                                    url = urlparse(ur['url'])
                                    conn=httplib.HTTPConnection(url.hostname, url.port)
                                    # print url.path,ur['expanded_url'],ur
                                    conn.request('HEAD', url.path)
                                    rsp=conn.getresponse()
                                    if rsp.status in (301,401):
                                        nurl=rsp.getheader('location')
                                    else:
                                        nurl=ur['expanded_url']

                                    # if 'youtube' in rsp.getheader('location') or 'vimeo' in rsp.getheader('location'):
                                    #     self.video.append(rsp.getheader('location'))
                                else:
                                    nurl=ur['expanded_url']
                                if any([i in nurl for i in ('youtube','vimeo')]):
                                    self.video.append(nurl)
                                else:
                                    self.canttell.append(nurl)
                                # else:
                                #     self.canttell.append(ur['expanded_url'])
        elif r_or_p=='python':                  
            hts=dici.get('hashtags',None)
            # print dici
            # print '============='
            if hts:
                # print hts,'+++++++++++++++++++++++++',type(hts)
                for ht in hts:
                    # self.hashtags.add(ht)
                    self.hashtags.add(ht['text'].lower().encode('utf-8'))
            # entities=dici.get('entities',None)
            # if entities!=None:
            #     hashtags=entities.get('hashtags',None)
            #     if hashtags!=None:
            #         for ht in hashtags:
            #             self.hashtags.add(ht['text'].lower().encode('utf-8'))
                # if 'urls' in entities:
                    # with httplib.HTTPConnection(url.hostname, url.port) as conn:
                        # for ur in entities['urls']:
            if 'media' in dici:
                # print dici['media'],'mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm',type(hts)
                for ur in dici['media']:
                    # print ur
                # ur=dici['media']
                    if ur.get('type',None) == 'photo':
                        self.photo+=1
                    # else:
                    if 'http://t.co/' in ur['expanded_url']:
                        url = urlparse(ur['url'])
                        conn=httplib.HTTPConnection(url.hostname, url.port)
                        # print url.path,ur['expanded_url'],ur
                        conn.request('HEAD', url.path)
                        rsp=conn.getresponse()
                        if rsp.status in (301,401):
                            nurl=rsp.getheader('location')
                        else:
                            nurl=ur['expanded_url']

                        # if 'youtube' in rsp.getheader('location') or 'vimeo' in rsp.getheader('location'):
                        #     self.video.append(rsp.getheader('location'))
                    else:
                        nurl=ur['expanded_url']
                    # print nurl,'/////////////////////////////////'
                    if any([i in nurl for i in ('youtube','vimeo')]):
                        self.video.append(nurl)
                    else:
                        self.canttell.append(nurl)

        # self.hashtag_count=0
        # self.media=None
        self.created_at=dici.get('created_at',None)
        self.id=dici.get('id_str',None)
        self.text=dici.get('text',None)
        self.lang=dici.get('lang',None)
        self.retweet_count=dici.get('retweet_count',None)
        self.retweeted=dici.get('retweeted',None)
        self.in_reply_to_user_id_str=dici.get('in_reply_to_user_id_str',None)
        # coord=dici.get('coordinates',None)
        # if coord != None:
        #     self.coordinates=coord.get('coordinates',None)

        self.coordinates=json.dumps(dici.get('coordinates',''))
        bplace=dici.get('place',None)
        if bplace != None:
            self.bbox=bplace.get('bounding box',None)
        place=dici.get('place',None)

        # if isinstance(place,dict):

        #     self.place=unicode(place.get('full_name',None))
        # else:
        self.place=place
        if useus:
            # print useus.keys()
            self.screen_name=useus['screen_name'].encode('utf-8')
            self.user_id=useus.get('id',None)
            self.followers_count=useus.get('followers_count',None)
            self.friends_count=useus.get('friends_count',None)
            self.statuses_count=useus.get('statuses_count',None)
            self.listed_count=useus.get('listed_count')
        else:
            self.screen_name=None
            self.user_id=None
            self.followers_count=None
            self.friends_count=None
            self.statuses_count=None
            self.listed_count=None

        # self.video=None
        # self.photo=None
        # self.dici=dici

    def as_list(self):
        return [self.id,self.lang,self.retweet_count,self.place,self.created_at,len(self.hashtags),len(self.photo),len(self.canttell),len(self.video)]
    def as_dict(self):
        # return {'id':self.id,'lang':self.lang,'retweet count':self.retweet_count,'Place':self.place,'Created At':self.created_at,'Number of Hashtags':len(self.hashtags),'Number of Photos':len(self.photo),'Number of Cant tell':len(self.canttell),'Number of video':len(self.video)}
        return {'id':self.id,'lang':self.lang,'retweet_count':self.retweet_count,'place':self.place,'created_at':self.created_at,'hashtag_count':len(self.hashtags),'Number of Photos':len(self.photo),'Number of Cant tell':len(self.canttell),'Number of video':len(self.video),'coordinates':self.coordinates,'bounding':self.bbox}

    def as_dict_hash(self):
        return ({'hashtags':self.hashtags},{'id':self.id,'lang':self.lang,'retweet_count':self.retweet_count,'place':self.place,'created_at':self.created_at,'hashtag_count':len(self.hashtags),'Number of Photos':len(self.photo),'Number of Cant tell':len(self.canttell),'Number of video':len(self.video),'coordinates':self.coordinates,'bounding':self.bbox})
    def hsa_as_dic_hash(self):
        return ({'hashtags':self.hashtags}, {'id':self.id,'lang':self.lang,'retweet_count':self.retweet_count,'place':self.place,
        'created_at':self.created_at,'hashtag_count':len(self.hashtags),'hashtags':list(self.hashtags),
         'coordinates':self.coordinates,'bounding':self.bbox,
        'followers_count':self.followers_count,
        'friends_count':self.friends_count,'statuses_count':self.statuses_count,'listed_count':self.listed_count})

    def users_as_dict_hash(self):
        return ({'hashtags':self.hashtags}, {'id':self.id,'lang':self.lang,'retweet_count':self.retweet_count,'place':self.place,
        'created_at':self.created_at,'hashtag_count':len(self.hashtags),'hashtags':list(self.hashtags),
        'Number of Photos':self.photo, 'Number of Cant tell':len(self.canttell),
        'Mentions':self.mentions, 'mention_count':self.mention_count,
        'Number of video':len(self.video), 'coordinates':self.coordinates,'bounding':self.bbox,
        'screen_name':self.screen_name,'user_id':self.user_id,'followers_count':self.followers_count,
        'friends_count':self.friends_count,'statuses_count':self.statuses_count,'text':self.text,'listed_count':self.listed_count})
# usdi['screen_name'],usdi['id_str'],usdi['followers_count'],usdi['friends_count'],usdi['statuses_count']
# 
# self.screen_name=None
# self.user_id=None
# self.followers_count=None
# self.friends_count=None
# self.statuses_count=None