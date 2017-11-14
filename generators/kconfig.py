import os
import re

def create_subdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def to_symbol(s):
    s = re.sub(' ','_', s)
    s = re.sub('-','_', s)
    s = re.sub('\+','P', s)
    s = re.sub('[^0-9a-zA-Z_]', '', s)
    return s

def to_mcu_symbol(s):
    return "MCU_Device_" + to_symbol(s)
def to_core_symbol(s):
    return "MCU_Core_" + to_symbol(s)
def to_family_symbol(s):
    return "MCU_Family_" + to_symbol(s)
def to_vendor_symbol(s):
    return "MCU_Vendor_" + to_symbol(s)

def generate_kconfig_mcus(database,
                          filename,
                          svd_dir_template,
                          ld_script_template,
                          header=None,
                          footer=None):

    config = ""
    for mcu in database.list():
        symbol = to_mcu_symbol(mcu['name'])

        if 'svd_file' in mcu and len(mcu['svd_file']) > 0:
            svd_dir = svd_dir_template.format(svd=mcu['svd_file'][:-4],
                                              name=mcu['name'],
                                              vendor=mcu['vendor'],
                                              family=mcu['family'])
        else:
            svd_dir = None

        config += "config %s\n" % symbol
        config += "      bool\n"
        config += "      select %s\n" % to_family_symbol(mcu['family'])
        config += "      select %s\n" % to_core_symbol(mcu['cpu_core'])

        if svd_dir:
            config += "      option source_dir=\"%s\"\n" % svd_dir

        config += "\n"
        config += "if %s\n" % symbol
        config += "   config MCU_Device_Name\n"
        config += "         string\n"
        config += "         default \"%s\"\n" % mcu['name']
        if svd_dir:
            config += "   config MCU_SVD_Path\n"
            config += "         string\n"
            config += "         default \"%s\"\n" % svd_dir
            config += "   config MCU_SVD_%s\n" % to_symbol(mcu['svd_file'][:-4])
            config += "         bool\n"
            config += "         default y\n"
        config += "   config MCU_LD_Script_Path\n"
        config += "         string\n"
        config += "         default \"%s\"\n" % ld_script_template.format (name=mcu['name'],
                                                                           vendor=mcu['vendor'],
                                                                           family=mcu['family'])
        config += "endif\n"

    with open(filename, 'w') as file:
        if header:
            file.write(header)
        file.write(config)
        if footer:
            file.write(footer)

def generate_kconfig_mcus_choice(database,
                                 filename,
                                 header=None,
                                 footer=None):

    config = ""

    # Vendor choice
    config += "choice CHOICE_MCU_VENDOR\n"
    config += "       prompt \"Select micro-controller vendor\"\n"
    for vendor in database.vendors():
        config +="   config CHOICE_%s\n" % to_vendor_symbol(vendor)
        config +="          bool \"%s\"\n" % vendor
    config += "endchoice\n"

    for vendor in database.vendors():

        # Family choice per vendor
        config += "if CHOICE_%s\n" % to_vendor_symbol(vendor)
        config += "choice CHOICE_MCU_%s_FAMILY\n" % to_symbol(vendor)
        config += "       prompt \"Select micro-controller family\"\n"
        for fam in database.families(vendor):
            config +="   config CHOICE_%s\n" % to_family_symbol(fam)
            config +="          bool \"%s\"\n" % fam
        config += "endchoice\n"
        config += "endif\n"

        for fam in database.families(vendor):

            config += "if CHOICE_%s\n" % to_family_symbol(fam)
            config += "choice CHOICE_MCU_DEVICE_%s\n" % to_family_symbol(fam)
            config += "       prompt \"Select micro-controller device\"\n"
            for mcu in database.list():
                if mcu['family'] == fam:
                    config +="   config CHOICE_%s\n" % to_mcu_symbol(mcu['name'])
                    config +="          bool \"%s\"\n" % mcu['name']
                    config +="          select %s\n" % to_mcu_symbol(mcu['name'])

            config += "endchoice\n"
            config += "endif\n"

    with open(filename, 'w') as file:
        if header:
            file.write(header)
        file.write(config)
        if footer:
            file.write(footer)

def generate_kconfig_families(database,
                              filename,
                              header=None,
                              footer=None):

    config = ""
    for family in database.families():
        symbol = to_family_symbol(family)

        config += "config %s\n" % symbol
        config += "      bool\n"
        config += "\n"
        config += "if %s\n" % symbol
        config += "   config MCU_Family_Name\n"
        config += "         string\n"
        config += "         default \"%s\"\n" % family
        config += "endif\n"

    with open(filename, 'w') as file:
        if header:
            file.write(header)
        file.write(config)
        if footer:
            file.write(footer)

def generate_kconfig_cores(database,
                           filename,
                           header=None,
                           footer=None):

    config = ""
    for core in database.cores():
        symbol = to_core_symbol(core)

        config += "config %s\n" % symbol
        config += "      bool\n"
        config += "\n"
        config += "if %s\n" % symbol
        config += "   config MCU_Core_Name\n"
        config += "         string\n"
        config += "         default \"%s\"\n" % core
        config += "endif\n"

    with open(filename, 'w') as file:
        if header:
            file.write(header)
        file.write(config)
        if footer:
            file.write(footer)
