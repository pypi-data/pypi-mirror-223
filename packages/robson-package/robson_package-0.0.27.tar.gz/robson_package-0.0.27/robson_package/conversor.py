class Temperatura:
    def __init__(self, celsius):
        self.valor = celsius

    def converter_farenheit(self):
        return self.valor * 1.8 + 32
    
    def converter_kelvin(self):
        return self.valor + 273.15
    

if __name__ == "__main__":
    celsius = float(input("Digite a temperatura em Celsius: "))
    conversor = Temperatura(celsius)
    print(f"{celsius}°C equivale a {conversor.converter_farenheit()}°F")
    print(f"{celsius}°C equivale a {conversor.converter_kelvin()}K")