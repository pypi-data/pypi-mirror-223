import pytest
import wandb as wb
from wbutils import create_artifact

TRAIN_DATA = [
    {
        'en': 'Hello!',
        'pt': 'Olá!'
    },
    {
        'en': 'I love eating pizza.',
        'pt': 'Eu amo comer pizza.'
    }
]


def test_create_artifact_basic():
    artifact = create_artifact(artifact_name='dummy', artifact_type='dummy-type', description='Dummy artifact',
                               metadata={}, files={})
    assert isinstance(artifact, wb.Artifact)


def test_create_artifact_basic():
    files = {
        'train.json': TRAIN_DATA
    }
    metadata = {
        'source': 'manual',
        'task': 'translation'
    }
    description = 'Sample PT to EN translation'
    artifact = create_artifact(artifact_name='pt-to-en-train', artifact_type='pt-to-en-translation',
                               description=description, metadata=metadata, files=files)
    assert isinstance(artifact, wb.Artifact)
