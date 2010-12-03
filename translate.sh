#!/bin/bash
xgettext --keyword=tr blink/*.py blink/configuration/*.py blink/widgets/*.py blink/update/*.py -o locale/blink.pot
#msgfmt -o blink/locale/ru/LC_MESSAGES/blink.mo blink/locale/ru/LC_MESSAGES/blink.po
