import cosmoscripting
from simulator.wrapper import simulate
from utils.block_parser import BlockParser

def execute_ptr(mk, content):
    start_time = validate_ptr(content)
    cosmo = cosmoscripting.Cosmo()
    cosmo.unloadLastCatalog()
    catalog = simulate(mk, content)
    cosmo.loadCatalogFile(catalog)

    cosmo.setTime(start_time + ' UTC')
    cosmo.gotoObject('JUICE', 0)

def validate_ptr(content):
    parser = BlockParser(content)
    parser.process()
    return parser.start_times[0]
