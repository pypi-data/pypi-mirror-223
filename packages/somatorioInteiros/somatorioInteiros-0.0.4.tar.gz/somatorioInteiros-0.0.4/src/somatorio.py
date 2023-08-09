class somatorioInteiros:
    def __init__(self, numeros : list) -> None:
        self._numeros = numeros
    
    def somar(self):
        soma = 0
        for i in self._numeros:
            soma += int(i)
        return soma