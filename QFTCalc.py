import matplotlib.pyplot as plt
import json
import os

class QFTCalculator:
    def __init__(self, storage_path="results.json"):
        self.storage_path = storage_path
        self.results = []
        self.load_results()

    def load_results(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r") as f:
                self.results = json.load(f)
        else:
            self.results = []

    def save_results(self):
        with open(self.storage_path, "w") as f:
            json.dump(self.results, f)

    def qft_gold_test(self, nil, tb1, tb2, mitogen):
        if nil > 8:
            return "Indeterminate"

        tb1_diff = tb1 - nil
        tb2_diff = tb2 - nil

        tb1_positive = tb1_diff >= 0.35 and tb1_diff >= 0.25 * nil
        tb2_positive = tb2_diff >= 0.35 and tb2_diff >= 0.25 * nil

        if tb1_positive or tb2_positive:
            return "Positive"

        tb1_negative = tb1_diff < 0.35 or (tb1_diff >= 0.35 and tb1_diff < 0.25 * nil)
        tb2_negative = tb2_diff < 0.35 or (tb2_diff >= 0.35 and tb2_diff < 0.25 * nil)

        if (tb1_negative or tb2_negative) and mitogen >= 0.5:
            return "Negative"
        else:
            return "Indeterminate"

    def input_sample(self):
        print("\nEnter the sample number and values for the 4 tubes:")
        try:
            sample_num = input("Sample number: ").strip()
            nil_input = input("Nil: ")
            nil = 10.00 if nil_input.strip() == '>10' else float(nil_input)

            tb1_input = input("TB1 (If >10 then enter '>10'): ")
            tb1 = 10.00 if tb1_input.strip() == '>10' else float(tb1_input)

            tb2_input = input("TB2 (If >10 then enter '>10'): ")
            tb2 = 10.00 if tb2_input.strip() == '>10' else float(tb2_input)

            mitogen_input = input("Mitogen (If >10 then enter '>10'): ")
            mitogen = 10.00 if mitogen_input.strip() == '>10' else float(mitogen_input)
        except ValueError:
            print("Invalid input. Please enter numeric values.")
            return None

        return (sample_num, nil, tb1, tb2, mitogen)

    def add_result(self, sample_num, nil, tb1, tb2, mitogen, result):
        self.results.append({
            "Sample": sample_num,
            "Nil": nil,
            "TB1": tb1,
            "TB2": tb2,
            "Mitogen": mitogen,
            "Result": result
        })
        self.save_results()

    def show_results(self):
        if not self.results:
            print("No results yet.")
            return

        print("\nPast Results:")
        for idx, r in enumerate(self.results, 1):
            print(f"{idx}: Sample={r['Sample']}, Nil={r['Nil']}, TB1={r['TB1']}, TB2={r['TB2']}, Mitogen={r['Mitogen']} => {r['Result']}")

    def plot_sample(self, sample_num, nil, tb1, tb2, mitogen):
        tubes = ['Nil', 'TB1', 'TB2', 'Mitogen']
        values = [nil, tb1, tb2, mitogen]
        plt.figure(figsize=(6,4))
        plt.bar(tubes, values, color=['gray', 'blue', 'green', 'red'])
        plt.xlabel("Tube")
        plt.ylabel("IFNy (Interferon Gamma)")
        plt.title(f"Sample {sample_num} - IFNy by Tube")

        # Threshold lines
        plt.axhline(0.35, color='orange', linestyle='--', label='0.35 threshold')
        plt.axhline(0.25 * nil, color='purple', linestyle=':', label='0.25 x Nil threshold')

        # Annotate thresholds
        plt.text(3.1, 0.35, '0.35', color='orange', va='bottom')
        plt.text(3.1, 0.25 * nil, f'0.25 x Nil ({0.25 * nil:.2f})', color='purple', va='bottom')

        # Add explanation
        plt.figtext(0.5, 0.01,
            "Positive: TB1 or TB2 >= 0.35 AND >= 0.25 x Nil\n"
            "Negative: TB1 and TB2 < 0.35 OR < 0.25 x Nil (if Mitogen >= 0.5)",
            ha="center", fontsize=9)

        plt.ylim(0, max(values + [0.35, 0.25 * nil]) + 1)
        plt.legend()
        plt.show()

    def plot_all_samples(self):
        if not self.results:
            print("No results to plot.")
            return
        tubes = ['Nil', 'TB1', 'TB2', 'Mitogen']
        plt.figure(figsize=(10,6))
        bar_width = 0.18
        x = range(len(tubes))
        for idx, r in enumerate(self.results):
            values = [r["Nil"], r["TB1"], r["TB2"], r["Mitogen"]]
            plt.bar([i + idx*bar_width for i in x], values, bar_width, label=f"Sample {r['Sample']}")
        plt.xticks([i + bar_width*(len(self.results)-1)/2 for i in x], tubes)
        plt.xlabel("Tube")
        plt.ylabel("IFNy (Interferon Gamma)")
        plt.title("All Samples - IFNy by Tube")
        plt.legend()
        plt.show()

def main_menu():
    calc = QFTCalculator()
    while True:
        print("\nQFT Calculator Menu:")
        print("1. Run new test")
        print("2. View past results")
        print("3. Plot all saved samples")
        print("4. Exit")
        choice = input("Choose an option: ").strip()
        if choice == '1':
            sample = calc.input_sample()
            if sample:
                sample_num, nil, tb1, tb2, mitogen = sample
                result = calc.qft_gold_test(nil, tb1, tb2, mitogen)
                print(f"Result: {result}")
                calc.add_result(sample_num, nil, tb1, tb2, mitogen, result)
                calc.plot_sample(sample_num, nil, tb1, tb2, mitogen)
        elif choice == '2':
            calc.show_results()
        elif choice == '3':
            calc.plot_all_samples()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu()
