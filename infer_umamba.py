import os
import torch
from os.path import join
from nnunetv2.inference.predict_from_raw_data import nnUNetPredictor
from nnunetv2.utilities.dataset_name_id_conversion import convert_id_to_dataset_name

def run_inference(case_img_path: str, out_dir: str):

    DATASET_ID = 112
    CONFIGURATION = "3d_fullres"
    CHECKPOINT_NAME = "checkpoint_best.pth"
    FOLDS = (1,)

    dataset_name = convert_id_to_dataset_name(DATASET_ID)

    model_dir = join(
        os.environ["nnUNet_results"],
        dataset_name,
        f"nnUNetTrainer__nnUNetPlans__{CONFIGURATION}",
    )

    if not os.path.isdir(model_dir):
        raise RuntimeError(f"Model folder not found: {model_dir}")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    predictor = nnUNetPredictor(
        tile_step_size=0.6,
        use_gaussian=False,
        use_mirroring=False,
        device=device,
        verbose=True,
    )

    predictor.initialize_from_trained_model_folder(
        model_dir,
        use_folds=FOLDS,
        checkpoint_name=CHECKPOINT_NAME,
    )

    os.makedirs(out_dir, exist_ok=True)

    predictor.predict_from_files(
        [(case_img_path,)],
        out_dir,
        save_probabilities=False,
        overwrite=True,
    )

    return out_dir