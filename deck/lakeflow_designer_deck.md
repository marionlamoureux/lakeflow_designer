---
marp: true
theme: default
paginate: true
backgroundColor: #fff
style: |
  section {
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
  }
  h1 {
    color: #FF3621;
  }
  h2 {
    color: #1B3139;
  }
  table {
    font-size: 0.75em;
  }
---

<!-- _class: lead -->

# Lakeflow Designer
## Preparation de donnees visuelle, gouvernee, scalable
### No-code sur Databricks -- Public Preview

---

# Agenda

1. Positionnement : pourquoi un outil no-code gouverne ?
2. Qu'est-ce que Lakeflow Designer ?
3. Capacites principales -- deep dive
4. Demo live : scenario OTC / reconciliation
5. Mapping des outils vs alternatives
6. Gouvernance & lineage
7. Prochaines etapes

---

# Le besoin

- Des **centaines d'applications ad-hoc** a industrialiser
- Des fichiers Excel envoyes par email, des workflows desktop non traces
- Des regulateurs qui demandent **tracabilite et lineage** de bout en bout
- Des utilisateurs **metier, pas IT** -- le no-code est un imperatif

> L'enjeu n'est pas de changer d'outil. C'est d'industrialiser sans perdre l'agilite metier.

---

# Lakeflow Designer

Un **canvas visuel drag-and-drop** integre a Databricks.

- Pipeline de donnees visuel -- **zero code requis**
- Chaque transformation **genere du code** (auditable, reproductible)
- Execution **serverless** (pas d'infra a gerer)
- Integration native **Unity Catalog** (gouvernance des le depart)
- **Genie Code** : assistant IA pour generer des transformations en langage naturel
- Publication, scheduling, orchestration dans Databricks Jobs

**Statut :** Public Preview (23 avril 2026)

---

# Les operateurs

| Operateur | Fonction | Equivalent usuel |
|---|---|---|
| **Source** | Tables UC, volumes, CSV/Excel (drag-drop), Google Drive, SharePoint | Input Data |
| **Filter** | Filtrage graphique par conditions | Filter |
| **Transform** | Selection, renommage, colonnes calculees | Select + Formula |
| **Join** | Inner, Left, Right, Full | Join |
| **Combine** | Union, Intersect, Except | Union |
| **Aggregate** | Groupement + SUM, AVG, COUNT, MEDIAN, STDDEV... | Summarize |
| **Pivot** | Lignes vers Colonnes et Colonnes vers Lignes | Cross Tab + Transpose |
| **Sort / Limit** | Tri et limitation | Sort + Sample |
| **SQL** | Requetes SELECT custom | SQL custom |
| **Python** | Code PySpark (distribue) | Python tool |
| **Output** | Ecriture vers table Unity Catalog | Output |

---

# Point cle : l'ingestion Excel

**Le pattern qui change tout :**

1. L'utilisateur metier a un fichier Excel d'ajustements reglementaires
2. Il le **glisse-depose directement sur le canvas**
3. Lakeflow Designer cree automatiquement un operateur Source
4. Le fichier est integre dans un **pipeline gouverne** avec lineage complet

> Plus besoin d'envoyer des Excel par email. Le fichier ad-hoc entre dans le meme pipeline que les donnees structurees, avec tracabilite complete.

**Sources supportees :** Tables UC, Volumes, CSV, Excel, Google Drive, SharePoint, + Lakeflow Connect (SaaS : Salesforce, Workday, etc.)

---

# Genie Code -- Assistant IA

**Langage naturel vers transformation -- le differenciateur**

- Decrire ce qu'on veut en francais ou en anglais
- Genie genere l'expression Spark SQL / PySpark
- Contexte-aware : connait le schema, les colonnes, les types
- Upload d'images (ex: screenshot d'une formule existante)
- Historique interactif pour affiner iterativement

**Exemples :**
- *"Classifier le risque : High si MTM > 1M, Medium entre 100k et 1M, Low sinon"*
- *"Calculer le nombre de jours avant maturite"*
- *"Detecter les trades sans settlement (break)"*

**Les alternatives n'ont pas d'equivalent.**

