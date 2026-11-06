# mutt-hildon: a graphical mail client on top of Mutt

A small Maemo 5 application (Python 2.5, PyGTK, python-hildon). It is a GUI layer over command line tools:
**it has no network code of its own, it only runs commands.**

| Task | Done by |
|---|---|
| read INBOX (list, message body) | `curl` 8.x (mbedTLS, TLS 1.3) over IMAP; the login goes through stdin, never the command line |
| send, reply | `msmtp` (the command from `set sendmail` in `~/.muttrc`) |
| full client | menu item **Open Mutt** starts `osso-xterm -e mutt` |

Why not Python `imaplib`: Python 2.5 uses OpenSSL 0.9.8 (TLS 1.0) and Centrum refuses TLS 1.0. Through curl it works.

The package depends on `mutt`, `msmtp`, `curl`, `python2.5`, `python-gtk2` and `python2.5-hildon`.

## Setup
There is none of its own. It reads `~/.muttrc` (`imap_user`, `folder`, `realname`, `from`, `sendmail`) and the password
from `~/.msmtp-password` (mode 600), like Mutt and msmtp do. Nothing secret is ever written to the repository.
```sh
(umask 077; read -s -p 'Password: ' p; echo; echo "$p" > ~/.msmtp-password)
```
Start it with the **Mail (Mutt)** icon in the menu or with `mutt-hildon`. Run it as the user `user`, not as root.

## Features (version 0.4)
- the 25 newest INBOX messages (sender, date, subject, Czech text works), refresh and "Older messages" (next page of history) from the menu,
- reading a message (text/plain, otherwise HTML with the tags removed), list of attachments (not saved yet),
- reply with a quote, new message, sending through msmtp, errors shown as banners,
- **Disk cache** (SQLite, `~/.mutt-hildon/cache.db`, module `store.py`): headers and every message body you open are kept.
  The list appears at once on start (before any network traffic), opened messages show in milliseconds and the
  cache can be read without a connection. Refresh updates it, forgets messages deleted on the server and keeps the
  newest N (setting "Messages kept on disk", default 300). "Older messages" shows cached ones first, then downloads.
- **Outbox**: when sending fails (no network, server error) the message is not lost, it is saved in the same database.
  The title shows `Mail (2 unsent)`. The **Refresh** button first tries to send the outbox, then reads mail (the
  automatic timer only reads). The **Outbox** menu lists the unsent messages with the last error; tap one to edit
  it again, or discard all.
- **Delete** (message menu): the message is copied to the trash folder from `set trash` in `~/.muttrc` and removed from INBOX.
  The Message-ID is checked first, so a changed mailbox never deletes the wrong message. EXPUNGE also removes other
  messages already flagged as deleted (for example by Mutt),
- **Settings** (main menu, saved in `~/.mutt-hildon.conf`): automatic refresh interval in minutes (default 0 = off, so
  mail is fetched only when the window opens or on Refresh), page size (25), ask before deleting, delete to trash,
- **Address completion** in the "To" field (module `contacts.py`): after two typed letters of a name or address it suggests
  matches for the part after the last comma. Two sources: the phone address book (`~/.osso-abook/db/addressbook.db`, read
  only, the EMAIL fields of its vCards) and addresses learned from the mail itself (senders of cached messages and
  recipients of sent ones, table `addresses` in the cache). The phone book of this N900 holds only phone numbers, so for now
  the learned addresses are what you get; add e-mail addresses to contacts in the stock Contacts application and they
  show up at once. The completion window itself could not be tested without a display,
- opening Mutt.

## Not yet
Move to other folders, the "seen" flag (curl `BODY[]` marks a message as read; cached messages are not downloaded again), folders other than INBOX, attachments, several
accounts, refresh while the application is closed, a cache of messages other than INBOX, translations (gettext).
These items are in [TODO.md](../../TODO.md).

## Tests
`make -C apps/mutt-hildon test`: package, files, .desktop entry and icons, strict Python 2.5 compilation, an offline
self-test of the back end (`/opt/mutt-hildon/selftest.py`: RFC 2047 headers, multipart, HTML, message building,
configuration, paging, delete guard, settings, cache, outbox, vCard parsing, address learning and suggestions) and, when the account is configured, a read-only INBOX listing. The window itself cannot be tested
without a display; it was tried by hand on the phone.

## Files
`mailcore.py` (IMAP/SMTP back end without GUI), `store.py` (SQLite cache, outbox, learned addresses), `contacts.py` (address book and suggestions), `mutt-hildon` (windows), `selftest.py`, `make-icon.sh` and `icons/` (ImageMagick
generated icons), `package.sh`, `test.sh`.
