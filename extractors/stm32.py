import json
import os.path
from xml.dom import minidom

vendor_id = 'STMicro'

def extract(targets_file, mcus):

    print "Loading MCU definitions from " + targets_file
    xmldoc  = minidom.parse(targets_file)
    mculist = xmldoc.getElementsByTagName('mcu')

    for mcu in mculist:

        mcu_name = mcu.getElementsByTagName('name')[0].firstChild.data
        family   = mcu.getElementsByTagName('familyId')[0].firstChild.data.upper()
        core     = mcu.getElementsByTagName('core')[0].firstChild.data
        svd      = mcu.getElementsByTagName('svd')[0]
        svdfile  = svd.getElementsByTagName('name')[0].firstChild.data
        package  = mcu.getElementsByTagName('package')[0].firstChild.data

        rom_list = []
        ram_list = []

        for mem in mcu.getElementsByTagName('memory'):
            typ  = mem.getAttribute("type")
            addr = mem.getElementsByTagName('address')[0].firstChild.data
            size = mem.getElementsByTagName('size')[0].firstChild.data

            mem_info = {}
            mem_info['name']    = typ
            mem_info['address'] = addr
            mem_info['size']    = size

            if typ == 'RAM':
                ram_list += [mem_info]
            elif typ == 'ROM':
                rom_list += [mem_info]
            else:
                raise

        mcu_info = {}
        mcu_info['name']     = mcu_name
        mcu_info['family']   = family
        mcu_info['cpu_core'] = core
        mcu_info['svd_file'] = svdfile
        mcu_info['ram']      = ram_list
        mcu_info['rom']      = rom_list
        mcu_info['vendor']   = vendor_id

        mcus.append(mcu_info)
