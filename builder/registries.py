from ragkit import (
    AugmentationBlock,
    RetrieverBlock,
    GeneratorBlock,
    SwitchBlock,
    LeastToMost
)
from ragkit import HyDE, StepBack

BLOCK_REGISTRY = {
    "augmentation": AugmentationBlock,
    "retriever": RetrieverBlock,
    "generator": GeneratorBlock,
    "switch": SwitchBlock,
}

AUGMENTATION_REGISTRY = {
    "hyde": HyDE,
    "stepback": StepBack,
    "least_to_most": LeastToMost
}
