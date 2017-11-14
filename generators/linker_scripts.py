import os

def create_subdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def memory_line(name, perms, address, size):
    return "  %s (%s) : ORIGIN = %s, LENGTH = %s\n" % (name, perms, address, size)

def ld_memory_desc(mcu, unified_names=False):

    out  = "\n"
    out += "MEMORY\n"
    out += "{\n"

    rom_cnt = 1
    for mem in mcu['rom']:
        if unified_names:
            name = 'rom%d' % rom_cnt
            rom_cnt += 1
        else:
            name = mem['name']

        out += memory_line(name, "rx", mem['address'], mem['size'])

    ram_cnt = 1
    for mem in mcu['ram']:
        if unified_names:
            name = 'ram%d' % ram_cnt
            ram_cnt += 1
        else:
            name = mem['name']

        out += memory_line(name, "rwx", mem['address'], mem['size'])

    out += "}\n"

    return out

def generate_linker_scripts(database,
                            filename_template,
                            header=None,
                            footer=None,
                            unified_names=False):

    for mcu in database.list():
        outfile = filename_template.format(name=mcu['name'],
                                           vendor=mcu['vendor'],
                                           family=mcu['family'])

        create_subdir(os.path.dirname (outfile))

        with open(outfile, 'w') as file:
            if header is not None:
                file.write(header)
            file.write(ld_memory_desc(mcu, unified_names))
            if footer is not None:
                file.write(footer)
            file.write("\n")
