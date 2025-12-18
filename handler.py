import os
import requests
import runpod
from infer_umamba import run_inference
from storage import upload_to_r2  # ou onde estiver essa função


def handler(event):
    # ===============================
    # 1) INPUT
    # ===============================
    job_id = event["input"]["job_id"]
    input_url = event["input"]["input_url"]

    print(f"[JOB {job_id}] Starting job")
    print(f"[JOB {job_id}] Input URL: {input_url}")

    # ===============================
    # 2) WORKDIR ISOLADO
    # ===============================
    workdir = f"/tmp/{job_id}"
    input_dir = os.path.join(workdir, "input")
    output_dir = os.path.join(workdir, "output")

    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    input_path = os.path.join(input_dir, "case_0000.nii.gz")

    # ===============================
    # 3) DOWNLOAD
    # ===============================
    r = requests.get(input_url, timeout=120)
    r.raise_for_status()

    with open(input_path, "wb") as f:
        f.write(r.content)

    print(f"[JOB {job_id}] Input downloaded")

    # ===============================
    # 4) INFERÊNCIA
    # ===============================
    run_inference(input_path, output_dir)

    print(f"[JOB {job_id}] Inference finished")

    # ===============================
    # 5) UPLOAD RESULTADO
    # ===============================
    mask_path = os.path.join(output_dir, "case_mask.nii.gz")

    if not os.path.exists(mask_path):
        raise RuntimeError("Mask file not found after inference")

    mask_url = upload_to_r2(mask_path)

    print(f"[JOB {job_id}] Mask uploaded: {mask_url}")

    # ===============================
    # 6) OUTPUT
    # ===============================
    return {
        "status": "ok",
        "mask_url": mask_url
    }


runpod.serverless.start({"handler": handler})
