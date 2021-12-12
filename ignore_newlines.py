"""
Yield word changes, ignoring whitespace.

2021-12-11 v0.1 by Cees Timmerman
"""

import re
import sys


def same(old, new):
    r"""Compare without whitespace diffs.

    >>> same('long line', 'long\nline')
    True
    """
    old2 = re.sub('\\s+', ' ', f' {old} ')
    new2 = re.sub('\\s+', ' ', f' {new} ')
    # print(f"COMPARE {repr(old2)} TO {repr(new2)}")
    return old2 == new2


def no_whitespace_diff(file=sys.stdin):
    """Filter diff ouput.

    >>> from io import StringIO
    >>> for change in no_whitespace_diff(StringIO(
    ... '''3c3,4
    ... < bees are nice
    ... ---
    ... > bees are
    ... > nice
    ... 6,7c7,8
    ... < second
    ... < diff
    ... ---
    ... > second diff
    ... > and more!''')): print(change)
    6,7c7,8
    < second
    < diff
    ---
    > second diff
    > and more!
    """
    change = ''
    part = ''
    old = ''
    line: str
    for line in file:
        if re.match(r'^(?P<range1start>[0-9]+)(?P<range1end>,[0-9]+)?'
                    r'(?P<type>[acd])'  # Added, changed, or deleted.
                    r'(?P<range2start>[0-9]+)(?P<range2end>,[0-9]+)?$',
                    line):
            if not same(old, part):
                yield change
            change = ''
            part = ''
        elif line.startswith('---'):
            old = part
            part = ''
        else:
            part += line[2:]

        change += line

    if not same(old, part):
        yield change


def no_whitespace_cdiff(file=sys.stdin):
    """Filter cdiff ouput.

    >>> from io import StringIO
    >>> for change in no_whitespace_cdiff(StringIO(
    ... '''*** a.txt       2021-12-11 22:16:26.478662800 +0100
    ... --- b.txt       2021-12-11 23:50:41.235329900 +0100
    ... ***************
    ... *** 3 ****
    ... ! bees are nice
    ... --- 3,4 ----
    ... ! bees are
    ... ! nice
    ... ***************
    ... *** 6,7 ****
    ... ! second
    ... ! diff
    ... --- 7,8 ----
    ... ! second diff
    ... ! and more!''')): print(change, end='')
    *** a.txt       2021-12-11 22:16:26.478662800 +0100
    --- b.txt       2021-12-11 23:50:41.235329900 +0100
    ***************
    *** 6,7 ****
    ! second
    ! diff
    --- 7,8 ----
    ! second diff
    ! and more!
    """
    change = ''
    part = ''
    old = ''
    line: str
    for line in file:
        # print("LINE", repr(line))
        if re.match(r'^\*{3} (?P<range1start>[0-9]+)'
                    r'(?P<range1end>,[0-9]+)? \*{4}$', line):
            # print("PART1")
            if (not old and not part) or not same(old, part):
                # print("YIELDING CHANGE", repr(change))
                yield change
                change = ''
            else:
                # print(f"SKIPPING non-change for {repr(old)} vs {repr(part)} of {repr(change)}")
                change = ''
            # print("CLEARING PART", repr(part))
            part = ''
        elif re.match(r'^--- (?P<range2start>[0-9]+)'
                      r'(?P<range2end>,[0-9]+)? ----$', line):
            # print("PART2")
            old = part
            part = ''
        elif re.match(r'^[*-]{3}', line):
            # print("CRUFT")
            pass
        else:
            part += line[2:]

        change += line
        # print("CHANGE", repr(change))

    if not same(old, part):
        yield change


def no_whitespace_udiff(file=sys.stdin):
    """Filter udiff ouput.

    >>> from io import StringIO
    >>> for change in no_whitespace_cdiff(StringIO(
    ... '''*** a.txt       2021-12-11 22:16:26.478662800 +0100
    ... --- b.txt       2021-12-11 23:50:41.235329900 +0100
    ... ***************
    ... *** 3 ****
    ... ! bees are nice
    ... --- 3,4 ----
    ... ! bees are
    ... ! nice
    ... ***************
    ... *** 6,7 ****
    ... ! second
    ... ! diff
    ... --- 7,8 ----
    ... ! second diff
    ... ! and more!''')): print(change, end='')
    *** a.txt       2021-12-11 22:16:26.478662800 +0100
    --- b.txt       2021-12-11 23:50:41.235329900 +0100
    ***************
    *** 6,7 ****
    ! second
    ! diff
    --- 7,8 ----
    ! second diff
    ! and more!
    """
    change = ''
    part = ''
    old = ''
    old_change_type = ''
    line: str
    for line in file:
        # print("LINE", repr(line))
        if re.match(r'^@@ [+-](?P<range1start>[0-9]+)'
                    r'(?P<range1end>,[0-9]+)?'
                    r' [+-](?P<range2start>[0-9]+)'
                    r'(?P<range2end>,[0-9]+)? @@$', line):
            if same(old, part):
                # print("SKIP")
                change = ''
            else:
                # print("YIELD", repr(change))
                yield change
                change = ''
            # print("CLEARING PART", repr(part))
            old = ''
            part = ''
        elif re.match(r'^[+-]{3} ', line):
            # TODO: Test -- and ++ line diff!
            yield line
            continue
        else:
            change_type = line[0]
            if change_type != old_change_type:
                #  print("PART2 FR!", change_type)
                old = part
                part = ''
                old_change_type = change_type

            part += line[1:]
            # print("OLD", repr(old), "PART", repr(part))

        change += line
        # print("CHANGE", repr(change))

    if not same(old, part):
        # print("YIELD LAST", repr(change))
        yield change


if __name__ == '__main__':
    fun = no_whitespace_diff
    if '-c' in sys.argv:
        fun = no_whitespace_cdiff
    elif '-u' in sys.argv:
        fun = no_whitespace_udiff
    for diff in fun():
        print(diff, end='')
