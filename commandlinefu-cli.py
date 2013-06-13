#!/usr/bin/python
#original => https://github.com/q6r/commandlinefu-cli.git
import sys
import getopt
from urllib2 import urlopen, URLError
from urllib import quote
from base64 import b64encode
from json import loads
import re
VERSION = 0.2

def main():
    option = 0
    if(len(sys.argv)<2):
        usage()
        sys.exit(1)
    try:
        opts, args = getopt.getopt(sys.argv[1:]
                                   ,"harvt:u:c:"
                                   ,["help", "all", "command=", "tagged", "random", "using"])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(-1)
    for opt, command in opts:
        #command = quote(command)
        if opt == "-v":
            print "commandlinefu v%g" % VERSION
            sys.exit(0)
        elif opt in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif opt in ("-a", "--all"):
            rjson = request_page("browse")
        elif opt in ("-r", "--random"):
            rjson = request_page("random")
        elif opt in ("-c", "--command"):
            rjson = request_page("matching/%s/%s/sort-by-votes" % (command, b64encode(command)))
        elif opt in ("-u", "--using"):
            rjson = request_page("using/%s/sort-by-votes" % (command))
        elif opt in ("-t", "--tagged"):
            rjson = request_page("tagged/163/%s/sort-by-votes" % command)
    if rjson == "[]":
        print "[%s] not found" % command
        sys.exit(1)
    print_result(rjson, command)
    sys.exit(1)

def print_result(rjson, command):
    data = loads(rjson)
    data.reverse()
    for i in range(0,len(data)):
        votes = data[i]["votes"]
        cmd = data[i]["command"]
        cmd = cmd.replace(command, ansi("cyan")+command+ansi("off"))
        cmd = re.sub(r'([!O>=(<>+@^)$*`#&{}\\\'":/|;,.?-])', ansi("cyan")+r'\1'+ansi("off"),cmd)
        cmd = cmd.replace("|", ansi("cyan")+"|"+ansi("off"))
        print "%s%03s %s%s\n    %s" % ( ansi("magenta")
                                    , votes
                                    , data[i]["summary"]
                                    , ansi("off")
                                    , cmd)

def ansi(name):
    colors = {
        "off"       :0,
        "bold"      :1,
        "italic"    :3,
        "underline" :4,
        "blink"     :5,
        "inverse"   :7,
        "hidden"    :8,
        "black"     :30,
        "red"       :31,
        "green"     :32,
        "yellow"    :33,
        "blue"      :34,
        "magenta"   :35,
        "cyan"      :36,
        "white"     :37,
        "black_bg"  :40,
        "red_bg"    :41,
        "green_bg"  :42,
        "yellow_bg" :43,
        "blue_bg"   :44,
        "magenta_bg":45,
        "cyan_bg"   :46,
        "white_bg"  :47
    }
    return "\033[%dm" % (colors[name])


def request_page(url_part):
    try:
        url = "http://www.commandlinefu.com/commands/" + url_part
        print url
        rjson = urlopen(url+"/json")
        rjson = rjson.read()
        return rjson
    except URLError, err:
        print str(err)
        sys.exit(1)

def usage():
    commands = {
        "-a":"\t\tShow latest commandlinefu submissions",
        "-r":"\t\tShow random commandlinefu command",
        "-c <command>":"\tSearch for specific command",
        "-u <command>":"\tSearch command using ",
        "-t <command>":"\tSearch for tagged commands",
        "-h":"\t\tShow help",
        "-v":"\t\tVersion",
        }
    print "Usage : %s" % sys.argv[0]
    for options in commands:
        print "\t %s%s" % (options, commands[options])

#--------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
