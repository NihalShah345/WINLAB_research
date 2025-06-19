import re
import pandas as pd
import sys

def read_file_lines(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.readlines()
    except Exception as e:
        print(f"Error opening file: {e}")
        return []

def extract_gain_and_metrics(lines):
    records = []
    current_gain = None

    for line in lines:
        if "Gain" in line:
            try:
                parts = line.strip().split()
                gain_index = parts.index("Gain")
                current_gain = float(parts[gain_index + 1])
            except (ValueError, IndexError):
                continue

        elif "SNR=" in line and "FER=" in line and current_gain is not None:
            try:
                snr_match = re.search(r"SNR=([\d\.eE+-]+)", line)
                fer_match = re.search(r"FER=([\d\.eE+-]+)", line)
                if snr_match and fer_match:
                    snr = float(snr_match.group(1))
                    fer = float(fer_match.group(1))
                    records.append([current_gain, snr, fer])
            except ValueError:
                continue

    return records

def write_output_csv(data, out_path):
    try:
        df = pd.DataFrame(data, columns=["Gain", "SNR", "FER"])
        df.to_csv(out_path, index=False)
        print(f"Data written to CSV successfully at '{out_path}'.")
    except Exception as e:
        print(f"Error writing CSV: {e}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <input_file> <output_file>")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    lines = read_file_lines(input_file)
    if not lines:
        print("No data found.")
        return

    data = extract_gain_and_metrics(lines)
    if data:
        write_output_csv(data, output_file)
    else:
        print("No valid gain/SNR/FER data found.")

if __name__ == "__main__":
    main()
