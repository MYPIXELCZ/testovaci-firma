#!/bin/sh
# Ke každé zprávě přidá pražský čas: Ondřejovi píšeme časy vždy v pražském čase (viz FAILS.md).
echo "Pražský čas: $(TZ=Europe/Prague date '+%-d. %-m. %Y %H:%M %Z') (UTC$(TZ=Europe/Prague date '+%:z')). Časy pro Ondřeje vždy převádět z UTC na pražský čas."
