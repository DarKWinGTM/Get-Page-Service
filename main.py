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

                    time.sleep(10)

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
                        if random.randrange(100) >= 64:
                            PYREPLIT(
                                repl = '/'.join([
                                    re.split('/|\.', self.load[self.cccc].url)[3], 
                                    re.split('/|\.', self.load[self.cccc].url)[2]
                                ])
                            ).kills()
                        if random.randrange(100) >= 16:
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
            time.sleep( random.randrange( 10, 60 ) )

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
                        
                        if random.randrange(100) >= 64:
                            PYREPLIT(
                                repl = '/'.join([
                                    re.split('/|\.', self.load[self.cccc].url)[3], 
                                    re.split('/|\.', self.load[self.cccc].url)[2]
                                ])
                            ).kills()
                        if random.randrange(100) >= 16:
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
            time.sleep( random.randrange( 10, 60 ) )

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
    #   'PatiwatNumbut/Get-Page-Run-Token'
    #   'PatiwatNumbut/Get-Page-Run-Cpanel-0000'
    #   'PatiwatNumbut/Get-Page-Run-Cpanel-0001'
    #   'PatiwatNumbut/Get-Page',
    #   NodeNetwork tonmaster.1.08@gmail.com
    'NodeNetwork/aw-packedtrx-express-00001',
    'NodeNetwork/aw-packedtrx-express-00002',
    'NodeNetwork/aw-packedtrx-express-00003',
    'NodeNetwork/aw-packedtrx-express-00004',
    'NodeNetwork/aw-packedtrx-express-00005',
    'NodeNetwork/aw-packedtrx-express-10001',
    'NodeNetwork/aw-packedtrx-express-10002',
    'NodeNetwork/aw-packedtrx-express-10003',
    'NodeNetwork/aw-packedtrx-express-10004',
    'NodeNetwork/aw-packedtrx-express-10005',
    'NodeNetwork/aw-packedtrx-express-20001',
    'NodeNetwork/aw-packedtrx-express-20002',
    'NodeNetwork/aw-packedtrx-express-20003',
    'NodeNetwork/aw-packedtrx-express-20004',
    'NodeNetwork/aw-packedtrx-express-20005',
    
    #   NodeNetwork003 tonmaster.1.08+003@gmail.com
    'NodeNetwork003/aw-packedtrx-express-00001',
    'NodeNetwork003/aw-packedtrx-express-00002',
    'NodeNetwork003/aw-packedtrx-express-00003',
    'NodeNetwork003/aw-packedtrx-express-00004',
    'NodeNetwork003/aw-packedtrx-express-00005',
    'NodeNetwork003/aw-packedtrx-express-10001',
    'NodeNetwork003/aw-packedtrx-express-10002',
    'NodeNetwork003/aw-packedtrx-express-10003',
    'NodeNetwork003/aw-packedtrx-express-10004',
    'NodeNetwork003/aw-packedtrx-express-10005',
    'NodeNetwork003/aw-packedtrx-express-20001',
    'NodeNetwork003/aw-packedtrx-express-20002',
    'NodeNetwork003/aw-packedtrx-express-20003',
    'NodeNetwork003/aw-packedtrx-express-20004',
    'NodeNetwork003/aw-packedtrx-express-20005',

    #   NodeNetwork tonmaster.1.08@gmail.com
    'NodeNetwork/aw-express-20001',
    'NodeNetwork/aw-express-20002',
    'NodeNetwork/aw-express-20003',
    'NodeNetwork/aw-express-20004',
    'NodeNetwork/aw-express-20005',
    'NodeNetwork/aw-express-20001',
    'NodeNetwork/aw-express-20002',
    'NodeNetwork/aw-express-20003',
    'NodeNetwork/aw-express-20004',
    'NodeNetwork/aw-express-20005',
    'NodeNetwork/aw-express-20006',
    'NodeNetwork/aw-express-20007',
    'NodeNetwork/aw-express-20008',
    'NodeNetwork/aw-express-20009',
    'NodeNetwork/aw-express-20010',

    #   NodeNetwork001 tonmaster.1.08+001@gmail.com
    'NodeNetwork001/aw-express-20001',
    'NodeNetwork001/aw-express-20002',
    'NodeNetwork001/aw-express-20003',
    'NodeNetwork001/aw-express-20004',
    'NodeNetwork001/aw-express-20005',
    'NodeNetwork001/aw-express-20001',
    'NodeNetwork001/aw-express-20002',
    'NodeNetwork001/aw-express-20003',
    'NodeNetwork001/aw-express-20004',
    'NodeNetwork001/aw-express-20005',
    'NodeNetwork001/aw-express-20006',
    'NodeNetwork001/aw-express-20007',
    'NodeNetwork001/aw-express-20008',
    'NodeNetwork001/aw-express-20009',
    'NodeNetwork001/aw-express-20010',

    #   NodeNetwork002 tonmaster.1.08+002@gmail.com
    'NodeNetwork002/aw-express-20001',
    'NodeNetwork002/aw-express-20002',
    'NodeNetwork002/aw-express-20003',
    'NodeNetwork002/aw-express-20004',
    'NodeNetwork002/aw-express-20005',
    'NodeNetwork002/aw-express-20001',
    'NodeNetwork002/aw-express-20002',
    'NodeNetwork002/aw-express-20003',
    'NodeNetwork002/aw-express-20004',
    'NodeNetwork002/aw-express-20005',
    'NodeNetwork002/aw-express-20006',
    'NodeNetwork002/aw-express-20007',
    'NodeNetwork002/aw-express-20008',
    'NodeNetwork002/aw-express-20009',
    'NodeNetwork002/aw-express-20010',

    #   NodeNetwork003 tonmaster.1.08+003@gmail.com
    'NodeNetwork003/aw-express-20001',
    'NodeNetwork003/aw-express-20002',
    'NodeNetwork003/aw-express-20003',
    'NodeNetwork003/aw-express-20004',
    'NodeNetwork003/aw-express-20005',
    'NodeNetwork003/aw-express-20001',
    'NodeNetwork003/aw-express-20002',
    'NodeNetwork003/aw-express-20003',
    'NodeNetwork003/aw-express-20004',
    'NodeNetwork003/aw-express-20005',
    'NodeNetwork003/aw-express-20006',
    'NodeNetwork003/aw-express-20007',
    'NodeNetwork003/aw-express-20008',
    'NodeNetwork003/aw-express-20009',
    'NodeNetwork003/aw-express-20010'
]:
    i.append(x)
    if len(i) >= 10:
        WEBCHECK(i, mode = 'chk').thread()
        i = []

