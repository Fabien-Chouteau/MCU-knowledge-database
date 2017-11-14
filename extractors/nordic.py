vendor_id = 'Nordic'

# Nordic device are actually not extracted for files...
def extract(mcus):

    common_mcu_info = {}
    common_mcu_info['family']   = 'nRF51'
    common_mcu_info['cpu_core'] = 'ARM Cortex-M0'
    common_mcu_info['vendor']   = vendor_id
    common_mcu_info['svd_file'] = 'nrf51.svd'

    variants = [{'id': 'AA', 'ram': '0x4000', 'rom': '0x40000'}, # 16k 256k
                {'id': 'AB', 'ram': '0x4000', 'rom': '0x20000'}, # 16k 128k
                {'id': 'AC', 'ram': '0x8000', 'rom': '0x40000'}] # 32k 256k

    # nRF51822xx
    for var in variants:
        mcu_info = common_mcu_info.copy()
        mcu_info['name'] = 'nRF51822xx' + var['id']

        mcu_info['ram'] = [{'name': 'ram', 'address': '0x20000000', 'size':var['ram']}]
        mcu_info['rom'] = [{'name': 'rom', 'address': '0x0', 'size':var['rom']}]

        mcus.append(mcu_info)

    # nRF51824
    mcu_info = common_mcu_info.copy()
    mcu_info['name'] = 'nRF51824QFAA'

    mcu_info['ram'] = [{'name': 'ram', 'address': '0x20000000', 'size':'0x4000'}] # 16k
    mcu_info['rom'] = [{'name': 'rom', 'address': '0x0', 'size':'0x40000'}] # 256k

    mcus.append(mcu_info)

    # nRF51422
    for var in variants:
        mcu_info = common_mcu_info.copy()
        mcu_info['name'] = 'nRF51422xx' + var['id']

        mcu_info['ram'] = [{'name': 'ram', 'address': '0x20000000', 'size':var['ram']}]
        mcu_info['rom'] = [{'name': 'rom', 'address': '0x0', 'size':var['rom']}]

        mcus.append(mcu_info)
