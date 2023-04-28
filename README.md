# forticlient_calculator
a script to analyze forticlient logs


Leggi il file di Log da FortiClient e calcola le ore di connessione al giorno


## Duration

Create 2 different csv files: one with all the connections, the other with the daily sum.

## Plot

call via cli with no args makes an annual report:

py src\plot.py


if month option is passed, it plots the durations for the month:

py src\plot.py --month=03-2023
