# -*- coding: utf-8 -*-
# Address suggestions for the "To" field of mutt-hildon (Python 2.5).
# Sources: (1) the phone address book (Maemo osso-abook, a Berkeley DB of vCards, read-only),
# (2) addresses learned from the mail itself (senders of cached messages, recipients of sent messages; table
# `addresses` in store.py). Both are merged by suggest().
import os
import email.utils

BOOK = os.path.join("~", ".osso-abook", "db", "addressbook.db")


def parse_vcards(text):
    """vCard text (3.0, may hold many cards) -> [(name, address)], one item per EMAIL line."""
    # Unfold continuation lines (RFC 2426): a line starting with a space or a tab continues the previous one.
    lines = []
    for ln in text.replace("\r", "").split("\n"):
        if ln[:1] in (" ", "\t") and lines:
            lines[-1] += ln[1:]
        else:
            lines.append(ln)
    res = []
    name = u""
    emails = []
    for ln in lines + ["END:VCARD"]:
        field = ln.split(":")[0].split(";")[0].upper()      # "EMAIL;TYPE=INTERNET:a@b" -> "EMAIL"
        value = ln.split(":", 1)[-1].strip()
        if field == "BEGIN":
            name, emails = u"", []
        elif field == "FN":
            name = value.decode("utf-8", "replace")
        elif field == "EMAIL" and "@" in value:
            emails.append(value.decode("utf-8", "replace"))
        elif field == "END":
            for a in emails:
                res.append((name, a))
            name, emails = u"", []
    return res


def read_addressbook(path=None):
    """All (name, address) pairs of the phone address book; [] when it is missing or unreadable."""
    path = os.path.expanduser(path or BOOK)
    try:
        import bsddb
        db = bsddb.hashopen(path, "r")
    except Exception:
        return []
    res = []
    try:
        for k in db.keys():
            res.extend(parse_vcards(db[k]))
    finally:
        db.close()
    return res


def addresses_in(value):
    """'A <a@x>, b@y' -> [(u'A', u'a@x'), (u'', u'b@y')]"""
    return [(n, a) for n, a in email.utils.getaddresses([value or u""]) if "@" in a]


def format_address(name, addr):
    if name:
        return u'%s <%s>' % (name, addr)
    return addr


def last_token(text):
    """The part of the To field after the last comma: (head including the comma and space, token)."""
    pos = text.rfind(",")
    return text[:pos + 1] + (pos >= 0 and text[pos + 1:pos + 2] == " " and " " or ""), text[pos + 1:].strip()


def suggest(store, book, token, limit=8):
    """Addresses whose name or address contains `token` (case-insensitive), the phone book first.
    Returns [(display, address)] without duplicates."""
    t = token.lower()
    if not t:
        return []
    seen = {}
    res = []
    for name, addr in list(book) + store.addr_search(t, limit * 2):
        key = addr.lower()
        if key in seen or (t not in key and t not in name.lower()):
            continue
        seen[key] = 1
        res.append((format_address(name, addr), addr))
        if len(res) >= limit:
            break
    return res
