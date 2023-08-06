from __future__ import annotations

import os
import wandb as wb

from .io import get_temp_path_to_file, EXTENSION_TO_IO


def create_artifact(artifact_name: str, artifact_type: str, description: str, metadata,
                    files: dict[str, object], extension_to_io: dict = EXTENSION_TO_IO) -> wb.Artifact:
    if 'files' in metadata:
        metadata['files_'] = metadata['files']
    metadata['files'] = list(files.keys())  # We need list because `odict_keys` cannot be serialized

    artifact = wb.Artifact(name=artifact_name, type=artifact_type, description=description, metadata=metadata)
    for filename, payload in files.items():
        extension = os.path.splitext(filename)[-1][1:]
        _, write_fn = extension_to_io[extension]
        path_to_file = get_temp_path_to_file(filename)
        write_fn(payload, path_to_file)
        artifact.add_file(path_to_file)
    return artifact


def load_data_from_artifact(artifact: wb.Artifact, path_to_artifact_folder: str | None,
                            extension_to_io: dict = EXTENSION_TO_IO) -> dict:
    if path_to_artifact_folder is None:
        path_to_artifact_folder = artifact.download()
    files = {}
    for filename in artifact.metadata['files']:
        extension = os.path.splitext(filename)[-1][1:]
        read_fn, _ = extension_to_io[extension]
        path_to_file = os.path.join(path_to_artifact_folder, filename)
        payload = read_fn(path_to_file)
        files[filename] = payload
    return files
