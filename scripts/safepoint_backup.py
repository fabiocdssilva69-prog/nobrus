#!/usr/bin/env python3
"""
Gera um SafePoint comprimido (.zip) de um diretório e calcula o hash SHA256 do arquivo resultante.
Uso:
  python safepoint_backup.py /caminho/para/diretorio -o /caminho/para/saidas
"""
import argparse
import datetime
import hashlib
import os
import shutil

def sha256_of_file(path: str) -> str:
    """Calcula o hash SHA256 de um arquivo."""
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def create_backup_zip(target_dir: str, output_dir: str = "."):
    """Cria um arquivo zip do diretório alvo e retorna o caminho e o hash SHA256."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    base_name = os.path.join(output_dir, f"colmeia_backup_{timestamp}")
    zip_path = shutil.make_archive(base_name, "zip", target_dir)
    checksum = sha256_of_file(zip_path)
    return zip_path, checksum

def main():
    parser = argparse.ArgumentParser(description="Cria um SafePoint zip e calcula o SHA256.")
    parser.add_argument("target_dir", help="Diretório a ser copiado")
    parser.add_argument("-o", "--output-dir", default=".", help="Diretório onde será salvo o backup zip")
    args = parser.parse_args()
    zip_path, checksum = create_backup_zip(args.target_dir, args.output_dir)
    print(f"Backup salvo em: {zip_path}")
    print(f"SHA256: {checksum}")

if __name__ == "__main__":
    main()
