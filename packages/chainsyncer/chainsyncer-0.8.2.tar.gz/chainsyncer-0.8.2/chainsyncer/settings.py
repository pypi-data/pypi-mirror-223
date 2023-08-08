# standard imports
import logging

# external imports
from hexathon import (
        to_int as hex_to_int,
        strip_0x,
        )
from chainlib.settings import ChainSettings

logg = logging.getLogger(__name__)


def process_sync_range(settings, config):
    o = settings.get('SYNCER_INTERFACE').block_latest()
    r = settings.get('CONN').do(o)
    block_offset = int(strip_0x(r), 16) + 1
    logg.info('network block height at startup is {}'.format(block_offset))

    keep_alive = False
    session_block_offset = 0
    block_limit = 0
    until = 0

    if config.true('_HEAD'):
        settings.set('SYNCER_OFFSET', block_offset)
        settings.set('SYNCER_LIMIT', -1)
        return settings

    session_block_offset = int(config.get('SYNCER_OFFSET'))
    until = int(config.get('SYNCER_LIMIT'))

    if until > 0:
        if until <= session_block_offset:
            raise ValueError('sync termination block number must be later than offset ({} >= {})'.format(session_block_offset, until))
        block_limit = until
    elif until == -1:
        keep_alive = True

    if session_block_offset == -1:
        session_block_offset = block_offset
    elif config.true('_KEEP_ALIVE'):
        block_limit = -1
    else:
        if block_limit == 0:
            block_limit = block_offset

    settings.set('SYNCER_OFFSET', session_block_offset)
    settings.set('SYNCER_LIMIT', block_limit)
    return settings
