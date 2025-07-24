def qft_gold_test(nil, tb1, tb2, mitogen):
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

while True:
    print("\nEnter the values for the 4 tubes:")
    try:
        nil_input = input("Nil: ")
        nil = 10.00 if nil_input.strip() == '>10' else float(nil_input)

        tb1_input = input("TB1: ")
        tb1 = 10.00 if tb1_input.strip() == '>10' else float(tb1_input)

        tb2_input = input("TB2: ")
        tb2 = 10.00 if tb2_input.strip() == '>10' else float(tb2_input)

        mitogen_input = input("Mitogen (If >10 then enter '>10'): ")
        mitogen = 10.00 if mitogen_input.strip() == '>10' else float(mitogen_input)
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        continue

    result = qft_gold_test(nil, tb1, tb2, mitogen)
    print(f"Result: {result}")

    again = input("Do you want to test another sample? (y/n): ").lower()
    if again != 'y':
        break