import cosmoscripting
from simulator.wrapper import test
from utils.block_parser import BlockParser

def execute_ptr(mk, content):
    start_time = validate_ptr(content)
    cosmo = cosmoscripting.Cosmo()
    cosmo.unloadLastCatalog()
    catalog = test(mk, content)
    cosmo.loadCatalogFile(catalog)

    cosmo.setTime(start_time + ' UTC')
    cosmo.gotoObject('JUICE')

def validate_ptr(content):
    parser = BlockParser(content)
    parser.process()
    return parser.start_times[0]
