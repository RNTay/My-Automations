#!/usr/bin/env python3

import re


def shorten_zoom_invitation(invitation: str) -> str:
    topic_pattern = r'Topic: ([\w .,?!/:\(\)\']*)'
    topic_string = re.findall(topic_pattern, invitation)[0]

    time_pattern = r'Time: ([\w .,?!/:\(\)]*)'
    time_string = re.findall(time_pattern, invitation)[0]
    group_time_pattern = r'([\w ]+), (\d+) ([\w :]+)'
    group_time_string = re.findall(group_time_pattern, time_string)[0]
    fixed_time_string = '{year} {month_day}, {time}'.format(year=group_time_string[1],
                                                            month_day=group_time_string[0],
                                                            time=group_time_string[2])

    link_pattern = r'Join Zoom Meeting\n([\w ./-=?]+)\n'
    link_string = re.findall(link_pattern, invitation)[0]

    meeting_id_pattern = r'(Meeting ID: [\d ]+)'
    meeting_id_string = re.findall(meeting_id_pattern, invitation)[0]

    passcode_pattern = r'(Passcode: [\w\d ]+)'
    passcode_string = re.findall(passcode_pattern, invitation)[0]

    shortened_invitation = '''{topic}
{time}

{link}

{meeting_id}
{passcode}'''.format(topic=topic_string,
                     time=fixed_time_string,
                     link=link_string,
                     meeting_id=meeting_id_string,
                     passcode=passcode_string)

    return shortened_invitation
