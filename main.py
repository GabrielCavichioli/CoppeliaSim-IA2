import torch
import torch.nn as nn
import torch.optim as optim

#____________________________________________INICIALIZAÇÃO__________________________________________________________________
class RedeNeural(nn.Module):
    def __init__(self, num_matrizes, num_leituras_por_matriz, num_saidas): # Ajustando o construtor da biblioteca
        super(RedeNeural, self).__init__()
        self.num_matrizes = num_matrizes
        self.num_leituras_por_matriz = num_leituras_por_matriz
        
        # Definir as camadas da rede
        self.camada_entrada = nn.Linear(num_matrizes * num_leituras_por_matriz, 64)  # Ajustando a camada de entrada da rede
        self.activation = nn.ReLU()           # Função de ativação ReLU
        self.camada_oculta = nn.Linear(64, 32)  # Camada oculta adicional
        self.camada_saida = nn.Linear(32, num_saidas)   # Ajustar a camada de saída
        
    def forward(self, x):
        x = x.view(-1, self.num_matrizes * self.num_leituras_por_matriz)  # Ajustando a dimensão da entrada
        x = self.activation(self.camada_entrada(x))
        x = self.activation(self.camada_oculta(x))
        x = self.camada_saida(x)
        return x

# Instância do modelo
num_matrizes = 5  # Número de matrizes de leituras (irá depender da leitura do sensor)
num_leituras_por_matriz = 4  # Número de leituras por matriz  (irá depender da leitura do sensor)
num_saidas = 2  # Velocidade dos motores esquerdo e direito
modelo = RedeNeural(num_matrizes, num_leituras_por_matriz, num_saidas)

# Definindo a função de perda e o otimizador
criterio = nn.MSELoss()                       # Função de perda: Mean Squared Error (MSE)
otimizador = optim.SGD(modelo.parameters(), lr=0.1)  # Otimizador: Stochastic Gradient Descent (SGD)

# Criando dados de exemplo (inputs e targets)
# Supondo que temos dados de exemplo de forma (batch_size, num_matrizes, num_leituras_por_matriz)
X = torch.rand(10, num_matrizes, num_leituras_por_matriz)  # Exemplo de tensor de entrada
Y = torch.rand(10, num_saidas)  # Exemplo de tensor de saída (velocidade dos motores)

#____________________________________________Treinamento__________________________________________________________________
num_epochs = 10000
for epoch in range(num_epochs):
    # Forward pass (calcular previsões)
    outputs = modelo(X)
    loss = criterio(outputs, Y)  # Calcular a perda
    
    # Backward pass (calcular gradientes e atualizar pesos)
    otimizador.zero_grad()       # Zerar gradientes acumulados
    loss.backward()              # Calcular gradientes
    otimizador.step()            # Atualizar pesos
    
    # Imprimir métricas de desempenho
    if (epoch+1) % 1000 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

# Saída
with torch.no_grad():
    saidas_teste = modelo(X)
    print('Saídas do modelo:')
    print(saidas_teste)
