# mutt-hildon: Hildon GUI over Mutt/msmtp (Python 2.5 scripts). Targets and conventions: ../../mk/app.mk
override APP     := mutt-hildon
VERSION ?= 0.4
# make-icon.sh writes icons/48.png and icons/64.png (package.sh installs them)
ICON_OUT := icons/64.png
RUN_CMD := /usr/bin/mutt-hildon
include ../../mk/app.mk
