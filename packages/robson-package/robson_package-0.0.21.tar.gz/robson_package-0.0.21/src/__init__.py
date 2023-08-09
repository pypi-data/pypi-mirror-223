from robson_package import robson_package as rp

temp = rp.Conversor(25)
far = temp.converter_farenheit()
kel = temp.converter_kelvin()
print(f'25ºC equivale a {far}ºF e {kel}K')