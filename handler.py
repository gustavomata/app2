import os
import requests
import runpod
from infer_umamba import run_inference

INPUT_PATH = "/app/data/input/case_0000.nii.gz"

def handler(event):
    job_id = event["input"]["job_id"]
    input_url = event["input"]["input_url"]

    output_dir = f"/app/data/output/{job_id}"
    os.makedirs("/app/data/input", exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # 1️⃣ baixar NIfTI
    r = requests.get(input_url, timeout=120)
    r.raise_for_status()
    with open(INPUT_PATH, "wb") as f:
        f.write(r.content)

    # 2️⃣ rodar inferência
    run_inference(INPUT_PATH, output_dir)

    # 3️⃣ subir máscara (exemplo)
    mask_path = os.path.join(output_dir, "case_mask.nii.gz")
    mask_url = upload_to_r2(mask_path)

    return {
        "status": "ok",
        "mask_url": mask_url
    }

runpod.serverless.start({"handler": handler})