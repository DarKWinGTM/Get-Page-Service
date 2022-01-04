import re
import os
import sys
import glob
import time
import json
import pytz
import random
import _thread
import datetime
import grequests
import cloudscraper
from inspect import currentframe as SourceCodeLine
from flask import Flask, json, jsonify, request, redirect, session, send_from_directory, Response, make_response, render_template
import gc

# IMPORT FOR PYREPLIT
import typer, requests, zipfile, shutil, logging
import snow_pyrepl as pyrepl

timedate = datetime.datetime
timezone = pytz.timezone

app = Flask(
    __name__, 
    static_url_path = '', 
    static_folder   = 'static',
    template_folder = 'templates'
)

__version__ = "1.1.9"

try:
	__sid__ = 's%3AiRnjOZamIqSXYxyaNvTWsL_6gVfI6QeP.%2FnMg%2F6SW3Hz7AnUyRcxNXiYARSCyY%2FVaSIUuLiiO9mc'
except:
	__sid__ = None

app = typer.Typer()



def grequests_except_handler(request, excetion):
    print(f'{ timedate.now() } EXCEPT : HANDLER { request.url }')




def get_json(user, name, sid):
	headers = {
		'Content-Type'      : 'application/json',
		'connect.sid'       : sid,
		'X-Requested-With'  : 'https://replit.com',
		'Origin'            : 'https://replit.com',
        'referer'           : f'https://replit.com/@{ user }/{ name }',
		'User-Agent'        : 'Mozilla/5.0'
	}
	cookies = {
		"connect.sid"       : sid
	}
	r = requests.get(
        f"https://replit.com/data/repls/@{ user }/{ name }", 
        headers=headers, 
        cookies=cookies
    )
	return r.json()['id']

def get_token(user, name, sid):
    r = cloudscraper.create_scraper(
        delay   = 32
    ).get(
        f'https://replit.com/@{ user }/{ name }', 
        headers = {
    		'Content-Type'      : 'application/json',
    		'connect.sid'       : sid,
    		'X-Requested-With'  : 'https://replit.com',
    		'Origin'            : 'https://replit.com',
            'referer'           : f'https://replit.com/@{ user }/{ name }',
            'Cache-Control'     : 'no-cache',
            'Cookie'            : f'connect.sid={ sid }; ',
        },
    	cookies = {
    		'connect.sid'       : sid
    	},
        timeout = 32
    )
    #   print( r )
    #   print( r.content )
    data = json.loads(r.text.split("<script id=\"__NEXT_DATA__\" type=\"application/json\">")[1].split("</script>")[0])['props']['pageProps']['connectionMetadata']
    return data['token'], f"{data['gurl']}/wsv2/{data['token']}"

def chk_token(user, name, sid):
    try:
        r = cloudscraper.create_scraper(
            delay   = 32
        ).get(
            f'https://replit.com/@{ user }/{ name }', 
            headers = {
        		'Content-Type'      : 'application/json',
        		'connect.sid'       : sid,
        		'X-Requested-With'  : 'https://replit.com',
        		'Origin'            : 'https://replit.com',
                'referer'           : f'https://replit.com/@{ user }/{ name }',
                'Cache-Control'     : 'no-cache',
                'Cookie'            : f'connect.sid={ sid }; ',
            },
        	cookies = {
        		'connect.sid'       : sid
        	},
            timeout = 32
        )
        #   print( r )
        #   print( r.content )
        #   data = json.loads(r.text.split("<script id=\"__NEXT_DATA__\" type=\"application/json\">")[1].split("</script>")[0])['props']['pageProps']['connectionMetadata']
        #   return data['token'], f"{data['gurl']}/wsv2/{data['token']}"
        print(f'{ timedate.now() } CHECK :: { SourceCodeLine().f_lineno } :: { user } { name } - { r.status_code }')
        return r.status_code
    except:
        print(f'{ timedate.now() } CHECK :: { SourceCodeLine().f_lineno } :: { user } { name } - 503')
        return 503

@app.command(help="Output the current version for Replit CLI")
def version():
	typer.echo(__version__)






