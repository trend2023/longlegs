# longlegs
Version 0.01

UPDATE: As of 2021 Septemper 25th script is not working due to more robust anti-scrapping measures implemented by BSCscan. There's no ETA for working script.

Simple python bscscan smart chain net gain/loss data scrapper.

Requires transactions list CSV file from BSCSCAN. Scrapper then cycles through every tx on the list, retrieving from bscscan how much BNB was spent (for buys) and how much BNB was received (for sells). Adding it all up for simple final report of total net gain/loss.

Example CSV file provided is of "bonfire" token, filtered from one specific wallet, suspected to belong to one of that project's developer.
