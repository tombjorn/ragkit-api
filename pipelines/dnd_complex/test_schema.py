SCHEMA = {
  "name": "dnd",
  "config": {
    "collection_name": "dnd",
    "system_prompt": "You are an expert D&D Dungeon Master.\n\nContext:\n{context}\n\nQuestion:\n{query}\n\nAnswer:"
  },
  "blocks": [
    {
      "type": "switch",
      "router": {
        "type": "regex",
        "rules": [
          {
            "pattern": "\\b(stat|AC|HP|damage|initiative|attack|strength|dexterity|constitution|saving throw)\\b",
            "route": "stat"
          },
          { "default": "lore" }
        ]
      },
      "routes": {
        "lore": {
          "name": "lore",
          "config": {
            "collection_name": "dnd",
            "system_prompt": None
          },
          "blocks": [
            {
              "type": "augmentation",
              "params": {
                "augmentations": ["least_to_most"],
                "include_original": True
              }
            },
            { "type": "retriever", "params": { "top_k": 5 } },
            { "type": "ranker" },
            { "type": "truncate", "params": { "top_k": 3 } },
            { "type": "generator" }
          ]
        },
        "stat": {
          "name": "stat",
          "config": {
            "collection_name": "dnd",
            "system_prompt": "You are a D&D rules expert. Present results as markdown tables."
          },
          "blocks": [
            {
              "type": "augmentation",
              "params": { "augmentations": [], "include_original": True }
            },
            {
              "type": "retriever",
              "params": {
                "top_k": 5,
                "metatag": { "source": "5e" }
              }
            },
            { "type": "truncate", "params": { "top_k": 3 } },
            { "type": "generator" }
          ]
        }
      }
    }
  ]
}
