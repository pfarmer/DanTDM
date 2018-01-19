# -*- coding: utf-8 -*-
import logging

log = logging.getLogger(__name__)


def listvms(cs, domainid=None):
    if not domainid:
        result = cs.listVirtualMachines({'listall': 'true'})
    else:
        result = cs.listVirtualMachines({'listall': 'true', 'domainid': domainid})
        log.debug(result.json())
    return result.json()['listvirtualmachinesresponse']['virtualmachine']
