from genericpath import exists
import json
from os import getcwd
from urllib.request import urlretrieve, Request, urlopen, HTTPError
from urllib.parse import urlencode
from socket import timeout
import http.client
import argparse
import signal

user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
http.client._MAXHEADERS = 50000
boards_found = []

def siginit_handler(sig, frame): exit(1)
signal.signal(signal.SIGINT, siginit_handler)

# Arguments
arg_parser = argparse.ArgumentParser(description='Recursively find a post number over a list of board archivers')
arg_parser.add_argument('post_number', type=int, help='Post number to look for')
arg_parser.add_argument('-t', "--thread", action='store_true', help='Look for only OPs')
arg_parser.add_argument('-T', "--timeout", type=int, help='Specify a custom tiemout. Default: 10')
arg_parser.add_argument('-1a', "--one-archive", action='store_true', help='Stop looking for the same board in different archives, regardless of wether it 404\'d or was found')
arg_parser.add_argument('-f', '--archives-file', help='Specify archives.json file. Default: ./archives.json')
arg_parser.add_argument('-nc', '--no-color', action='store_true', help='Remove coloring')
arg_parser.add_argument('-q', '--quiet', action='store_true', help='Reduce output by only printing result URLs')

args = arg_parser.parse_args()

# Initial variables
post_number = args.post_number

if args.archives_file:
    archives_location = args.archives_file
else:
    archive_location = f"{getcwd()}\\archives.json"

if args.timeout:
    custom_timeout = args.timeout
else:
    custom_timeout = 10

class color:
    CYAN = '\u001b[36m'
    GREEN = '\u001b[32m'
    BOLDGREEN = '\033[1;32m'
    RED = '\u001b[31m'
    BOLDRED = '\033[1;31m'
    RESET = '\u001b[0m'

# Make all colors blank if -nc
if args.no_color:
    for attr in dir(color):
        if not attr.startswith('__'):
            setattr(color, attr, '')

# Download archive.json
if not exists(archive_location):
    if not args.quiet: print(f"archives.json not found, downloading to {archive_location}")
    urlretrieve('https://raw.githubusercontent.com/ccd0/4chan-x/master/src/Archive/archives.json', archive_location)

# Load archive JSON
with open(archive_location) as f:
    archives = json.load(f)

# We recursively look in every board of every archive
for archive in archives:

    for board in archive['boards']:

        if board in boards_found:
            if not args.quiet: print(f"Skipping {color.CYAN}/{board}/{color.RESET} on {archive['name']}")
            continue

        if archive['software'] == 'foolfuuka':
            if not args.quiet: print(f"{color.CYAN}/{board}/{color.RESET} on {archive['name']}...".ljust(50), end = '', flush=True)

            if args.thread:
                url= f"https://{archive['domain']}/{board}/thread/{post_number}"
                req = Request(url, headers = user_agent)
            else:
                url = f"https://{archive['domain']}/{board}/search"
                form = {'text' : str(post_number), 'submit_post': 'Go to post number'}
                post = urlencode(form).encode()
                req = Request(url, data = post, headers = user_agent)

            try:
                page = urlopen(req, timeout=custom_timeout)
            except HTTPError as e:
                if e.code == 404:
                    if not args.quiet: print(color.RED,'404',color.RESET, sep='')
                    if args.one_archive: boards_found.append(board)
                    continue
                elif e.code == 403:
                    if not args.quiet: print(color.RED,'403',color.RESET, sep='')
                    if not args.quiet: print(color.BOLDRED,'Forbidden by server, skipping archiver. Check if you can access ', url, ' on your own browser.',color.RESET, sep='')
                    break
                else:
                    if not args.quiet: print(color.RED,e.code,color.RESET, sep='')
                    if not args.quiet: print(color.BOLDRED,'Unknown error, skipping archiver.',color.RESET, sep='')
                    break
            except timeout:
                if not args.quiet: print(color.RED,'Timed out',color.RESET, sep='')
                continue
            except:
                print(color.RED,'\nError while requesting page',color.RESET, sep='')
                raise
            
            if args.thread:
                if not args.quiet: print(color.GREEN,"FOUND!",color.RESET, sep='')
                print(color.BOLDGREEN,url,color.RESET, sep='')
                boards_found.append(board)
            else:
                response = str(http.client.parse_headers(page))
                first_ocurrence = response.find(f"https://{archive['domain']}/{board}/thread")
                if first_ocurrence != -1:
                    response = response[first_ocurrence:len(response)]
                    url = response[0:response.find('"')]
                    if not args.quiet: print(color.GREEN,"FOUND!",color.RESET, sep='')
                    print(color.BOLDGREEN,url,color.RESET, sep='')
                    boards_found.append(board)

                else:
                    if not args.quiet: print(color.RED,'404',color.RESET, sep='')
                    if args.one_archive: boards_found.append(board)

        #elif archive['software'] == 'fuuka':
            # Fuuka is WIP
