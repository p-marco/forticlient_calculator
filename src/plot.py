import csv
from datetime import datetime, timedelta
import argparse
import matplotlib.pyplot as plt


def convert_duration(duration_str):
    hours, minutes, seconds = duration_str.split(':')
    return float(hours) + float(minutes) / 60 + float(seconds) / 3600


def generate_report(data, start_date=None, end_date=None):
    # selezionare solo i dati nell'intervallo specificato
    selected_data = data
    if start_date is not None:
        selected_data = [(date, dur) for date, dur in selected_data if date >= start_date]
    if end_date is not None:
        selected_data = [(date, dur) for date, dur in selected_data if date <= end_date]

    # aggregare i dati per giorno o per mese
    if start_date is None and end_date is None:
        # aggregare i dati per mese
        grouped_data = {}
        for date, dur in selected_data:
            key = date.strftime('%Y-%m')
            if key not in grouped_data:
                grouped_data[key] = []
            grouped_data[key].append(dur)
        xlabel = 'Mese'
        ylabel = 'Durata media (ore)'
    else:
        # aggregare i dati per giorno
        grouped_data = {}
        for date, dur in selected_data:
            key = date.strftime('%Y-%m-%d')
            if key not in grouped_data:
                grouped_data[key] = []
            grouped_data[key].append(dur)
        xlabel = 'Giorno'
        ylabel = 'Durata (ore)'

    # calcolare la durata media per ogni periodo di tempo
    averages = {}
    for key, data in grouped_data.items():
        averages[key] = sum(data) / len(data)

    # Calcola la durata totale del mese
    total_month_duration = sum(sum(data) for data in grouped_data.values())

    # creare il grafico
    fig, ax = plt.subplots()
    ax.plot(list(averages.keys()), list(averages.values()))

    # impostare le etichette dell'asse X
    if start_date is None and end_date is None:
        ax.set_xticklabels(list(averages.keys()), rotation=45)
    else:
        x_labels = []
        for date in averages.keys():
            dt = datetime.strptime(date, "%Y-%m-%d")
            day_of_week = dt.strftime("%a")  # Ottieni il giorno della settimana abbreviato
            duration = round(averages[date], 2)  # Ottieni la durata e arrotonda a 2 decimali
            x_labels.append(f"{date[-2:]} ({day_of_week})\n{duration}")
        ax.set_xticklabels(x_labels)

    # impostare le etichette degli assi
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # Imposta il titolo del grafico con la durata totale del mese
    ax.set_title(f"Durata totale del mese: {total_month_duration:.2f} ore")


    # visualizzare il grafico
    plt.show()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--month', type=str, help='Genera un report mensile')
    parser.add_argument('--file', type=str, default='data/durations.csv', help='Nome del file CSV di input')
    return parser.parse_args()


if __name__ == '__main__':
    # analizzare gli argomenti della linea di comando
    args = parse_args()

    # aprire il file CSV e leggere i dati
    with open(args.file, 'r') as f:
        reader = csv.reader(f)
        data = [(datetime.strptime(row[0], '%Y-%m-%d'), convert_duration(row[1])) for row in reader]

    if args.month:
        # generare il report mensile per il mese specificato
        month, year = args.month.split('-')
        start_date = datetime(int(year), int(month), 1)
        end_date = start_date.replace(day=1, month=start_date.month + 1) - timedelta(days=1)
        generate_report(data, start_date=start_date, end_date=end_date)
    else:
        # generare il report annuale
        generate_report(data)
