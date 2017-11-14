import wget
import os
import re
from subprocess import call

def create_subdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

# Get pack list from the website by parsing the HTML page

outdir='atmel_packs'

create_subdir(outdir)

webpage=os.path.join(outdir, 'file.html')

wget.download('http://packs.download.atmel.com/', out=webpage)

regex = r'data-link="(.*)([\d]+\.[\d]+\.[\d]+)(\.atpack)"'

def ver_tuple(z):
    return tuple([int(x) for x in z.split('.') if x.isdigit()])

packs = {}
with open(webpage, 'r') as file:
    for line in file:
        match = re.search(regex, line)
        if match is not None:
            name    = match.group(1)
            version = match.group(2)
            if name in packs:
                old_version = packs[name]
                if cmp(ver_tuple(version), ver_tuple(old_version)) > 0:
                    # Only keep the highest version of the pack
                    packs[name] = version
            else:
                packs.update({name: version})


# Download and unzip packs

total_packs = len(packs)
current_pack = 1

for pack in packs:
    filename = pack + packs[pack] + ".atpack"
    outfile = os.path.join(outdir, filename)

    print "\n\nPack %s (%d of %d)\n" % (filename, current_pack, total_packs)
    current_pack += 1

    if not os.path.exists(outfile):
        outfile = wget.download('http://packs.download.atmel.com/' + filename,
                                out=outfile)
    else:
        print "pack already downloaded"

    print "\nUnzip " + outfile
    unzip_dir = os.path.join(outdir, 'pack', pack)
    create_subdir(unzip_dir)
    # Atmel packs are actualy zip files
    call(['unzip', '-d', unzip_dir, outfile])