class PYREPLIT():
    def __init__(
        self, 
        repl:str, 
        #   code:str
    ):
        
        self.repl = repl
        #   self.code = code
        
    def operation(
        self
    ):
        
        _thread.start_new_thread(self.shell, ())

    def connect(
        self, 
        vals
    ):
        
        while True:

            # GET REPLIT ID
            try:
                if self.id == None:
                        self.id                 = get_json(self.user, self.name, self.key)
            except Exception as e:
                print(f'{ timedate.now() } ERROR :: { SourceCodeLine().f_lineno } :: NOT SHARED REPLIT { self.user } { self.name } { e }')
                time.sleep(4)
                continue
            break
        
        while True:

            # GET REPLIT TOKEN AND URL
            try:
                if self.token == None or self.url == None:
                        self.token, self.url    = get_token(self.user, self.name, self.key)
                        open(f'{ self.user }_{ self.name }.json', 'w').write(json.dumps({
                                'id'    : self.id,
                                'token' : self.token,
                                'url'   : self.url
                        }, indent = 4))
            except Exception as e:
                self.token      = None
                self.url        = None
                self.client     = None
                self.runner     = None
                print(f'{ timedate.now() } ERROR :: { SourceCodeLine().f_lineno } :: NOT TOKEN REPLIT { self.user } { self.name } { e }')
                time.sleep(4)
                continue
        
            try:
                self.client             = pyrepl.Client(self.token, self.id, self.url)
            except Exception as e:
                self.token      = None
                self.url        = None
                self.client     = None
                self.runner     = None
                print(f'{ timedate.now() } ERROR :: { SourceCodeLine().f_lineno } :: NOT CLIENT REPLIT { self.user } { self.name } - { e }')
                time.sleep(4)
                continue
        
            try:
                self.runner             = self.client.open(vals, '')
            except Exception as e:
                self.token      = None
                self.url        = None
                self.client     = None
                self.runner     = None
                print(f'{ timedate.now() } ERROR :: { SourceCodeLine().f_lineno } :: NOT RUNNER REPLIT { self.user } { self.name } - { e }')
                time.sleep(4)
                continue
            break
        
        
        print( timedate.now(), 'USER  ::::', self.user )
        print( timedate.now(), 'NAME  ::::', self.name )
        print( timedate.now(), 'ID    ::::', self.id )
        print( timedate.now(), 'SOCK  :::: run_', self.runner )
        #   print( 'KEY   ::::', self.key )
        #   print( 'TOKEN ::::', self.token )
        #   print( 'URL   ::::', self.url )
    def shell(
        self
    ):
        
        self.user               = self.repl.split("/")[0]
        self.name               = self.repl.split("/")[1]
        self.key                = __sid__.strip()
        self.token              = None if not os.path.isfile( f'{ self.user }_{ self.name }.json' ) else json.load(open( f'{ self.user }_{ self.name }.json' ))['token']
        self.url                = None if not os.path.isfile( f'{ self.user }_{ self.name }.json' ) else json.load(open( f'{ self.user }_{ self.name }.json' ))['url']
        self.client             = None
        self.id                 = None if not os.path.isfile( f'{ self.user }_{ self.name }.json' ) else json.load(open( f'{ self.user }_{ self.name }.json' ))['id']
        self.runner             = None
        
        self.connect('shellrun2')
        
        while True:
                
            try:
                if random.randrange(100) >= 92:
                    self.output = self.runner.run({
                        'clear':{
                        }
                    }); #   print( self.output )

                    time.sleep(5)

                self.output = self.runner.run({
                    'runMain':{
                    }
                }); #   print( self.output )

                time.sleep(5)

                self.output = self.runner.run({
                    'runMain':{
                    }
                }); #   print( self.output )

                time.sleep(5)

                self.output = self.runner.run({
                    'runMain':{
                    }
                }); #   print( self.output )
                time.sleep(5)
                
            except Exception as e:
                print(f'{ timedate.now() } ERROR :: { SourceCodeLine().f_lineno } :: { self.user } { self.name } - { e }')
                time.sleep(4)
                self.connect('shellrun2')
                break
            
            time.sleep( random.randrange(3) )
            
            break

    def kills(
        self
    ):
        
        self.user               = self.repl.split("/")[0]
        self.name               = self.repl.split("/")[1]
        self.key                = __sid__.strip()
        self.token              = None if not os.path.isfile( f'{ self.user }_{ self.name }.json' ) else json.load(open( f'{ self.user }_{ self.name }.json' ))['token']
        self.url                = None if not os.path.isfile( f'{ self.user }_{ self.name }.json' ) else json.load(open( f'{ self.user }_{ self.name }.json' ))['url']
        self.client             = None
        self.id                 = None if not os.path.isfile( f'{ self.user }_{ self.name }.json' ) else json.load(open( f'{ self.user }_{ self.name }.json' ))['id']
        self.runner             = None
        
        self.connect('exec')

        while True:
                
            try:
                
                self.output = self.runner.run({
		            "exec": {
		            	"args": ['kill', '1']
		            }
                }); #   print( self.output )
                time.sleep(5)

                
            except Exception as e:
                print(f'{ timedate.now() } ERROR :: { SourceCodeLine().f_lineno } :: { self.user } { self.name } - { e }')
                time.sleep(4)
                self.connect('exec')
                continue
            
            time.sleep( random.randrange(3) )
            
            break

    def gits(
        self
    ):
        
        self.user               = self.repl.split("/")[0]
        self.name               = self.repl.split("/")[1]
        self.key                = __sid__.strip()
        self.token              = None if not os.path.isfile( f'{ self.user }_{ self.name }.json' ) else json.load(open( f'{ self.user }_{ self.name }.json' ))['token']
        self.url                = None if not os.path.isfile( f'{ self.user }_{ self.name }.json' ) else json.load(open( f'{ self.user }_{ self.name }.json' ))['url']
        self.client             = None
        self.id                 = None if not os.path.isfile( f'{ self.user }_{ self.name }.json' ) else json.load(open( f'{ self.user }_{ self.name }.json' ))['id']
        self.runner             = None
        
        self.connect('exec')

        while True:
                
            try:
                
                self.output = self.runner.run({
		            "exec": {
		            	"args": [ 'git', 'fetch' '--all' ]
		            }
                }); #   print( self.output )
                time.sleep(2)
                self.output = self.runner.run({
		            "exec": {
		            	"args": [ 'git', 'reset', '--hard' ]
		            }
                }); #   print( self.output )
                time.sleep(2)
                self.output = self.runner.run({
		            "exec": {
		            	"args": [ 'git', 'reset', '--hard', 'origin/master' ]
		            }
                }); #   print( self.output )
                time.sleep(2)
                self.output = self.runner.run({
		            "exec": {
		            	"args": [ 'git', 'stash', 'save', "''" ]
		            }
                }); #   print( self.output )
                time.sleep(2)
                self.output = self.runner.run({
		            "exec": {
		            	"args": [ 'git', 'pull']
		            }
                }); #   print( self.output )
                time.sleep(2)

                
            except Exception as e:
                print(f'{ timedate.now() } ERROR :: { SourceCodeLine().f_lineno } :: { self.user } { self.name } - { e }')
                time.sleep(4)
                self.connect('exec')
                continue
            
            time.sleep( random.randrange(5) )
            
            break

