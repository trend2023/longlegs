# longlegs
Version 0.01

Simple python bscscan smart chain net gain/loss data scrapper.

Requires transactions list SCV file from BSCSCAN. Scrapper then cycles through every tx on the list, retrieving from bscscan how much BNB was spent (for buys) and how much BNB was received (for sells). Adding it all up for simple final report of total net gain/loss.

Example CSV file provided is of "bonfire" token, filtered from one specific wallet, suspected to belong to one of that project's developer.
