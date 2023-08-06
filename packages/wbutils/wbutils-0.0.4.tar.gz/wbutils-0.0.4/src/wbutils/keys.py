from __future__ import annotations

TRAIN_SPLIT = 'train'
VAL_SPLIT = 'val'
TEST_SPLIT = 'test'
CHECK_SPLIT = 'check'
SPLITS = [TRAIN_SPLIT, VAL_SPLIT, TEST_SPLIT]
SPLITS3 = [TRAIN_SPLIT, VAL_SPLIT, TEST_SPLIT]
SPLITS4 = [TRAIN_SPLIT, VAL_SPLIT, TEST_SPLIT, CHECK_SPLIT]


DATASET_ARTIFACT_TYPE = 'dataset'
MODEL_ARTIFACT_TYPE = 'model'
WEIGHTS_FILENAME = 'weights.pth'

LOSS = 'loss'
ACCURACY_PCT = 'acc_pct'
ACCURACY_FRAC = 'acc_frac'
EPOCH = 'n_epochs'
EXAMPLE = 'n_examples'
OPTIMIZER = 'optimizer'
BATCH_SIZE = 'batch_size'
LR = 'lr'
DROPOUT_RATE = 'dropout_rate'