#   git fetch --all; git reset --hard; git reset --hard origin/master; git stash save ''; git pull; 
















class WEBCHECK():
    def __init__(
        self, 
        data = [], 
        mode = 'run'
    ):
        
        self.data = data
        self.mode = mode
        
    def thread(
        self
    ):
        if self.mode == 'run':
            self.thread = _thread.start_new_thread(self.run, ())
        if self.mode == 'chk':
            self.thread = _thread.start_new_thread(self.chk, ())
        if self.mode == 'ace':
            self.thread = _thread.start_new_thread(self.ace, ())
            

    def run(
        self
    ):
    
        while True:
        
            self.load = []
            self.resp = []
            self.list = []
            self.gate = []
            self.root = []
            
            for self.base in self.data:
                self.user               = self.base.split("/")[0]
                self.name               = self.base.split("/")[1]
                self.load.append(grequests.get(
                    f'https://{ self.name }.{ self.user }.repl.co/login', 
                    timeout = 12
                ))
                self.gate.append(f'https://{ self.name }.{ self.user }.repl.co')
                try:
                    self.root.append(f'https://{0}.repl.co/login'.format(
                        "" if not os.path.isfile( f'{ self.user }_{ self.name }.json' ) else json.load(open( f'{ self.user }_{ self.name }.json' ))['id']
                    ))
                except:
                    os.remove(f'{ self.user }_{ self.name }.json')
                    self.root.append(f'https://{0}.repl.co/login'.format("" ))
                #   self.root                 = 
                #   self.runner             = None
                
            self.resp.append(
                grequests.map(self.load)
            )
            self.resp.append(
                grequests.map(self.load)
            )
            self.resp.append(
                grequests.map(self.load)
            )
                
            for self.aaaa, self.bbbb in enumerate( self.resp ):
                
                self.list.append([])
                
                for self.cccc, self.dddd in enumerate( self.resp[ self.aaaa ] ):
                    try:
                        self.list[self.aaaa].append( self.resp[self.aaaa][self.cccc].status_code )
                    except:
                        self.list[self.aaaa].append( 502 )
            
            for self.aaaa, self.bbbb in enumerate( self.list ):
                for self.cccc, self.dddd in enumerate( self.list[ self.aaaa ] ):
                    
                    if (len([
                        self.eeee[ self.cccc ] for self.eeee in self.list if self.eeee[ self.cccc ] == 200
                    ]) <= 1 or not ([
                        self.eeee[ self.cccc ] for self.eeee in self.list
                    ][-1] == 200)) and not self.gate[self.cccc] == None:
                        
                        self.gate[self.cccc] = None
                        
                        print( f'{ timedate.now() } { self.thread } 503 : {self.cccc:02n}', self.load[self.cccc].url, [
                            self.eeee[ self.cccc ] for self.eeee in self.list
                        ] )
                        
                        PYREPLIT(
                            repl = '/'.join([
                                re.split('/|\.', self.load[self.cccc].url)[3], 
                                re.split('/|\.', self.load[self.cccc].url)[2]
                            ])
                        ).gits()
                        if random.randrange(100) >= 86:
                            PYREPLIT(
                                repl = '/'.join([
                                    re.split('/|\.', self.load[self.cccc].url)[3], 
                                    re.split('/|\.', self.load[self.cccc].url)[2]
                                ])
                            ).kills()
                        if random.randrange(100) >= 48:
                            chk_token(
                                re.split('/|\.', self.load[self.cccc].url)[3], 
                                re.split('/|\.', self.load[self.cccc].url)[2], 
                                __sid__.strip()
                            )
                        
                        PYREPLIT(
                            repl = '/'.join([
                                re.split('/|\.', self.load[self.cccc].url)[3], 
                                re.split('/|\.', self.load[self.cccc].url)[2]
                            ])
                        ).shell()
                        
                        try     : 
                            if not self.root[self.cccc] == '':
                                _thread.start_new_thread(requests.get(self.root[self.cccc]) , ())
                        except  : pass
                        try     : 
                            if not self.root[self.cccc] == '':
                                _thread.start_new_thread(requests.get(f'https://render-tron.appspot.com/screenshot/{ self.root[self.cccc] }'), ())
                        except  : pass

                    elif (len([
                        self.eeee[ self.cccc ] for self.eeee in self.list if self.eeee[ self.cccc ] == 200
                    ]) >= 1 or ([
                        self.eeee[ self.cccc ] for self.eeee in self.list
                    ][-1] == 200)) and not self.gate[self.cccc] == True:
                    
                        self.gate[self.cccc] = True
                        

                        print( f'{ timedate.now() } { self.thread } 200 : {self.cccc:02n}', self.load[self.cccc].url )

                        if random.randrange(100) >= 50:
                            chk_token(
                                re.split('/|\.', self.load[self.cccc].url)[3], 
                                re.split('/|\.', self.load[self.cccc].url)[2], 
                                __sid__.strip()
                            )
                        
                        try     : 
                            if not self.root[self.cccc] == '':
                                _thread.start_new_thread(requests.get(self.root[self.cccc]) , ())
                        except  : pass
                        try     : 
                            if not self.root[self.cccc] == '':
                                _thread.start_new_thread(requests.get(f'https://render-tron.appspot.com/screenshot/{ self.root[self.cccc] }'), ())
                        except  : pass

                        try     : 
                            if re.search('awcloud-token', self.load[self.cccc].url):
                                _thread.start_new_thread(requests.get(self.load[self.cccc].url.replace('/login', '')), ())
                            else:
                                _thread.start_new_thread(requests.get(self.load[self.cccc].url.replace('/login', '/run')), ())
                        except  : pass
                        try     : _thread.start_new_thread(requests.post(self.load[self.cccc].url.replace('/login', '')), ())
                        except  : pass
                        try     : _thread.start_new_thread(requests.get(f'https://render-tron.appspot.com/screenshot/{ self.load[self.cccc].url.replace("/login", "") }'), ())
                        except  : pass
                    
            print('\n'.join([str( f'{ timedate.now() } { self.thread } DONE ' + str(x) ) for x in self.list]))
            time.sleep( 10 )
    def chk(
        self
    ):
    
        while True:
        
            self.load = []
            self.resp = []
            self.list = []
            self.gate = []
            self.root = []
            
            for self.base in self.data:
                self.user               = self.base.split("/")[0]
                self.name               = self.base.split("/")[1]
                self.load.append(grequests.get(
                    f'https://{ self.name }.{ self.user }.repl.co', 
                    timeout = 12
                ))
                self.gate.append(f'https://{ self.name }.{ self.user }.repl.co')
                try:
                    self.root.append(f'https://{0}.repl.co'.format(
                        "" if not os.path.isfile( f'{ self.user }_{ self.name }.json' ) else json.load(open( f'{ self.user }_{ self.name }.json' ))['id']
                    ))
                except:
                    os.remove(f'{ self.user }_{ self.name }.json')
                    self.root.append(f'https://{0}.repl.co'.format("" ))
                #   self.root                 = 
                #   self.runner             = None
                
            self.resp.append(
                grequests.map(self.load)
            )
            self.resp.append(
                grequests.map(self.load)
            )
            self.resp.append(
                grequests.map(self.load)
            )
                
            for self.aaaa, self.bbbb in enumerate( self.resp ):
                
                self.list.append([])
                
                for self.cccc, self.dddd in enumerate( self.resp[ self.aaaa ] ):
                    try:
                        self.list[self.aaaa].append( self.resp[self.aaaa][self.cccc].status_code )
                    except:
                        self.list[self.aaaa].append( 502 )
            
            for self.aaaa, self.bbbb in enumerate( self.list ):
                for self.cccc, self.dddd in enumerate( self.list[ self.aaaa ] ):
                    
                    if (len([
                        self.eeee[ self.cccc ] for self.eeee in self.list if self.eeee[ self.cccc ] == 200
                    ]) <= 1 or not ([
                        self.eeee[ self.cccc ] for self.eeee in self.list
                    ][-1] == 200)) and not self.gate[self.cccc] == None:
                        
                        self.gate[self.cccc] = None
                        
                        print( f'{ timedate.now() } { self.thread } 503 : {self.cccc:02n}', self.load[self.cccc].url, [
                            self.eeee[ self.cccc ] for self.eeee in self.list
                        ] )
                        
                        #   if random.randrange(100) >= 32:
                        #       PYREPLIT(
                        #           repl = '/'.join([
                        #               re.split('/|\.', self.load[self.cccc].url)[3], 
                        #               re.split('/|\.', self.load[self.cccc].url)[2]
                        #           ])
                        #       ).gits()
                        if random.randrange(100) >= 64:
                            PYREPLIT(
                                repl = '/'.join([
                                    re.split('/|\.', self.load[self.cccc].url)[3], 
                                    re.split('/|\.', self.load[self.cccc].url)[2]
                                ])
                            ).kills()
                        if random.randrange(100) >= 48:
                            chk_token(
                                re.split('/|\.', self.load[self.cccc].url)[3], 
                                re.split('/|\.', self.load[self.cccc].url)[2], 
                                __sid__.strip()
                            )
                        
                        PYREPLIT(
                            repl = '/'.join([
                                re.split('/|\.', self.load[self.cccc].url)[3], 
                                re.split('/|\.', self.load[self.cccc].url)[2]
                            ])
                        ).shell()
                        
                        try     : 
                            if not self.root[self.cccc] == '':
                                _thread.start_new_thread(requests.get(self.root[self.cccc]) , ())
                        except  : pass
                        try     : 
                            if not self.root[self.cccc] == '':
                                _thread.start_new_thread(requests.get(f'https://render-tron.appspot.com/screenshot/{ self.root[self.cccc] }'), ())
                        except  : pass

                    elif (len([
                        self.eeee[ self.cccc ] for self.eeee in self.list if self.eeee[ self.cccc ] == 200
                    ]) >= 1 or ([
                        self.eeee[ self.cccc ] for self.eeee in self.list
                    ][-1] == 200)) and not self.gate[self.cccc] == True:
                    
                        self.gate[self.cccc] = True
                        

                        print( f'{ timedate.now() } { self.thread } 200 : {self.cccc:02n}', self.load[self.cccc].url )

                        if random.randrange(100) >= 50:
                            chk_token(
                                re.split('/|\.', self.load[self.cccc].url)[3], 
                                re.split('/|\.', self.load[self.cccc].url)[2], 
                                __sid__.strip()
                            )
                        
                        try     : _thread.start_new_thread(requests.post(self.load[self.cccc].url), ())
                        except  : pass
                        try     : _thread.start_new_thread(requests.get(f'https://render-tron.appspot.com/screenshot/{ self.load[self.cccc].url }'), ())
                        except  : pass
                    
            print('\n'.join([str( f'{ timedate.now() } { self.thread } DONE ' + str(x) ) for x in self.list]))
            time.sleep( random.randrange( 30, 90 ) )
    def ace(
        self
    ):
    
        while True:
        
            self.load = []
            self.resp = []
            self.list = []
            self.gate = []
            
            for self.base in self.data:
                self.addr               = self.base
                self.load.append(grequests.get(
                    f'{ self.addr }', 
                    headers = {
                        'User-Agent'        : random.choice([
                            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 slurp', 
                            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36', 
                            'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.5277.764 Mobile Safari/537.36'
                        ]), 
                        'Accept'            : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 
                        'Accept-Language'   : 'en-US,en;q=0.9'
                    }, 
                    timeout = 20
                ))
                self.gate.append(f'{ self.addr }')
                
            self.resp.append(
                grequests.map(self.load)
            )
            self.resp.append(
                grequests.map(self.load)
            )
            self.resp.append(
                grequests.map(self.load)
            )
                
            for self.aaaa, self.bbbb in enumerate( self.resp ):
                
                self.list.append([])
                
                for self.cccc, self.dddd in enumerate( self.resp[ self.aaaa ] ):
                    try:
                        self.list[self.aaaa].append( self.resp[self.aaaa][self.cccc].status_code )
                    except:
                        self.list[self.aaaa].append( 502 )
            
            for self.aaaa, self.bbbb in enumerate( self.list ):
                for self.cccc, self.dddd in enumerate( self.list[ self.aaaa ] ):
                    
                    if (len([
                        self.eeee[ self.cccc ] for self.eeee in self.list if self.eeee[ self.cccc ] == 200
                    ]) <= 1 or not ([
                        self.eeee[ self.cccc ] for self.eeee in self.list
                    ][-1] == 200)) and not self.gate[self.cccc] == None:
                        
                        self.gate[self.cccc] = None
                        
                        print( f'{ timedate.now() } { self.thread } 503 : {self.cccc:02n}', self.load[self.cccc].url, [
                            self.eeee[ self.cccc ] for self.eeee in self.list
                        ] )

                        for count in range(0, 6):
                            try         :
                                _thread.start_new_thread(requests.get(f'https://render-tron.appspot.com/screenshot/{ self.load[self.cccc].url }'), ())
                            except      :
                                pass
                            time.sleep( random.randrange(8) )

                    elif (len([
                        self.eeee[ self.cccc ] for self.eeee in self.list if self.eeee[ self.cccc ] == 200
                    ]) >= 1 or ([
                        self.eeee[ self.cccc ] for self.eeee in self.list
                    ][-1] == 200)) and not self.gate[self.cccc] == True:
                    
                        self.gate[self.cccc] = True
                        
                        print( f'{ timedate.now() } { self.thread } 200 : {self.cccc:02n}', self.load[self.cccc].url )

                        if random.randrange(100) >= 64:
                            try     :
                                _thread.start_new_thread(requests.get(f'https://render-tron.appspot.com/screenshot/{ self.load[self.cccc].url }'), ())
                            except  :
                                pass
                    
            print('\n'.join([str( f'{ timedate.now() } { self.thread } DONE ' + str(x) ) for x in self.list]))
            time.sleep( random.randrange(120) )


i = []
for x in [
    'mikemaesod/awcloud-token'
]:
    i.append(x)
    if len(i) >= 6:
        WEBCHECK(i).thread()
        i = []

if len(i) >= 1:
    WEBCHECK(i).thread()
    i = []
else:
    i = []


while True:
    #   print('SURF IS RUNNING')
    time.sleep( 8 )
    continue


