def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

def fahrenheit_to_celsius(f):
    return (f - 32) * 5/9

def main():
    print("=== Temperature Converter ===")
    print("1. Celsius to Fahrenheit")
    print("2. Fahrenheit to Celsius")

    try:
        choice = input("Choose an option (1 or 2): ").strip()
        if choice not in ['1', '2']:
            raise ValueError("Invalid choice. Select 1 or 2.")

        temp = float(input("Enter the temperature: "))

        if choice == '1':
            if temp < -273.15:
                raise ValueError("Temperature below absolute zero.")
            result = celsius_to_fahrenheit(temp)
            print(f"{temp}°C = {result:.2f}°F")
        else:
            if temp < -459.67:
                raise ValueError("Temperature below absolute zero.")
            result = fahrenheit_to_celsius(temp)
            print(f"{temp}°F = {result:.2f}°C")

    except ValueError as e:
        print("Error:", e)

main()
