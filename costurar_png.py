import struct
import zlib
import os

# --- Dimensões da Imagem ---
WIDTH = 0
HEIGHT = 0
# ---------------------------------

def create_png(width, height, zlib_data):

    signature = b'\x89PNG\r\n\x1a\n'

    ihdr_content = struct.pack('!IIBBBBB', width, height, 8, 6, 0, 0, 0)
    ihdr_crc = struct.pack('!I', zlib.crc32(b'IHDR' + ihdr_content) & 0xFFFFFFFF)
    ihdr = struct.pack('!I', len(ihdr_content)) + b'IHDR' + ihdr_content + ihdr_crc

    idat_content = zlib_data
    idat_crc = struct.pack('!I', zlib.crc32(b'IDAT' + idat_content) & 0xFFFFFFFF)
    idat = struct.pack('!I', len(idat_content)) + b'IDAT' + idat_content + idat_crc

    iend_content = b''
    iend_crc = struct.pack('!I', zlib.crc32(b'IEND' + iend_content) & 0xFFFFFFFF)
    iend = struct.pack('!I', len(iend_content)) + b'IEND' + iend_content + iend_crc

    return signature + ihdr + idat + iend

try:
    with open('arquivo.zlib', 'rb') as f:
        zlib_data = f.read()

    png_data = create_png(WIDTH, HEIGHT, zlib_data)

    with open('arquivo_flag.png', 'wb') as f:
        f.write(png_data)

    print(f"[+] Imagem criada com sucesso: arquivo_flag.png ({WIDTH}x{HEIGHT})")

except FileNotFoundError:
    print("[-] Erro: Arquivo 'arquivo.zlib' não encontrado. Verifique se está na pasta certa.")
