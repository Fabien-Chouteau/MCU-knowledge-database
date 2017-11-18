import json
from extractors import stm32, cmsis_pdsc

from optparse import OptionParser
import os.path

parser = OptionParser()
parser.add_option("", "--stm32_targets_xml", dest="stm32_targets_xml",
                  help="STM32 target description xml file")

parser.add_option("", "--atmel_packs_dir", dest="atmel_packs_dir",
                  help="Directory containing ATMEL packs (with .pdsc files)")

parser.add_option("", "--cmsis_pdsc_dir", dest="cmsis_pdsc_dir",
                  help="Directory containing CMSIS .pdsc files")

parser.add_option("-o", "--output_file", dest="out_file",
                  help="Path of the json output file")

(options, args) = parser.parse_args()

mcus = []

if options.stm32_targets_xml:
    # Get STMicro MCU info
    stm32.extract(options.stm32_targets_xml, mcus)
else:
    print "Warning: STM32 target file not specified"

if options.atmel_packs_dir:
    # Get Atmel MCU info
    cmsis_pdsc.extract(options.atmel_packs_dir, mcus)
else:
    print "Warning: ATMEL packs directory not specified"

if options.cmsis_pdsc_dir:
    cmsis_pdsc.extract(options.cmsis_pdsc_dir, mcus)
else:
    print "Warning: CMSIS pdsc directory not specified"

print "Number of MCUs: %d" % len(mcus)

mcus.sort()

if options.out_file:
    with open(options.out_file, 'w') as out:
        out.write(json.dumps(mcus, indent=1))
else:
    print json.dumps(mcus, indent=1)
