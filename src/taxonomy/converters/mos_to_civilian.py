"""Convert MOS to civilian skills."""
MOS_MAP = {
    '25B': 'network_administrator',
    '18A': 'operations_manager',
}

def convert_mos(mos_code: str) -> str:
    return MOS_MAP.get(mos_code.upper(), 'unknown')
