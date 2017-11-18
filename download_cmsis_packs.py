import wget
import os
import re
from subprocess import call
from xml.dom import minidom

def create_subdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

# Get pack list from the website by parsing the HTML page

outdir='cmsis_packs'

create_subdir(outdir)

index=os.path.join(outdir, 'index.html')

index=wget.download('http://sadevicepacksprodus.blob.core.windows.net/idxfile/index.idx', out=index)

regex = r'.*pdsc url="(.*)" name"(.*) version="([0-9.]*)/*'

with open(index, 'r') as file:
    for line in file:
        if line.startswith('<pdsc'):
            xmldoc  = minidom.parseString('<blah>' + line + '</blah>')
            pdsc = xmldoc.getElementsByTagName('pdsc')[0]
            name = pdsc.getAttribute("name")
            url = pdsc.getAttribute("url")
            version = pdsc.getAttribute("version")
            print "pack '%s' version %s @ %s" % (name, version, url)
            if ('DFP' in name or 'DeviceFamilyPack' in name) and not name.startswith('Keil'):

                name = name[:-5]
                full_url = url + name + '.' + version + '.pack'
                outfile = os.path.join(outdir, name)

                if not os.path.exists(outfile):
                    print "Downloading '%s'" % full_url
                    outfile = wget.download(full_url, out=outfile)
                else:
                    print "pack already downloaded"

                print "\nUnzip " + outfile
                unzip_dir = os.path.join(outdir, 'packs', name)
                create_subdir(unzip_dir)
                # Atmel packs are actualy zip files
                call(['unzip', '-d', unzip_dir, outfile])
