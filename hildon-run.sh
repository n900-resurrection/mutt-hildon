# Name: Mail (Mutt)
# Sourced by scripts/hildon-run.sh (INSIDE the Workshop) for: make hildon-run APP=mutt-hildon
# Prepares a throw-away home with demo data, so the GUI starts without an account and without any network traffic.
# Python 2.5 / PyGTK is what the program needs; the sources are copied to sysroot/opt/mutt-hildon (where qemu-user finds
# /opt/mutt-hildon, like on the phone), the home lives in build/fakehome and is created once (HILDON_RESET=1 starts from scratch).
PY2=1
export QEMU_LD_PREFIX="$SR" LC_ALL=C LANG=C
HOME="$PROJ/build/fakehome"
export HOME
mkdir -p "$HOME" "$SR/opt/mutt-hildon"
# the home and the demo data are created once (HILDON_RESET=1 makes them again), so a second start does not wipe the cache
[ -z "${HILDON_RESET:-}" ] || rm -rf "$HOME"; mkdir -p "$HOME"
cp "$PROJ"/apps/mutt-hildon/*.py "$PROJ/apps/mutt-hildon/mutt-hildon" "$SR/opt/mutt-hildon/"
cat > "$HOME/.muttrc" <<'RC'
set imap_user = "demo@centrum.cz"
set folder = "imaps://imap.invalid/"
set sendmail = "/bin/false"
set realname = "Demo"
RC
echo demo > "$HOME/.msmtp-password"; chmod 600 "$HOME/.msmtp-password"
# demo messages in the disk cache (the list appears from the cache before any network access)
[ -f "$HOME/.mutt-hildon/cache.db" ] || PYTHONPATH="$PROJ/scripts/hildon-stubs:/usr/lib/pymodules/python2.5/gtk-2.0:/usr/lib/pymodules/python2.5:/usr/lib/python2.5/site-packages" \
  qemu-arm "$SR/usr/bin/python2.5" "$PROJ/apps/mutt-hildon/hildon-demo-data.py"
RUN_SCRIPT=/opt/mutt-hildon/mutt-hildon
