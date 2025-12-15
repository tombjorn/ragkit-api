DND_SCHEMA = {
    "name": "dnd",
    "description": "D&D RAG pipeline with lore + rules",
    "blocks": [
        {
            "id": "augmentation",
            "type": "AugmentationBlock",
            "options": {
                "hyde": {
                    "enabled": True,
                    "description": "Hypothetical document expansion"
                }
            }
        },
        {
            "id": "retriever",
            "type": "RetrieverBlock",
            "options": {
                "top_k": {
                    "type": "int",
                    "default": 3,
                    "min": 1,
                    "max": 10
                }
            }
        },
        {
            "id": "generator",
            "type": "GeneratorBlock"
        }
    ]
}
