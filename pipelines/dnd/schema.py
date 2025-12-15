DND_SCHEMA = {
    "name": "dnd",

    "config": {
        "collection_name": "dnd",
        "system_prompt": (
            "You are a D&D expert. "
            "Use the provided context to answer the question.\n\n"
            "Context:\n{context}\n\nQuestion:\n{query}\n\nAnswer:"
        ),
    },

    "blocks": [
        {
            "type": "augmentation",
            "params": {
                "augmentations": ["hyde"],
                "include_original": True,
            },
        },
        {
            "type": "retriever",
            "params": {
                "top_k": 3,
            },
        },
        {
            "type": "generator",
            "params": {},
        },
    ],
}
