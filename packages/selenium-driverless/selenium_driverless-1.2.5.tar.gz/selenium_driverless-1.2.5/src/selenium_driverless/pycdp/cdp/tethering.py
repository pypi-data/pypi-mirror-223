# DO NOT EDIT THIS FILE!
#
# This file is generated from the CDP specification. If you need to make
# changes, edit the generator and regenerate all of the modules.
#
# CDP domain: Tethering (experimental)

from __future__ import annotations

import typing
from dataclasses import dataclass

from .util import event_class, T_JSON_DICT


def bind(
        port: int
) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]:
    '''
    Request browser port binding.

    :param port: Port number to bind.
    '''
    params: T_JSON_DICT = dict()
    params['port'] = port
    cmd_dict: T_JSON_DICT = {
        'method': 'Tethering.bind',
        'params': params,
    }
    json = yield cmd_dict


def unbind(
        port: int
) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]:
    '''
    Request browser port unbinding.

    :param port: Port number to unbind.
    '''
    params: T_JSON_DICT = dict()
    params['port'] = port
    cmd_dict: T_JSON_DICT = {
        'method': 'Tethering.unbind',
        'params': params,
    }
    json = yield cmd_dict


@event_class('Tethering.accepted')
@dataclass
class Accepted:
    '''
    Informs that port was successfully bound and got a specified connection id.
    '''
    #: Port number that was successfully bound.
    port: int
    #: Connection id to be used.
    connection_id: str

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Accepted:
        return cls(
            port=int(json['port']),
            connection_id=str(json['connectionId'])
        )
