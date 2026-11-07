# mutt-hildon: Hildon GUI over Mutt/msmtp (Python 2.5 scripts). Targets and conventions: ../../mk/app.mk
override APP     := mutt-hildon
VERSION ?= 0.4
RUN_CMD := /usr/bin/mutt-hildon
include ../../mk/app.mk
