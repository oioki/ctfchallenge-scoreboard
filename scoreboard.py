#!/usr/bin/env python3

import re
import requests

from jinja2 import Template

import config


REGEX_FLAG = r'.*<td style="text-align: center">(?P<date>[0-9]+/[0-9]+/[0-9]+ [0-9]+:[0-9]+:[0-9]+|)</td>'
REGEX_HINTS = r'.*<td style="text-align: center">(?P<hints_used>[0-9]+)/(?P<hints_total>[0-9]+)</td>'

DEMO_CONTEXT = {
    'title': 'Awesome CTF competition',
    'teams': [
        {
            'team': 'Crazy Panthers',
            'flags_found': 12,
            'hints_used': 3,
        },
        {
            'team': 'Border Hounds',
            'flags_found': 11,
            'hints_used': 8,
        },
        {
            'team': 'Nameless Sentinels',
            'flags_found': 10,
            'hints_used': 5,
        },
    ]}


context = {
    'title': config.TITLE,
    'teams': [],
}

for team in config.TEAMS:
    hints_used = hints_total = 0
    flags_found = flags_total = 0

    url = 'https://ctfchallenge.co.uk/user/{}'.format(team)
    r = requests.get(url)

    for line in r.text.split('\n'):
        m = re.match(REGEX_FLAG, line)
        if m:
            flags_total += 1
            if m.groupdict()['date'] != '':
                flags_found += 1

        m = re.match(REGEX_HINTS, line)
        if m:
            d = m.groupdict()
            hints_used += int(d['hints_used'])
            hints_total += int(d['hints_total'])

    context['teams'].append(
        {
            "team": team,
            "flags_found": flags_found,
            "hints_used": hints_used,
        }
    )

context['teams'] = sorted(context['teams'], key=lambda x: -x['flags_found'])

# comment line below to use actual scores from ctfchallenge.co.uk
context = DEMO_CONTEXT


with open('template.html', 'r') as f:
    template = Template(f.read())

with open('index.html', 'w') as f:
    f.write(template.render(context=context))
