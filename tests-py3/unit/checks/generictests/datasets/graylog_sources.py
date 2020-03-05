#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# yapf: disable
# type: ignore

checkname = 'graylog_sources'

info = [
    [
        u'{"sources": {"my_source_1": 81216, "my_source_2": 10342}, "range": 0, "total": 1, "took_ms": 3}'
    ]
]

discovery = {'': [(u'my_source_1', {}), (u'my_source_2', {})]}

checks = {
    '': [
        (
            u'my_source_1', {}, [
                (
                    0, 'Total number of messages: 81216', [
                        ('messages', 81216, None, None, None, None)
                    ]
                ),
                (
                    0, 'Average number of messages (30 m): 0.00', [
                        ('msgs_avg', 0, None, None, None, None)
                    ]
                )
            ]
        ),
        (
            u'my_source_2', {}, [
                (
                    0, 'Total number of messages: 10342', [
                        ('messages', 10342, None, None, None, None)
                    ]
                ),
                (
                    0, 'Average number of messages (30 m): 0.00', [
                        ('msgs_avg', 0, None, None, None, None)
                    ]
                )
            ]
        )
    ]
}
