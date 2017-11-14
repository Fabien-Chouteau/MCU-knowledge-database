import json
import fnmatch
import os
import os.path
from xml.dom import minidom

vendor_id = 'Atmel'

def extract(packs_dir, mcus):

    # Find all .pdsc files
    matches = []
    for root, dirnames, filenames in os.walk(packs_dir):
        for filename in fnmatch.filter(filenames, '*.pdsc'):
            matches.append(os.path.join(root, filename))

    for pdsc_file in matches:
        print "Loading MCU definitions from " + pdsc_file
        xmldoc     = minidom.parse(pdsc_file)
        familylist = xmldoc.getElementsByTagName('family')

        for family in familylist:
            familyname = family.getAttribute('Dfamily')

            # Filter some of the stange device declaration from Atmel
            if familyname.startswith("ARM"):
                continue

            mculist = xmldoc.getElementsByTagName('device')

            for mcu in mculist:
                mcu_name  = mcu.getAttribute('Dname')

                processor = mcu.getElementsByTagName('processor')[0]
                core      = processor.getAttribute('Dcore')

                if core.startswith('Cortex'):
                    core = "ARM " + core

                debug     = mcu.getElementsByTagName('debug')
                if len(debug) > 0:
                    svdfile   = os.path.basename(debug[0].getAttribute('svd'))
                else:
                    svdfile   = ''

                rom_list = []
                ram_list = []

                for mem in mcu.getElementsByTagName('memory'):
                    id    = mem.getAttribute("id")
                    addr  = mem.getAttribute("start")
                    size  = mem.getAttribute("size")

                    mem_info = {}
                    mem_info['name']    = id
                    mem_info['address'] = addr
                    mem_info['size']    = size

                    if 'RAM' in id:
                        ram_list += [mem_info]
                    elif 'ROM' in id:
                        rom_list += [mem_info]
                    else:
                        raise

                mcu_info = {}
                mcu_info['name']     = mcu_name
                mcu_info['family']   = familyname
                mcu_info['cpu_core'] = core
                mcu_info['svd_file'] = svdfile
                mcu_info['ram']      = ram_list
                mcu_info['rom']      = rom_list
                mcu_info['vendor']   = vendor_id

                mcus.append(mcu_info)
