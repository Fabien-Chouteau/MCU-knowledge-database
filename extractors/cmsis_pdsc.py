import json
import fnmatch
import os
import os.path
from xml.dom import minidom

def update_proc_info(proc_info, proc_node):
    core = proc_node.getAttribute('Dcore')
    if core != "":
        proc_info['core'] = core

def parse_device(mcus, node, vendor_id, familyname, proc_info):

    mcu_name  = node.getAttribute('Dname')

    processor = node.getElementsByTagName('processor')
    if len (processor) != 0:
        update_proc_info(proc_info, processor[0])


    if 'core' not in proc_info:
        print "no core for this MCU: " + mcu_name
        core = ""
    else:
        core = proc_info['core']

    if core.startswith('Cortex'):
        core = "ARM " + core

    debug = node.getElementsByTagName('debug')
    if len(debug) > 0:
        svdfile   = os.path.basename(debug[0].getAttribute('svd'))
    else:
        svdfile   = ''

    rom_list = []
    ram_list = []

    for mem in node.getElementsByTagName('memory'):
        id    = mem.getAttribute("id")
        addr  = mem.getAttribute("start")
        size  = mem.getAttribute("size")

        if not id:
            id = mem.getAttribute("name")

        mem_info = {}
        mem_info['name']    = id
        mem_info['address'] = addr
        mem_info['size']    = size

        if 'RAM' in id:
            ram_list += [mem_info]
        elif 'ROM' in id or 'FLASH' in id:
            rom_list += [mem_info]
        # else:
        #     print "memory id: '%s'" % str(mem.toxml())
        #     raise

    mcu_info = {}
    mcu_info['name']     = mcu_name
    mcu_info['family']   = familyname
    mcu_info['cpu_core'] = core
    mcu_info['svd_file'] = svdfile
    mcu_info['ram']      = ram_list
    mcu_info['rom']      = rom_list
    mcu_info['vendor']   = vendor_id

    mcus.append(mcu_info)

def extract(pdsc_dir, mcus):

    # Find all .pdsc files
    matches = []
    for root, dirnames, filenames in os.walk(pdsc_dir):
        for filename in fnmatch.filter(filenames, '*.pdsc'):
            matches.append(os.path.join(root, filename))

    for pdsc_file in matches:
        print "Loading MCU definitions from " + pdsc_file

        try:
            xmldoc     = minidom.parse(pdsc_file)
        except:
            print "invalid XML file: " + pdsc_file
            continue

        vendor_id  = xmldoc.getElementsByTagName('vendor')
        if len(vendor_id) != 0:
            vendor_id = vendor_id[0].firstChild.data
        else:
            vendor_id = 'Unkown_Vendor'

        familylist = xmldoc.getElementsByTagName('family')

        for family in familylist:

            subfamilylist = family.getElementsByTagName('subFamily')

            proc_info = {}

            processor  = family.getElementsByTagName('processor')
            if len(processor) != 0:
                update_proc_info(proc_info, processor[0])

            if len(subfamilylist) == 0:
                familyname = family.getAttribute('Dfamily')

                # Filter some of the stange device declaration from Atmel
                if familyname.startswith("ARM"):
                    continue

                mculist = family.getElementsByTagName('device')
                for mcu_node in mculist:
                    parse_device(mcus, mcu_node, vendor_id, familyname, proc_info)
            else:
                for subfamily in subfamilylist:
                    familyname = subfamily.getAttribute('DsubFamily')

                    processor  = subfamily.getElementsByTagName('processor')
                    if len(processor) != 0:
                        update_proc_info(proc_info, processor[0])

                    mculist = subfamily.getElementsByTagName('device')
                    for mcu_node in mculist:
                        parse_device(mcus, mcu_node, vendor_id, familyname, proc_info)
