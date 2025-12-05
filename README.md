# CTF Writeup: Reconstrução de Cabeçalho PNG a partir de Fluxo ZLIB Corrompido.
Este repositório documenta a metodologia utilizada para resolver um CTF fornecido em uma comunidade do Discord. O desafio em questão possuia uma imagem PNG que teve seu cabeçalho e metadados removidos, tornando-a irrecuperável por visualizadores padrão. O desafio exigiu análise forense de baixo nível e a aplicação de fórmulas de reconstrução de formatos de arquivo.

# 1. O Problema (O Desafio Forense)
O desafio inicial apresentava um arquivo de imagem (imagem.png) que:
  1. Não abria em viewers de imagem padrão.
  2. Ferramentas de análise de esteganografia (como zsteg) falhavam ao identificar conteúdo.
  3. O comando file clasisficava o arquivo como data genérico, confirmando a corrupção do cabeçalho

# 2. Metodologia de Análise
A solução exigiu o isolamento do payload de pixel bruto e a dedução da dimensão da imagem:

## 2.1 Extração do Conteúdo Embarcado
Para isolar os componentes internos do arquivo, foi utilizada a ferramenta de análise binária binwalk:
```bash
binwalk -e steg.png
```
O binwalk extraiu o conteúdo para uma pasta (_imagem.png.extracted), revelando dois componentes; um stream de dados brutos e um stream comprimindo ZLIB. Esta é a parte crítica, pois o ZLIB contém os dados de pixel que precisavam ser reconstruídos. 

## 2.2 A Lógica Crítica: Dedução de Dimensão
Com os pixels extraídos, o principal obstáculo era determinar a Largura (W) e a Altura (H), sem as quais a imagem não poderia ser reconstruída. Essa informação foi deduzida a partir do tamanho total do payload ZLIB e da estrutura do formato PNG:
  - BPP (Bytes por Pixel): Através da inspeção do arquivo, foi determinado o número de bytes por pixel (geralmente 3 para RGB).
  - Fórmula de Reconstrução: O tamanho do payload de dados não comprimidos em um PNG é a soma do tamanho de todas as linhas de scanline.
```
Tamanho Bruto = H x ((W x BPP) + 1)
```
Onde o +1 se refere ao byte de filtro que o PNG adiciona a cada nova linha horizontal. 

Através da busca por combinações de números inteiros que satisfizessem a equação para o tamanho bruto, a única dimensão lógica encontrada foi adicionada no arquivo. 

# 3. A Solução Técnica (Stitching em Python)
Com as dimensões confirmadas, o passo final foi programático. Um script Python foi criado para:
  1. Criar assinatura PNG (\x89PNG\r\n\x1a\n).
  2. Gerar o chunk IHDR (Image Header) contendo as dimensões e o BPP.
  3. "Costurar" (Stich) o stream ZLIB de pixels extraídos no chunk IDAT (Image Data).
  4. Gerar o CRC32 de cada chunk (como exigido pela especificação PNG).
O script reconstruiu a imagem, que voltou a ser um PNG válido.