---

# Data Profiling & Preview

**Feedback instantane a chaque etape :**

- **Sample** (1 000 lignes) pour iterer rapidement
- **Full dataset** pour validation
- **Profiling** : distributions, stats, comptage de nulls
- **Comparaison** entree/sortie
- Cliquer sur n'importe quel operateur pour voir son resultat

> Pas besoin de lancer le workflow complet. Previews instantanes a chaque etape.

---

# Demo live

### Scenario : Reconciliation OTC & Reporting Reglementaire

```
  otc_trades (UC)  ----+
                       +--> Join --> Filter --> Transform --> Aggregate --> Output (UC)
  counterparties (UC) -+                          |
                                                  +-- Join avec Excel adjustments
  settlements (UC)  -------> Join (Left) ------+
                                               +--> Break detection --> Output (UC)
  adjustments.xlsx  -------> Drag & drop ------+
```

**4 sources dont 1 Excel** | Enrichissement | Detection de breaks | Rapport de synthese | Lineage

---

# Gouvernance & Architecture

### Unity Catalog natif
- Sources et outputs = assets UC gouvernes
- **Lineage colonne par colonne** trace automatiquement
- Controles d'acces (GRANT/REVOKE) appliques aux pipelines visuels
- **Tracabilite complete** pour les auditeurs (y compris le fichier Excel)

### Code genere
- Chaque transformation visuelle produit du code
- Auditable, reproductible, versionnable
- Graduation path : export vers notebooks pour les cas avances

### Serverless
- Zero gestion de cluster
- Paiement a l'usage
- Demarrage instantane, auto-scale

---

# Mapping des outils

| Dimension | Desktop classique | Lakeflow Designer |
|---|---|---|
| **Execution** | Machine unique | Distribue (Spark serverless) |
| **Gouvernance** | Externe / manuelle | Unity Catalog natif |
| **Assistance IA** | Aucune | Genie Code (NL vers code) |
| **Scheduling** | Serveur dedie ($$$) | Integre + Databricks Jobs |
| **Collaboration** | Galerie / partage fichiers | Workspace partage + Git |
| **Sources** | Drivers ODBC/fichiers | UC tables, volumes, SaaS connectors |
| **Lineage** | Aucun | Automatique, colonne par colonne |
| **Scalabilite** | GB | TB+ |
| **Modele de cout** | Licence par poste | Consommation |
| **Export code** | Limite | Spark SQL / PySpark complet |

---

# Ce que Lakeflow Designer ne fait pas (encore)

Transparence totale :

| Capacite | Statut | Alternative sur Databricks |
|---|---|---|
| Spatial analytics | Pas dans Designer | H3 / Mosaic en notebooks |
| ML / Predictif dans le canvas | Pas dans Designer | AutoML / MosaicAI |
| Generation de rapports PDF | Pas dans Designer | AI/BI Dashboards |
| Macros / workflows reutilisables | Pas encore | Notebooks parametres |
| Mode offline desktop | Cloud uniquement | -- |
| Connecteurs specifiques (SAP...) | Verifier Lakeflow Connect | -- |

---

# Demo

### Deroulage prevu

| Etape | Duree | Contenu |
|---|---|---|
| Cadrage | ~10' | Positionnement no-code + gouvernance |
| Demo live | ~40' | Scenario OTC fil rouge + interactions |
| Mapping outils | ~15' | Equivalences, gaps (honnete) |
| Discussion + next | reste | Leurs workflows, atelier 2 |

---

# Prochaines etapes

1. **Identifier les 10 workflows prioritaires** a migrer
2. **Atelier 2 approfondi** : tester avec les donnees reelles du client
3. **Pilot** : un workflow de production migre end-to-end
4. **Formation equipe** : Genie Code pour accelerer l'adoption
5. **Review gouvernance** : lineage UC vs audit actuel

### Ressources
- [Documentation Lakeflow Designer](https://docs.databricks.com/aws/en/designer/what-is-lakeflow-designer)
- [Lab repository](https://github.com/marionlamoureux/lakeflow_designer)

---

<!-- _class: lead -->

# Merci
## Questions ?
