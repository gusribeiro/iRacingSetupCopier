# iRacing Setup Copier

[English](#english) | [Português](#português)

## English

### Description
iRacing Setup Copier is a Python utility that helps iRacing users automatically copy setup files (.sto) to their corresponding car folders in the iRacing setups directory. This tool is particularly useful for managing multiple setup files and ensuring they are placed in the correct car folders.

### Features
- Automatically detects setup folders in your iRacing directory
- Copies .sto files to their corresponding car folders based on the car code in the filename
- Provides both terminal and GUI feedback about the copying process
- Error handling and validation for file operations
- Supports the VRS setup file naming convention (VRS_25S1DS_CARCODE_*.sto)

### Requirements
- Python 3.x
- Windows operating system
- iRacing installed with the default setup directory structure

### Installation
1. Clone this repository:
```bash
git clone https://github.com/yourusername/iRacingSetupCopier.git
cd iRacingSetupCopier
```

2. No additional dependencies are required as the script uses only Python standard libraries.

### Usage
1. Download the latest executable from the releases page
2. Place the executable in the folder containing your .sto setup files
3. Double-click the executable to run it
4. The program will automatically:
   - Find your iRacing setups directory
   - Copy the setup files to their corresponding car folders
   - Show a summary of the operation results

### File Naming Convention
The script expects setup files to follow this naming pattern:
```
*_*_CARCODE_*.sto
```
Where:
- CARCODE must be in the third position, separated by underscores (_)
- CARCODE is the car identifier that matches the folder name in your iRacing setups directory

## Português

### Descrição
iRacing Setup Copier é uma utilidade em Python que ajuda usuários do iRacing a copiar automaticamente arquivos de setup (.sto) para suas respectivas pastas de carros no diretório de setups do iRacing. Esta ferramenta é particularmente útil para gerenciar múltiplos arquivos de setup e garantir que eles sejam colocados nas pastas corretas dos carros.

### Funcionalidades
- Detecta automaticamente as pastas de setup no seu diretório do iRacing
- Copia arquivos .sto para suas respectivas pastas de carros baseado no código do carro no nome do arquivo
- Fornece feedback tanto no terminal quanto em interface gráfica sobre o processo de cópia
- Tratamento de erros e validação para operações com arquivos
- Suporta a convenção de nomenclatura de arquivos de setup do VRS (VRS_25S1DS_CARCODE_*.sto)

### Requisitos
- Python 3.x
- Sistema operacional Windows
- iRacing instalado com a estrutura padrão de diretório de setups

### Instalação
1. Clone este repositório:
```bash
git clone https://github.com/yourusername/iRacingSetupCopier.git
cd iRacingSetupCopier
```

2. Não são necessárias dependências adicionais, pois o script utiliza apenas bibliotecas padrão do Python.

### Como Usar
1. Baixe o executável mais recente da página de releases
2. Coloque o executável na pasta que contém seus arquivos de setup .sto
3. Dê um duplo clique no executável para executá-lo
4. O programa irá automaticamente:
   - Encontrar seu diretório de setups do iRacing
   - Copiar os arquivos de setup para suas respectivas pastas de carros
   - Mostrar um resumo dos resultados da operação

### Convenção de Nomenclatura de Arquivos
O script espera que os arquivos de setup sigam este padrão de nome:
```
*_*_CARCODE_*.sto
```
Onde:
- CARCODE deve estar na terceira posição, separado por underscores (_)
- CARCODE é o identificador do carro que corresponde ao nome da pasta no seu diretório de setups do iRacing