if len(i) >= 1:
    WEBCHECK(i, mode = 'chk').thread()
    i = []
else:
    i = []
i = []
for x in [
    # DarKWinGTM
    'https://t6u0k.sse.codesandbox.io', 
    'https://hxl0o.sse.codesandbox.io', 
    'https://jebfs.sse.codesandbox.io', 
    'https://vgqm5.sse.codesandbox.io', 
    'https://sncvu.sse.codesandbox.io', 
    'https://8r4pc.sse.codesandbox.io', 
    'https://mk2v0.sse.codesandbox.io', 
    'https://bjxwk.sse.codesandbox.io', 
    'https://ity0i.sse.codesandbox.io', 
    'https://h8mte.sse.codesandbox.io',
    
    # NodeNetwork10800001
    'https://og69k.sse.codesandbox.io', 
    'https://4vpre.sse.codesandbox.io', 
    'https://3vo69.sse.codesandbox.io', 
    'https://yir26.sse.codesandbox.io', 
    'https://p6mzp.sse.codesandbox.io', 
    'https://iqpkf.sse.codesandbox.io', 
    'https://iol00.sse.codesandbox.io', 
    'https://hl4e4.sse.codesandbox.io', 
    'https://8cqcc.sse.codesandbox.io', 
    'https://d7v51.sse.codesandbox.io',

    # NodeNetwork10800002
    'https://bd7ec.sse.codesandbox.io',
    'https://woh4o.sse.codesandbox.io',
    'https://6nif3.sse.codesandbox.io',
    'https://qqh90.sse.codesandbox.io',
    'https://fnox1.sse.codesandbox.io',
    'https://hc5f0.sse.codesandbox.io',
    'https://26do4.sse.codesandbox.io',
    'https://7ffsv.sse.codesandbox.io',
    'https://higoc.sse.codesandbox.io',
    'https://7c8ep.sse.codesandbox.io',

    # NodeNetwork10800003
    'https://l3fdw.sse.codesandbox.io',
    'https://fnsxo.sse.codesandbox.io',
    'https://8dqhu.sse.codesandbox.io',
    'https://lnop5.sse.codesandbox.io',
    'https://4zc9j.sse.codesandbox.io',
    'https://thxqn.sse.codesandbox.io',
    'https://2qnif.sse.codesandbox.io',
    'https://vjj79.sse.codesandbox.io',
    'https://11vhu.sse.codesandbox.io',
    'https://kr8gs.sse.codesandbox.io'
]:
    i.append(x)
    if len(i) >= 10:
        time.sleep(random.uniform(0.11, 0.64))
        WEBCHECK(i, mode = 'ace').thread()
        i = []

