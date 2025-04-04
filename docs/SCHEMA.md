# CombatBalancer YAML Schema Reference

This document defines the structure and allowed values for all components of the CombatBalancer YAML configuration system.

---

## Combatant

```yaml
combatant:
  type: object
  properties:
    id:
      type: string
      description: Unique identifier for the combatant.
    type:
      type: string
      enum: [pc, npc]
    name:
      type: string
    character_class:
      type: string
      description: Required for PCs.
    level:
      type: integer
      description: Required for PCs.
    challenge_rating:
      type: string
      description: Required for NPCs.
    role:
      type: string
      enum: [melee, ranged, support]
    max_hp:
      type: integer
      description: Maximum hit points.
    hp:
      type: integer
    ac:
      type: integer
    position:
      type: object
      properties:
        x:
          type: integer
        y:
          type: integer
      required: [x, y]
    movement_speed:
      type: integer
      description: Movement speed in feet.
    ability_scores:
      type: object
      properties:
        str:
          type: integer
        dex:
          type: integer
        con:
          type: integer
        int:
          type: integer
        wis:
          type: integer
        cha:
          type: integer
      required: [str, dex, con, int, wis, cha]
    action_slots:
      type: object
      properties:
        action:
          type: integer
          default: 1
        bonus_action:
          type: integer
          default: 1
        reaction:
          type: integer
          default: 1
      required: [action, bonus_action, reaction]
    behavior:
      type: string
      enum: [focus_melee, focus_ranged, focus_weakest, retaliate, random]
    resources:
      type: array
      items:
        type: object
        properties:
          name:
            type: string
            description: e.g., "spell_slots_level_1" or "bardic_inspiration"
          value:
            type: integer
            description: Current amount available.
          max_value:
            type: integer
            description: Maximum possible amount.
        required: [name, value, max_value]
    ability_group:
      type: string
      description: "Identifier (ID) reference to the ability group associated with this combatant."
  required:
    - id
    - type
    - name
    - role
    - hp
    - ac
    - position
    - movement_speed
    - ability_scores
    - action_slots
    - behavior
    - resources
    - ability_group
```

---

## Abilities (Grouped)

```yaml
abilities:
  type: object
  properties:
    actions:
      type: array
      items:
        type: object
        properties:
          name:
            type: string
          type:
            type: string
            enum: [attack, heal, buff, debuff]
          amount:
            type: string   # Represents a dice expression or effect description
          resource:
            type: string   # Optional resource reference (omit if not applicable)
          scaling:
            oneOf:
              - type: string
                enum: [none]
              - type: object
                properties:
                  type:
                    type: string
                    enum: [per_slot_level]
                  additional_dice:
                    type: string       # Dice expression, e.g., "1d4"
                  threshold:
                    type: integer      # Base slot level above which scaling applies (e.g., 1 means scaling starts at 2nd level/slot)
                required: [type, additional_dice, threshold]
          range:
            type: integer
          to_hit:
            type: string
            description: "Attack roll modifier (e.g., 'd20+7'). Optional for attack actions."
          save_dc:
            type: number
            description: "Saving throw DC for the ability, if applicable (e.g., 15). Optional."
        required: [name, type, amount, scaling, range]
    bonus_actions:
      type: array
      items:
        type: object
        properties:
          name:
            type: string
          type:
            type: string
            enum: [attack, heal, buff, debuff]
          amount:
            type: string   # Dice expression or effect description
          resource:
            type: string   # Optional resource reference
          scaling:
            oneOf:
              - type: string
                enum: [none]
              - type: object
                properties:
                  type:
                    type: string
                    enum: [per_slot_level]
                  additional_dice:
                    type: string
                  threshold:
                    type: integer
                required: [type, additional_dice, threshold]
          range:
            type: integer
          to_hit:
            type: string
            description: "Attack roll modifier for bonus actions (e.g., 'd20+7'). Optional."
          save_dc:
            type: number
            description: "Saving throw DC for bonus actions, if applicable. Optional."
        required: [name, type, amount, scaling, range]
    reactions:
      type: array
      items:
        type: object
        properties:
          name:
            type: string
          type:
            type: string
            enum: [reaction_effect]
          trigger:
            type: string   # A description or identifier for the trigger condition
          effect:
            type: string   # A description or identifier for the reaction effect
          resource:
            type: string   # Optional resource reference
          range:
            type: integer
          to_hit:
            type: string
            description: "Attack roll modifier for reactions, if applicable. Optional."
          save_dc:
            type: number
            description: "Saving throw DC for reactions, if applicable. Optional."
        required: [name, type, trigger, effect, range]
    passives:
      type: array
      items:
        type: object
        properties:
          name:
            type: string
          trigger:
            type: string
            description: "Optional condition or timing that triggers the passive, e.g., 'start of turn', 'end of turn', 'on attack with advantage'"
          effect:
            type: string
            description: "Description or dice expression for the passive's effect."
          frequency:
            type: string
            description: "How often the passive can trigger, e.g., 'once per turn', 'always active'"
        required: [name, effect]
    
  required: [actions, bonus_actions, reactions]
```

## Terrain

```yaml
terrain:
  type: object
  properties:
    dimensions:
      type: object
      properties:
        width:
          type: integer
          description: "The width of the grid (number of columns)."
        height:
          type: integer
          description: "The height of the grid (number of rows)."
      required: [width, height]
    cells:
      type: array
      description: "List of cells with non-clear terrain. Any cell not listed is assumed to be clear."
      items:
        type: object
        properties:
          x:
            type: integer
            description: "The x-offset (column index) of the cell."
          y:
            type: integer
            description: "The y-offset (row index) of the cell."
          type:
            oneOf:
              - type: string
                enum:
                  - clear
                  - half_cover
                  - three_quarter_cover
                  - difficult
                  - half_cover+difficult
                  - three_quarter_cover+difficult
              - type: object
                properties:
                  cover:
                    type: string
                    enum: ["clear", "half_cover", "three_quarter_cover"]
                  difficult:
                    type: boolean
                required: ["cover", "difficult"]
        required:
          - x
          - y
  required:
    - dimensions
```

---

## Party

```yaml
party:
  type: object
  properties:
    name:
      type: string
      description: "The name or identifier for the party."
    members:
      type: array
      description: "A list of combatant IDs representing party members."
      items:
        type: string
  required:
    - name
    - members
```

---

## Encounter

```yaml
encounter:
  type: object
  properties:
    party:
      type: string
      description: "Identifier (name or ID) of the friendly party."
    enemies:
      type: string
      description: "Identifier (name or ID) of the enemy party."
    difficulty_target:
      type: string
      enum: [easy, balanced, deadly]
      description: "The intended difficulty level for the encounter."
    iterations:
      type: integer
      description: "Number of simulation iterations to run."
    max_rounds:
      type: integer
      description: "Maximum number of rounds per simulation."
  required:
    - party
    - enemies
    - difficulty_target
    - iterations
    - max_rounds
```