# BINDINC API uitlezen en NDJSON omzetten naar CSV

1. Uitpakken in apart mapje.
2. Eenmalig setupenv.bat uitvoeren. (Maakt een virtual environment aan en installeert de benodigde packages.)
3. API key in een bestand zetten (`secure\bindinc_api_key`).
4. Eigenlijke code uitvoeren:
    - **import_binge.py**: om data te importeren
    - **ndjson_to_csv.py**: om NDJSON te converteren naar CSV
    - **split_csv.py**: om CVS in kleinere delen te splitsen
    - **settings.py**: alle instellingen

Paar opmerkingen:

- Voor het testen heb ik het maximumaantal iteraties op 1 gezet. Dan krijg je dus maar een sample van de data. 
- Niet alle data wordt naar CSV omgezet, alleen de velden die zijn gespecificeerd in export_fields. Bij geneste velden moet je een punt gebruiken.
- De waarden van velden met meer dan een waarde worden samengevoegd tot één. Scheidingsteken kun je opgeven.
- CSV-outputformaat is configureerbaar. De instellingen worden rechtstreeks doorgegeven aan de standaard CSV-writer van Python; kan dus eventueel worden aangevuld met andere opties (zie documentatie csv module).
- API-key staat in een apart bestand. Dat is wat veiliger en netter.

Het omzetten naar CSV gebeurt recursief. Het is niet grondig getest; is dus nog wat kwetsbaar.

# Release notes

### 19 december 2022
- Het is nu mogelijk om in `settings.export_fields` een filter toe te voegen voor nodes met lijsten. 
  Voorbeeld:

  ```python
  export_fields : [...
    'identifiers.id[source="Binge",level="program"]',
    ...
  ]
  ```
  Exporteer `identifiers` > `id` alleen als `source` gelijk is aan `Binge` en `level` gelijk aan `program`. 
- Bug fixes:
  - Check expliciet of CSV-bestand bestaat voor het al of niet toevoegen van rijkoppen (in plaats van afhankelijk van `csv_options.file_mode`).
  - Cast te exporteren waarden altijd expliciet naar string.