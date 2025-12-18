import os
import subprocess

URL = "https://app2.cad4share.com/download/p1iikb6x9UxDJHz/ygXeGOlKmAa7L/nnUNet_results.zip"
TARGET = "/models"

if not os.path.exists(f"{TARGET}/nnUNet_results"):
    print("⬇️ Baixando models...")
    os.makedirs(TARGET, exist_ok=True)

    subprocess.run(["wget", "-O", "/tmp/models.zip", URL], check=True)
    subprocess.run(["unzip", "/tmp/models.zip", "-d", TARGET], check=True)

    print("✅ Models prontos")
else:
    print("✅ Models já existem")
