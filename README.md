# mutt-hildon

A small graphical mail client for the **Nokia N900** (Maemo 5 / Fremantle): Python 2.5, PyGTK and Hildon on top of command line tools.
It has no network code of its own, it only runs `curl` (IMAP), `msmtp` (SMTP) and, when you want the full client, `mutt`.

Why: the stock Modest e-mail application speaks TLS 1.0 only and cannot log in to servers that require TLS 1.2 or newer. The tools
used here are modern builds (curl 8 with mbedTLS, msmtp, Mutt 2) with TLS 1.2/1.3.

## Features
- INBOX list (newest 25, paging), message reading (plain text, HTML stripped), Czech and other charsets,
- reply with quote, new message, address completion in the "To" field (phone address book and learned addresses),
- disk cache (SQLite), so the list appears at once and works offline; outbox for messages that could not be sent,
- delete to the trash folder, settings (refresh interval, page size),
- a menu item that opens full Mutt in the terminal.

Details and the list of missing features: [mutt-hildon.md](mutt-hildon.md).

## Install
Packages are built by the [nokia-n900-apps](https://github.com/n900-resurrection/nokia-n900-apps) project (cross-compiling workshop with
the Fremantle sysroot). On the phone you need `mutt`, `msmtp` and `curl` (modern builds from the same project), `python2.5`,
`python-gtk2` and `python2.5-hildon`; then install the `mutt-hildon` `.deb` with `dpkg -i`.

Setup is the same as for Mutt and msmtp: `~/.muttrc` (`imap_user`, `folder`, `realname`, `from`, `sendmail`) and the password in
`~/.msmtp-password` (mode 600). Nothing secret belongs in this repository. Run it as the normal user, not as root.

## Build
This repository is meant to be a submodule at `apps/mutt-hildon` of nokia-n900-apps; the `Makefile` includes `../../mk/app.mk` from there:
```sh
make -C apps/mutt-hildon deb      # package build/deb/mutt-hildon_<version>-1maemo1_armel.deb
make -C apps/mutt-hildon install  # copy to the phone and dpkg -i
make -C apps/mutt-hildon test     # on-device tests (package must be installed)
```
`selftest.py` (offline test of the back end) runs on the phone or under Python 2.5: `python2.5 selftest.py`.

## Files
`mailcore.py` (IMAP/SMTP back end without GUI), `store.py` (SQLite cache, outbox, learned addresses), `contacts.py` (address book),
`mutt-hildon` (windows), `selftest.py`, `make-icon.sh` and `icons/`, `build.sh`, `package.sh`, `test.sh`.

## License
[MIT](LICENSE)
