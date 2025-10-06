# Data Folder

## 📁 Contents

This folder should contain:
- `er_inegalites_maladies_chroniques.csv` - Main dataset

## 📥 Data Download Instructions

### Option 1: Direct Download

1. Visit the DREES data portal:
   https://data.drees.solidarites-sante.gouv.fr/explore/dataset/er_inegalites_maladies_chroniques/

2. Click on "Export" button

3. Select "CSV" format

4. Save as `er_inegalites_maladies_chroniques.csv` in this folder

### Option 2: API Download (Python Script)

```python
import requests
import pandas as pd

# API endpoint
url = "https://data.drees.solidarites-sante.gouv.fr/api/explore/v2.1/catalog/datasets/er_inegalites_maladies_chroniques/exports/csv"

# Download
response = requests.get(url)

# Save
with open('er_inegalites_maladies_chroniques.csv', 'wb') as f:
    f.write(response.content)

print("✅ Dataset downloaded successfully!")
```

### Option 3: Manual Download (Alternative Portal)

Visit: https://www.data.gouv.fr/fr/datasets/inegalites-sociales-face-aux-maladies-chroniques-er-1243/

## 📊 Dataset Information

**Name:** Social Inequalities and Chronic Diseases (ER 1243)  
**Provider:** DREES (Direction de la Recherche, des Études, de l'Évaluation et des Statistiques)  
**Published:** October 2022  
**Size:** ~100,000 records  
**Format:** CSV (UTF-8 encoding)  
**License:** Open License / Licence Ouverte (Etalab)

## 📋 Data Dictionary

### Key Columns

- `varTauxLib` - Disease name (French)
- `type` - "prevalence" or "incidence"
- `varGroupage` - Grouping variable (income, region, education, etc.)
- `valGroupage` - Value of grouping variable
- `txStandDir` - Directly standardized rate (%)
- `txStandDirBB` - Lower bound 95% CI
- `txStandDirBH` - Upper bound 95% CI

### Grouping Variables

| Variable Code | Meaning | Values |
|--------------|---------|--------|
| SEXE | Gender | 1=Male, 2=Female |
| classeAge10 | Age groups | 10-year intervals |
| FISC_REG_S | Region | Region codes (11-93) |
| FISC_NIVVIEM_E2015_S_moy_10 | Income decile | 1=Poorest, 10=Richest |
| EAR_GS_S | Socio-professional | Job categories |
| EAR_DIPLR_S | Education | Diploma levels |

## ⚠️ Important Notes

1. **Large File:** The CSV is approximately 50-100 MB
2. **Encoding:** Use UTF-8 encoding when opening
3. **Do Not Commit:** This file should NOT be committed to git (see .gitignore)
4. **Deterministic:** Same source ensures reproducibility

## 🔒 License

**License:** Open License / Licence Ouverte v2.0  
**Terms:** Free to reuse, share, and adapt with attribution  
**Attribution Required:** DREES - Ministry of Health, France

### How to Cite

```
DREES (2022). Inégalités sociales face aux maladies chroniques (ER 1243). 
Direction de la Recherche, des Études, de l'Évaluation et des Statistiques, 
Ministère de la Santé et de la Prévention.
Retrieved from https://data.drees.solidarites-sante.gouv.fr/
```

## 📞 Support

- **Data Questions:** Contact DREES via their website
- **Technical Issues:** Open an issue on the project repository
- **Dashboard Questions:** mano.mathew@efrei.fr