# See https://github.com/susam/mintotp

import base64
import hmac
import struct
import time


def hotp(key, counter, digits=6, digest="sha1"):
    key = base64.b32decode(key.upper() + "=" * ((8 - len(key)) % 8))
    counter = struct.pack(">Q", counter)
    mac = hmac.new(key, counter, digest).digest()
    offset = mac[-1] & 0x0F
    binary = struct.unpack(">L", mac[offset : offset + 4])[0] & 0x7FFFFFFF
    return str(binary)[-digits:].zfill(digits)


def totp(key, time_step=30, digits=6, digest="sha1"):
    return totp_offset(key, time_step, 0, digits, digest)


def totp_offset(key, time_step=30, offset=-30, digits=6, digest="sha1"):
    """Generate TOTP code from key for any past or future time (use negative offset for past)"""
    return hotp(key, int((time.time() + offset) / time_step), digits, digest)
