from builder.registries import (BLOCK_REGISTRY, AUGMENTATION_REGISTRY) 

def list_blocks():
    """
    Returns block names + accepted parameters
    """
    blocks = {}

    for name, cls in BLOCK_REGISTRY.items():
        sig = cls.__init__.__annotations__
        blocks[name] = {
            "params": list(sig.keys()),
            "type": cls.__name__,
        }

    return blocks


def list_augmentations():
    return list(AUGMENTATION_REGISTRY.keys())
