"""Instruction Finetuning API"""
import random
import string
from typing import Dict, Optional

from mcli.api.cluster.api_get_clusters import get_clusters
from mcli.api.model.cluster_details import ClusterDetails
from mcli.api.runs import Run, create_run
from mcli.models.run_config import ComputeConfig, RunConfig, SchedulingConfig
from mcli.utils.utils_finetune import Model, get_mpt_parameters_dict


# TODO: migrate endpoints to the control plane instead of MCLI
###### Finetuning ######
def instruction_finetune(model: str,
                         train_data_path: str,
                         checkpoint_save_folder: str,
                         cluster: str,
                         eval_data_path: Optional[str] = None,
                         gpu_type: Optional[str] = None,
                         gpus: Optional[int] = None,
                         training_duration: str = '1ep',
                         wandb_config: Optional[Dict] = None) -> Run:
    """Finetunes a model on a small dataset and converts an MPT composer checkpoint to a
    hugging face checkpoint for inference.

    Args:
        model (str): Model to finetune (e.g. 'mosaicml/mpt-30b')
        train_data_path (str): HF dataset or remote path to training data
        checkpoint_save_folder (str): Folder to save checkpoints and HF checkpoints, currently must be an s3 or GCP path
        cluster (str): Name of cluster to run finetuning job on
        eval_data_path (Optional[str]): HF dataset or remote path to eval data
        gpu_type (Optional[str]): GPU type to train on
        gpus (Optional[int]): Number of GPUs to train on
        training_duration (str): Composer variable for the total number of epochs 
                                 or tokens to train on (e.g. 2ep or 10000tok)
        wandb_config (Optional[Dict]): Wandb config (e.g. {'entity': <your entity>, 'project': <your project>})
    """
    # Setup
    model_object = Model(model)
    short_model_name = model_object.get_short_name()

    # TODO: add other MPT model variants
    if short_model_name not in ['mpt-7b', 'mpt-30b', 'mpt-7b-8k']:
        raise ValueError(f'Invalid model name: {model}. Currently only supports mosaicml/mpt-7b, \
            mosaicml/mpt-30b, and mosaicml/mpt-7b-8k.')

    unique_identifier = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    run_name: str = f'finetune-{short_model_name}-{unique_identifier}'
    checkpoint_save_folder = checkpoint_save_folder.rstrip('/')
    checkpoint_path: str = f'{checkpoint_save_folder}/{run_name}/checkpoints'
    hf_checkpoint_path: str = f'{checkpoint_save_folder}/{run_name}/hf_checkpoints'

    # For now, we are utilizing the Composer trainer script in llm-foundry.
    # We should consider de-coupling our finetuning service from external, public repos
    integrations: list = [{
        'integration_type': 'git_repo',
        'git_repo': 'mosaicml/llm-foundry',
        'git_commit': '05c6055ed38c495df746bcc97ac371fa61acb2ef',
        'pip_install': '-e .[gpu]',
        'ssh_clone': False,  # Should be true if using a private repo
    }]

    # Auto-infer instance and number of gpus, defaults to 1 node
    final_gpu_type: Optional[str] = gpu_type
    final_gpus: Optional[int] = gpus
    if gpu_type is None or gpus is None:
        found_cluster: ClusterDetails = get_clusters([cluster])[0]
        # Find instance
        instance = [inst for inst in found_cluster.cluster_instances if inst.gpus > 0][0]
        final_gpu_type = gpu_type if gpu_type is not None else instance.gpu_type
        final_gpus = gpus if gpus is not None else instance.gpus

    if final_gpu_type is None or final_gpus is None:
        raise ValueError('Could not read GPU details from cluster. Please manually specify `gpu_type` \
            and `gpus` when calling `instruction_finetune`.')

    compute_config: ComputeConfig = {
        'cluster': cluster,
        'gpu_type': final_gpu_type,
        'gpus': final_gpus,
    }

    if model_object.model == 'mosaicml/mpt-7b':
        max_seq_len = 2048
    elif model_object.model == 'mosaicml/mpt-30b':
        max_seq_len = 8192
    elif model_object.model == 'mosaicml/mpt-7b-8k':
        max_seq_len = 8192
    else:
        raise NotImplementedError(f'Unsupported model: {model_object.model}')

    parameters = get_mpt_parameters_dict(model_name=model_object.model,
                                         train_data_path=train_data_path,
                                         checkpoint_save_folder=checkpoint_path,
                                         max_duration=training_duration,
                                         gpus=final_gpus,
                                         max_seq_len=max_seq_len)

    if wandb_config is not None:
        wandb_config['integration_type'] = 'wandb'
        integrations.append(wandb_config)
        parameters['loggers'] = {'wandb': {}}
        # TODO: add Composer prompts callback if wandb is enabled

    # Add eval block if provided
    if eval_data_path is not None:
        parameters['eval_interval'] = '0.25dur'
        parameters['eval_loader'] = {
            'name': 'finetuning',
            'dataset': {
                'hf_name': eval_data_path,
                'split': 'test',
                'max_seq_len': max_seq_len,
                'allow_pad_trimming': False,
                'decoder_only_format': True,
                # packing_ratio:
                'shuffle': False
            },
            'drop_last': True,
            'num_workers': 8,
            'pin_memory': False,
            'prefetch_factor': 2,
            'persistent_workers': True,
            'timeout': 0,
            'eval_first': True,  # Whether to evaluate the model before training
            'eval_subset_num_batches': -1,  # How many batches to evaluate on. -1 means evaluate on the entire dataset
            'device_eval_batch_size': 8,  # Evaluation batch size per GPU
        }

    # Create the scheduling config
    scheduling: SchedulingConfig = {
        'resumable': True,  # TODO: use watchdog instead, when available
    }

    command: str = f"""
        cd llm-foundry/scripts && \
        composer train/train.py $PARAMETERS && \
        cd inference && \
        python convert_composer_to_hf.py \
            --composer_path {checkpoint_path}/latest-rank0.pt.symlink \
            --hf_output_path {hf_checkpoint_path} \
            --output_precision bf16
    """

    run_config = RunConfig(
        name=run_name,
        compute=compute_config,
        image='mosaicml/pytorch:2.0.1_cu118-python3.10-ubuntu20.04',
        integrations=integrations,
        command=command,
        parameters=parameters,
        scheduling=scheduling,
    )

    # Run the finetuning job
    return create_run(run_config)
