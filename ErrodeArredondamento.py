import sympy as sp
x = sp.Symbol('x')

# Entrada da função
expressao = sp.sympify(input("Digite a função: "))

# Entradas dos limites do intervalo
a = sp.sympify(input("Digite o a: "))
b = sp.sympify(input("Digite o b: "))

# Converte para float apenas para os cálculos numéricos
a = float(a)
b = float(b)

# Número de trapézios e casas decimais
numero_trapezios = int(input("Digite o número de trapezios: "))
casas_decimais = int(input("Digite quantas casas decimais: "))

# Calcula o tamanho do passo
h = (b - a) / numero_trapezios

# Cria função numérica a partir da expressão simbólica
funcao_numerica = sp.lambdify(x, expressao, "math")

# Listas para armazenar os valores
valores_x = []
valores_fx = []

print("\nValor do passo:", round(h, casas_decimais))
print("\nTabela de valores:")
print("x\t f(x)")

# Preenche as listas e imprime a tabela com casas decimais fixas
for i in range(numero_trapezios + 1):
    xi = a + i * h
    fx = funcao_numerica(xi)
    
    valores_x.append(xi)
    valores_fx.append(fx)
    
    print(f"{xi:.{casas_decimais}f}\t {fx:.{casas_decimais}f}")

# Cálculo da área pelo método dos trapézios valores_fx[-1] sendo o ultimo valor da lista, entao o loop vai do segundo elemento ao penultimo
soma = (valores_fx[0] + valores_fx[-1]) / 2
for fx in valores_fx[1:-1]:
    soma += fx

area_trapezios = h * soma

# Erro de arredondamento
erro_arredondamento = numero_trapezios * (5 * 10**-(casas_decimais + 1)) * h

# Segunda derivada para erro de truncamento
segunda_derivada = sp.diff(expressao, x, 2)
f2 = sp.lambdify(x, segunda_derivada, "math")

# Calcula o máximo da segunda derivada
max_segunda = 0
for i in range(numero_trapezios + 1):
    xi = a + i * h
    valor = abs(f2(xi))
    if valor > max_segunda:
        max_segunda = valor

# Erro de truncamento usando a fórmula (b-a)^3 / 12 * max|f''(x)| / n^2,
# O que acontece e que utilizando a formula (b-a)^3 /12 * max|f''(x)| estava considerando como se fosse apenas 1 trapezio,
#como pra achar o maximo da segunda derivada dividimos em n(n sendo o numero de trapezios) subintervalos cada subintervalo tem um tamanho h = b-a/n
# e isso da um erro proporcional a h^3, entao cada subintervalo gera um erro <= h^3/12 * max|f''(x)
# uma vez que temos n trapezios cada um com um erro ~ h^3, ao somar todos eles da um erro perto de n * h^3
# entao temos erro de truncamento total = n * h^3/12 * max|f''(x)|
# substituindo o h por b-a/n temos que:
#                   n * (b-a/n)^3/12 * max|f''(x)| = n * (b-a)^3/12n^3 * max|f''(x)| = (b-a)^3/12n^2 * max|f''(x)|
erro_truncamento = ((b - a)**3 / 12) * max_segunda / numero_trapezios**2

# Erro total
erro_total = erro_arredondamento + erro_truncamento

# Intervalo com erro
inferior = area_trapezios - erro_total
superior = area_trapezios + erro_total

# Impressão dos resultados arredondados para o usuário
print("\nSoma das áreas dos trapézios:", round(area_trapezios, casas_decimais))
print("Erro de arredondamento <= ", round(erro_arredondamento, casas_decimais+1))
print("Erro de truncamento <= ", round(erro_truncamento, casas_decimais))
print("Erro total <= ", round(erro_total, casas_decimais))
print("Intervalo com erro:")
print(f"[{round(inferior, casas_decimais)} ; {round(superior, casas_decimais)}]")