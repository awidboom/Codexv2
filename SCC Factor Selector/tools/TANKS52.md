`tools/tanks52_workbook.py` supports two workflows:

- Generate a human-editable fillable workbook, then convert it to a TANKS import workbook.
- Build a TANKS import workbook directly from JSON.

Examples:

```powershell
python tools/tanks52_workbook.py --fillable-template-out tools\tanks52_fillable_template.xlsx
python tools/tanks52_workbook.py --from-fillable tools\tanks52_fillable_template.xlsx tools\tanks52_import.xlsx

python tools/tanks52_workbook.py --template-out tools\my_tank.json
python tools/tanks52_workbook.py tools\my_tank.json tools\my_tank.xlsx
```

The generated import workbook matches the current cloud app export/import shape:

- `TankData`
- `CustomOrganicLiquids`
- `CustomPetroleumLiquids`
- `CustomMixtures`
- `CustomMeteorologicalData`

The fillable workbook includes these sheets:

- `Instructions`
- `Tanks`
- `MonthlyContents`
- `CustomMeteorologicalData`
- `CustomOrganicLiquids`
- `CustomMixtures`
- `CustomPetroleumLiquids`
- `CustomPetroleumComponents`
- `Reference`

Each import `TankData` row contains these JSON-stringified columns:

- `tankType`
- `tankIdentification`
- `location`
- `tankChar`
- `tankFit`
- `tankContents`
- `tanSolAbs`
- `petChem`
- `petDist`

The converter resolves:

- AP-42 meteorological locations
- Custom meteorological locations from the fillable workbook
- Solar absorptance from shell/roof color and condition
- AP-42 organic and petroleum liquids
- Custom organic liquids, mixtures, and petroleum liquids from the fillable workbook

This helper is for import/export compatibility. It does not reproduce all EPA UI validation behavior or run the loss calculations itself.