if len(i) >= 1:
    WEBCHECK(i, mode = 'ace').thread()
    i = []
else:
    i = []


i = []
for x in [
    #   'patiwatnumbut/awcloud-token',
    'FFPREMIUM/awcloud-token',
    #-   'artwisut/awcloud-token', 
    #-   'sakchaipingsran/awcloud-token', 
    #-   'lifferty/awcloud-token', 
    'praniti99/awcloud-token', 
    #-   'fourz/awcloud-token', 
    #-   'jo1232/awcloud-token', 
    #-   'boomswxx945/awcloud-token', 
    'kuk1990/awcloud-token', 
    'fluffy1004/awcloud-token', 
    'mikemaesod/awcloud-token', 
    #-   'tee51551/awcloud-token', 
    'thanachai12/awcloud-token', 
    #-   'supernop/awcloud-token', 
    #-   'aorsai5/awcloud-token', 
    #-   'najabangaras/awcloud-token', 
    #-   'bowonratkitisak/awcloud-token', 
    #-   'akepordee/awcloud-token', 
    #-   'songeiei1/awcloud-token', 
    'nunkh0ng/awcloud-token', 
    #-   'golfgappz/awcloud-token', 
    #-   'la12va/awcloud-token', 
    #-   'khowglong2/awcloud-token', 
    #-   'awjate/awcloud-token', 
    #-   'starshiprs/awcloud-token', 
    #-   'man88/awcloud-token', 
    #-   'dhongerus/awcloud-token', 
    #-   'awduchbot1/awcloud-token', 
    'aongseal/awcloud-token', 
    #-   'catsince/awcloud-token', 
    #-   'e25icl/awcloud-token', 
    #-   'tongatipbk/awcloud-token', 
    'micvbn/awcloud-token', 
    #-   'domminic11/awcloud-token', 
    #-   'onibrku10/awcloud-token', 
    #-   'aphichai123/awcloud-token', 
    'aengkung1234/awcloud-token', 
    #-   'ae9041a/awcloud-token', 
    #-   'mustaza300/awcloud-token', 
    'yaizaq/awcloud-token', 
    #-   'pppeach/awcloud-token', 
    #-   'thanaphol2123/awcloud-token', 
    'soongusto/awcloud-token', 
    'appleblue1/awcloud-token', 
    'teeraporn12519/awcloud-token', 
    'jakkarinninpan/awcloud-token', 
    #-  'kolokden01/awcloud-token', 
    'pattarasakphuan/awcloud-token', 
    #-   'idspoon/awcloud-token', 
    #-   'maxnoizas/awcloud-token', 
    'biskittlm/awcloud-token', 
    'joetk074/awcloud-token', 
    #-   'wealthme01/awcloud-token', 
    #-   'bb4747/awcloud-token', 
    'pond37611/awcloud-token', 
    'trananhquan/awcloud-token', 
    #-   'pongtanaanon789/awcloud-token', 
    #-   'mostok002/awcloud-token', 
    'TranAnhQuan0001/awcloud-token', 
    'TranAnhQuan0002/awcloud-token', 
    'TranAnhQuan0003/awcloud-token', 
    'sg3000/awcloud-token', 
    #-   'alienbot15/awcloud-token', 
    #-   'bas120741/awcloud-token', 
    #-   'replitbotaw01/awcloud-token', 
    #-  'replitbotaw02', 
    #-  'replitbotaw03', 
    #-  'rovesea/awcloud-token', 
    'phillipbansilis/awcloud-token', 
    'PhillipBan00001/awcloud-token', 
    #-  'itinba/awcloud-token', 
    #-  'onemanstory/awcloud-token', 
    #-  'apolloart16/awcloud-token', 
    'areeyagamefi/awcloud-token', 
    'ninjauk13/awcloud-token', 
    #-  'sodomkk/awcloud-token', 
    #-  'fireworkiz/awcloud-token', 
    #-  'warapon1/awcloud-token', 
    #-  'ohhwirat/awcloud-token', 
    #-  'oliengshop757/awcloud-token', 
    'maxmagod/awcloud-token', 
    #-  'maii15/awcloud-token', 
    #-  'noom1/awcloud-token', 
    #-  'pixx2020/awcloud-token', 
    #-  'mafiazarr/awcloud-token', 
    'raicyberteam/awcloud-token', 
    'oak2323/awcloud-token', 
    'poomminerz/awcloud-token', 
    #-  'Bankenstein/awcloud-token', 
    'areeyagamefi2/awcloud-token', 
    #-  'freddy007/awcloud-token', 
    #-  'alderman08/awcloud-token',  
    #-  'awdvii3636/awcloud-token',  
    #-  'poopui1234/awcloud-token',  
    #-  'awboat5656/awcloud-token',  
    #-  'awboat6565/awcloud-token',  
    #-  'awbpn5454/awcloud-token',  
    #-  'awbpn4545/awcloud-token',  
    #-  'awall6363/awcloud-token',  
    'saksitbot/awcloud-token',  
    #-  'spints34/awcloud-token',  
    #-  'thekidkudo/awcloud-token',  
    'sometimex21/awcloud-token',  
    #-  'zekisz1150/awcloud-token',  
    #-  'janghyuk789563/awcloud-token',  
    'Alentine/awcloud-token',  
    #-  'MOGTH001/awcloud-token',  
    #-  'waritza/awcloud-token',  
    'nanthakawut191/awcloud-token',  
    #-  'werayutphonyut/awcloud-token',  
    #-  'rachan7428/awcloud-token',  
    'sophonnjk/awcloud-token', 
    #-  'Mazajan2011/awcloud-token',  
    'jakkapongw/awcloud-token',  
    #   'sinlapa/awcloud-token',  
    'zenith009/awcloud-token',   
    'rainbowz7/awcloud-token', 
    #-  'c1193/awcloud-token', 
    #-  'sinkidlukyim5/awcloud-token', 
    'alosimbay/awcloud-token', 
    'ArmTheeranai/awcloud-token', 
    'maxim522th/awcloud-token', 
    'imoyoyo/awcloud-token', 
    'djnusr001/awcloud-token', 
    'aum833/awcloud-token', 
    'codeduck7210/awcloud-token', 
    'sodamint1z/awcloud-token', 
    'maxwalker123/awcloud-token', 
    'maxwalker543/awcloud-token', 
    'khunote/awcloud-token', 
    'thunderbow/awcloud-token', 
    'affranchise/awcloud-token', 
    'ChristopherRico/awcloud-token', 
    'ChanonAcm/awcloud-token', 
    'joealien/awcloud-token', 
    #-   'deedie/awcloud-token', 
    'JeingBTC/awcloud-token', 
    #-  'punthanin/awcloud-token', 
    #-  'newawtothemoon1/awcloud-token', 
    'AWCNT/awcloud-token', 
    'PunPathaninKaew/awcloud-token', 
    'naptec/awcloud-token', 
    'SucasemKlinmak2276/awcloud-token', 
    'tar555/awcloud-token', 
    'incenaja/awcloud-token', 
    #-  'uselesswd/awcloud-token', 
    'Aa034261643/awcloud-token', 
    #-  'tonslum/awcloud-token', 
    'MBZin/awcloud-token', 
    'detection/awcloud-token', 
    'jjj1928/awcloud-token', 
    'samasak/awcloud-token', 
    'newnowican/awcloud-token', 
    'bluelions/awcloud-token', 
    #-  'yuttanatanuki/awcloud-token', 
    'henry009/awcloud-token', 
    'aa2698/awcloud-token', 
    'kitti1417/awcloud-token', 
    'basekrab/awcloud-token', 
    #-  'rambutan1985/awcloud-token', 
    'testmonitor/awcloud-token', 
    'Dear12345/awcloud-token', 
    'dear123456/awcloud-token', 
    'artnothing123/awcloud-token', 
    'nonbelleskgame3/awcloud-token', 
    'boomvespa/awcloud-token', 
    'nkpt23/awcloud-token', 
    'toomw81/awcloud-token', 
    'TreeCoin/awcloud-token', 
    'lulita999/awcloud-token', 
    'CatTH007/awcloud-token', 
    'aunkung1234/awcloud-token', 
    'ittiphatkaewsod/awcloud-token', 
    'iRyoma/awcloud-token', 
    'rockbell123/awcloud-token', 
    'sunza1234/awcloud-token', 
    'robinjheart/awcloud-token', 
    'zeuss001/awcloud-token', 
    'MadzCat468/awcloud-token', 
    'TranAnhQuan0004/awcloud-token', 
    #-  'iplayse7en/awcloud-token', 
    'porpy286/awcloud-token', 
    'punpun1703/awcloud-token',
    'arkacrypto12/awcloud-token',
    'tanuki01/awcloud-token', 
    'tanuki02/awcloud-token', 
    'got20031996/awcloud-token', 
    'CHiNJUNG96/awcloud-token', 
    'Chaysenberg/awcloud-token', 
    'tawlextodtor/awcloud-token', 
    'affranchise2/awcloud-token', 
    'Benzafk14/awcloud-token', 
    'Max150245/awcloud-token', 
    'bluelions/awcloud-token', 
    #-  'aor19/awcloud-token', 
    'vorvae/awcloud-token', 
    'jkawbot/awcloud-token', 
    'yibzy/awcloud-token', 
    'MunkGorn/awcloud-token', 
    'icappuccino/awcloud-token', 
    'Palomaza/awcloud-token', 
    'taohucreate/awcloud-token', 
    'tumtheeraphat/awcloud-token', 
    'wachirawitz/awcloud-token', 
    'ttamama/awcloud-token', 
    'alienmineice321/awcloud-token', 
    'JSstarter1/awcloud-token', 
    'arunluch27/awcloud-token', 
    'Huapok/awcloud-token', 
    'knalak11/awcloud-token', 
    'soushi01/awcloud-token', 
    'subalu/awcloud-token', 
    'waxdnzr/awcloud-token', 
    'frongseraw/awcloud-token', 
    'home189/awcloud-token', 
    'home8956/awcloud-token', 
    'JUNKBQY/awcloud-token', 
    'darun00/awcloud-token', 
    'jeffyandcake/awcloud-token'
]:
    i.append(x)
    if len(i) >= 10:
        time.sleep(random.uniform(0.11, 0.64))
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


