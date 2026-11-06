# -*- coding: utf-8 -*-
# All names and subjects are fictional. Fills the cache of $HOME/.mutt-hildon with demo messages (used by: make hildon-run APP=mutt-hildon).
import sys
sys.path.insert(0, "/opt/mutt-hildon")
import store, mailcore

rows = [(u"Alice Example", u"Schůzka ve čtvrtek (demo)", "Thu, 05 Nov 2026 08:10:52 -0800", 3),
        (u"Example Shop", u"Your order", "Wed, 04 Nov 2026 08:10:52 -0800", 2),
        (u"Bob Sample", u"Re: Fotky z dovolen\xe9", "Tue, 03 Nov 2026 08:10:52 -0800", 1)]
s = store.Store()
items = []
for i, (sender, subject, date, idx) in enumerate(rows):
    items.append({"idx": idx, "message_id": "<m%d@x>" % i, "from": sender, "subject": subject,
                  "date": mailcore.short_date(date), "ts": mailcore.date_ts(date)})
s.upsert_headers(items)
# bodies too, so that opening a message works offline (there is no IMAP server and no curl here)
bodies = [u"Ahoj,\n\nschůzka je ve čtvrtek v 10:00. Dej vědět, jestli ti to vyhovuje.\n\nAlice",
          u"Thank you for your order. This is a demo message.",
          u"Ahoj, fotky z dovolené posílám v příštím mailu.\n\nBob"]
for it, (sender, subject, date, idx), body in zip(items, rows, bodies):
    s.set_body(it["message_id"], {"body": body, "attachments": [], "to": u"demo@example.cz", "date": date})
s.close()
