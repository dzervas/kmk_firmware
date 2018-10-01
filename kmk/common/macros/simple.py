import string

from kmk.common.event_defs import (hid_report_event, keycode_down_event,
                                   keycode_up_event)
from kmk.common.keycodes import Keycodes, char_lookup
from kmk.common.macros import KMKMacro


def simple_key_sequence(seq):
    def _simple_key_sequence(state):
        for key in seq:
            if not getattr(key, 'no_press', None):
                yield keycode_down_event(key)
                yield hid_report_event()

            if not getattr(key, 'no_release', None):
                yield keycode_up_event(key)
                yield hid_report_event()

    return KMKMacro(keydown=_simple_key_sequence)


def send_string(message):
    seq = []

    for char in message:
        kc = None

        if char in char_lookup:
            kc = char_lookup[char]
        elif char in string.ascii_letters + string.digits:
            kc = getattr(Keycodes.Common, 'KC_{}'.format(char.upper()))

            if char.isupper():
                kc = Keycodes.Modifiers.KC_LSHIFT(kc)

        seq.append(kc)

    return simple_key_sequence(seq)
