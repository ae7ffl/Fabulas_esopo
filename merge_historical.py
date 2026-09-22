#!/usr/bin/env python3
"""
Actualiza el campo "historical" de fabulas_completas.json con datos
históricos concretos (fechas, nombres, lugares), usando hist_updates.json.

Uso:
    python3 merge_historical.py

Requiere que los tres archivos estén en la misma carpeta:
- fabulas_completas.json  (tu archivo actual, no se sobreescribe hasta el final)
- hist_updates.json       (las nuevas versiones del campo "historical")
- este script
"""
import json

with open("fabulas_completas.json", "r", encoding="utf-8") as f:
    fabulas = json.load(f)

with open("hist_updates.json", "r", encoding="utf-8") as f:
    updates = json.load(f)

actualizadas = 0
for fabula in fabulas:
    num = str(fabula["num"])
    if num in updates:
        fabula["historical"] = updates[num]
        actualizadas += 1

with open("fabulas_completas.json", "w", encoding="utf-8") as f:
    json.dump(fabulas, f, ensure_ascii=False, indent=1)

print(f"Actualizadas {actualizadas} fábulas de {len(fabulas)}.")
