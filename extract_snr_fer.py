import re
import sys
import csv
import os

def extract_metrics(input_path, output_path):
    # Pattern to capture SNR, FECFRAMEs, FER, TS Packets, PER
    pattern = re.compile(
        r"SNR=([\d\.]+);.*?FECFRAMEs=(\d+);.*?FER=([\d\.eE+-]+);.*?TS Packets=(\d+);.*?PER=([\d\.eE+-]+)"
    )

    records = []

    with open(input_path, "r", encoding="utf-8") as file:
        for line in file:
            match = pattern.search(line)
            if match:
                snr = float(match.group(1))
                fecframes = int(match.group(2))
                fer = float(match.group(3))
                ts_packets = int(match.group(4))
                per = float(match.group(5))
                records.append([snr, fer, fecframes, ts_packets, per])

    with open(output_path, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["SNR", "FER", "FECFRAMEs", "TS_Packets", "PER"])
        writer.writerows(records)

    print(f"Saved extracted data to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_snr_fer.py <input_file.txt> <output_file.csv>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not output_file.lower().endswith(".csv"):
        output_file += ".csv"

    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        sys.exit(1)

    extract_metrics(input_file, output_file)
