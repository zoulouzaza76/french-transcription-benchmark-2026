# Benchmarks Officiels de Précision des IA de Transcription en Français (2026 — `v1.1.0`) — Corpus Canal-U & 60 Preuves PDF

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24215193.svg)](https://doi.org/10.5281/zenodo.24215193)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Format: Frictionless Data Package](https://img.shields.io/badge/Standard-Frictionless_Data_Package-0f172a.svg)](./datapackage.json)
[![Preuves PDF: 60 Rapports Word](https://img.shields.io/badge/Preuves_V%C3%A9rifiables-60_PDF_Word-d97706.svg)](https://lescribeaudio.com/benchmarks-precision-transcription-ia-francais)

Jeu de données ouvert (`CSV`, `JSON`, `datapackage.json` compatible **data.gouv.fr** / **OpenAIRE** et `.zenodo.json` compatible **Zenodo / DataCite**) documentant l'évaluation comparative de **11 solutions de reconnaissance vocale (ASR) et de transcription automatique** sur de la parole francophone spontanée, académique et professionnelle, appuyée par **60 rapports PDF générés mécaniquement par l'outil `Révision > Comparer` de Microsoft Word**.

- **DOI officiel CERN / Zenodo (`v1.1.0`)** : [https://doi.org/10.5281/zenodo.24215193](https://doi.org/10.5281/zenodo.24215193) *(v1.0.0 : `10.5281/zenodo.24087383` — DOI conceptuel toutes versions : `10.5281/zenodo.24087382`)*
- **Page canonique et consultation directe des 60 PDF** : [https://lescribeaudio.com/benchmarks-precision-transcription-ia-francais](https://lescribeaudio.com/benchmarks-precision-transcription-ia-francais)
- **Éditeur du jeu de données** : **LE SCRIBE AUDIO** (Le Rheu / Rennes, France — `info@lescribeaudio.com` — `+33 9 61 44 46 64`)
- **Licence** : Creative Commons Attribution 4.0 International (`CC-BY-4.0`)

---

## Academic Abstract (English)

**Title:** *Open Benchmark of French Automatic Speech Recognition and AI Transcription Systems (2026): Real-World Editing Effort Measured via Microsoft Word Track Changes Across 60 Verifiable PDF Reports.*

**Abstract:** Commercial speech-to-text benchmarks routinely rely on normalized Word Error Rate (WER) computed on clean, studio-read English utterances stripped of punctuation, capitalization, and silent grammatical inflections. However, spoken French exhibits extensive homophony, silent plural and past-participle agreement markers (*« l'auteur / la hauteur »*, *« émaillage / et maillage »*, *« les élus ont vu / l'élu a vu »*), and domain-specific acronyms that purely acoustic single-pass models frequently misrender. To provide researchers (CNRS, French universities), public institutions, parliamentary and union minute-writers (CSE), and legal professionals with an auditable measure of real human post-editing effort, we evaluate **11 transcription tools** (*Le Scribe Audio*, *Gladia*, *noScribe / OpenAI Whisper Large v3*, *Happy Scribe*, *TurboScribe*, *MacWhisper*, *ElevenLabs Scribe v2*, *Sonix*, *Speechmatics Ursa ASR*, *AmberScript*, and *Microsoft Word 365*) on authentic French recordings from the **Canal-U** higher-education audiovisual repository (medical neuroscience, CNRS/CEA materials chemistry, University of Tours/OFB hydrobiology, and a 76-minute CNRS/C2RMF heritage science interview) alongside three professional acoustic archetypes (interview, multi-speaker meeting, conference). Each raw machine output is mechanically diffed against a human-verified reference transcript using **Microsoft Word (`Review > Compare`)**, counting every required insertion and deletion and exporting the complete redline proof as an open-access PDF. Across the three Canal-U scientific corpora, sequential two-pass multimodal inference (*Le Scribe Audio*, via Google Cloud Vertex AI in Europe) averages **72.0 Word revisions**, compared with **147.7 to 257.0 revisions** (`2.05×` to `3.57×` more edits) for single-pass Whisper and proprietary ASR engines. On the 76-minute CNRS/C2RMF interview, two-pass chunked inference yields **47 revisions** (`RTF 0.12`) versus **123 revisions** for local Whisper Large (*noScribe v0.8*, `RTF 0.55`) and **151 revisions** for *Microsoft Word 365* (`RTF 0.03`). In practical editorial workflows where manual transcription from scratch requires **4 to 7 hours of human labor per audio hour**, starting from a two-pass pre-transcription reduces full ear-checked proofreading and formatting to **2 to 3 hours per audio hour**—cutting total drafting time in half (`50%` reduction).

---

## 1. Protocole Scientifique & Reproduction sous Microsoft Word

Notre protocole repose sur **4 règles strictement reproductibles** :

1. **Sources audio publiques francophones à forte densité terminologique** : Conférences et entretiens extraits de la vidéothèque numérique de l'enseignement supérieur **Canal-U** (neurosciences médicales, physique-chimie des matériaux CNRS/CEA, écologie OFB/Université de Tours, sciences du patrimoine CNRS/C2RMF) complétés par trois situations acoustiques types (*Entretien individuel*, *Réunion multi-locuteurs*, *Conférence en salle*).
2. **Vérité terrain (*Gold Standard*) établie par réécoute humaine intégrale au casque** : Chaque enregistrement a été intégralement vérifié et corrigé à l'oreille par un relecteur francophone.
3. **Comptage mécanique par `Révision > Comparer` dans Microsoft Word** : Comparaison au niveau du mot (casse, accords, ponctuation inclus) entre la sortie brute non retouchée du logiciel testé et la vérité terrain humaine, et export du document annoté en PDF.
4. **Publication ouverte des 60 rapports PDF & du script Python d'évaluation reproductible (`scripts/evaluate_benchmark_reproducibility.py`)** : Chaque score publié dans les fichiers CSV et JSON pointe directement vers son rapport PDF complet hébergé en accès libre et peut être vérifié localement via `python3 scripts/evaluate_benchmark_reproducibility.py --audit`.

### 1.1 Configurations et Hyperparamètres d'Inférence (Whisper & Moteurs Évalués — `v1.1.0`)

- **Implémentations locales d'OpenAI Whisper (`noScribe v0.8`, `MacWhisper`)** : Modèle `Whisper large-v3` (`float16`), langue forcée `fr`, `beam_size = 5`, température `0.0` avec repli progressif, sans `initial_prompt`, filtrage VAD Silero et diarisation `pyannote.audio 3.1`.
- **Plateformes Cloud basées sur Whisper (`TurboScribe`)** : Mode de précision maximale (*« Baleine / Whisper Large-v3 »*), langue `fr`, détection des locuteurs activée, export brut sans post-édition.
- **Moteurs ASR propriétaires (`Gladia`, `Happy Scribe`, `ElevenLabs Scribe v2`, `Sonix`, `Speechmatics Ursa ASR`, `AmberScript`, `Microsoft Word 365`)** : Modèle standard `fr-FR`, ponctuation automatique et diarisation activées, sortie brute.
- **Architecture multimodale en 2 passes (`Le Scribe Audio`)** : Segments de `20 minutes` avec recouvrement de `5 secondes`, inférence séquentielle en 2 passes via **Google Cloud Vertex AI (en région Europe)** en mode *Mot à mot (Verbatim)* avec diarisation native, sans glossaire personnalisé.

---

## 2. Résultats Principaux

### 2.1 Benchmark Principal : 10 Logiciels sur 3 Corpus Scientifiques Canal-U (30 PDF)

Fichier source : [`dataset/benchmark_10_moteurs_canalu_2026.csv`](./dataset/benchmark_10_moteurs_canalu_2026.csv)

| Rang | Logiciel évalué | Architecture sous-jacente | Éch. 1 (ARAPI) | Éch. 2 (CNRS/CEA) | Éch. 3 (Univ. Tours) | Moyenne des révisions | Ratio vs 1er | Preuves PDF |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | **Le Scribe Audio** | IA multimodale 2 passes (Google Cloud Vertex AI Europe) | **92** | **52** | **72** | **72,0** | **1,00×** | [Éch.1](https://lescribeaudio.com/docs/benchmark/lescribe-sample1.pdf) · [Éch.2](https://lescribeaudio.com/docs/benchmark/lescribe-sample2.pdf) · [Éch.3](https://lescribeaudio.com/docs/benchmark/lescribe-sample3.pdf) |
| **2** | **Gladia** | Moteur ASR propriétaire | 170 | 157 | 116 | **147,7** | 2,05× | [Éch.1](https://lescribeaudio.com/docs/benchmark/gladia-sample1.pdf) · [Éch.2](https://lescribeaudio.com/docs/benchmark/gladia-sample2.pdf) · [Éch.3](https://lescribeaudio.com/docs/benchmark/gladia-sample3.pdf) |
| **3** | **noScribe** | OpenAI Whisper Large v3 | 158 | 148 | 143 | **149,7** | 2,08× | [Éch.1](https://lescribeaudio.com/docs/benchmark/noscribe-sample1.pdf) · [Éch.2](https://lescribeaudio.com/docs/benchmark/noscribe-sample2.pdf) · [Éch.3](https://lescribeaudio.com/docs/benchmark/noscribe-sample3.pdf) |
| **4** | **Happy Scribe** | Moteur ASR propriétaire | 184 | 149 | 135 | **156,0** | 2,17× | [Éch.1](https://lescribeaudio.com/docs/benchmark/happyscribe-sample1.pdf) · [Éch.2](https://lescribeaudio.com/docs/benchmark/happyscribe-sample2.pdf) · [Éch.3](https://lescribeaudio.com/docs/benchmark/happyscribe-sample3.pdf) |
| **5** | **TurboScribe** | OpenAI Whisper Large v3 | 166 | 159 | 145 | **156,7** | 2,18× | [Éch.1](https://lescribeaudio.com/docs/benchmark/turboscribe-sample1.pdf) · [Éch.2](https://lescribeaudio.com/docs/benchmark/turboscribe-sample2.pdf) · [Éch.3](https://lescribeaudio.com/docs/benchmark/turboscribe-sample3.pdf) |
| **6** | **MacWhisper** | Whisper Large v3 (Local) | 192 | 199 | 132 | **174,3** | 2,42× | [Éch.1](https://lescribeaudio.com/docs/benchmark/macwhisper-sample1.pdf) · [Éch.2](https://lescribeaudio.com/docs/benchmark/macwhisper-sample2.pdf) · [Éch.3](https://lescribeaudio.com/docs/benchmark/macwhisper-sample3.pdf) |
| **7** | **ElevenLabs** | Scribe v2 | 186 | 147 | 205 | **179,3** | 2,49× | [Éch.1](https://lescribeaudio.com/docs/benchmark/elevenlabs-sample1.pdf) · [Éch.2](https://lescribeaudio.com/docs/benchmark/elevenlabs-sample2.pdf) · [Éch.3](https://lescribeaudio.com/docs/benchmark/elevenlabs-sample3.pdf) |
| **8** | **Sonix** | Moteur ASR propriétaire | 220 | 226 | 205 | **217,0** | 3,01× | [Éch.1](https://lescribeaudio.com/docs/benchmark/sonix-sample1.pdf) · [Éch.2](https://lescribeaudio.com/docs/benchmark/sonix-sample2.pdf) · [Éch.3](https://lescribeaudio.com/docs/benchmark/sonix-sample3.pdf) |
| **9** | **Speechmatics** | Ursa ASR | 235 | 214 | 228 | **225,7** | 3,13× | [Éch.1](https://lescribeaudio.com/docs/benchmark/speechmatics-sample1.pdf) · [Éch.2](https://lescribeaudio.com/docs/benchmark/speechmatics-sample2.pdf) · [Éch.3](https://lescribeaudio.com/docs/benchmark/speechmatics-sample3.pdf) |
| **10** | **AmberScript** | Moteur ASR propriétaire | 261 | 262 | 248 | **257,0** | 3,57× | [Éch.1](https://lescribeaudio.com/docs/benchmark/amberscript-sample1.pdf) · [Éch.2](https://lescribeaudio.com/docs/benchmark/amberscript-sample2.pdf) · [Éch.3](https://lescribeaudio.com/docs/benchmark/amberscript-sample3.pdf) |

### 2.2 Étude de Cas Longue Durée : Entretien CNRS / C2RMF de 1 h 16 min (3 PDF)

Fichier source : [`dataset/benchmark_longue_duree_cnrs_c2rmf_1h16.csv`](./dataset/benchmark_longue_duree_cnrs_c2rmf_1h16.csv)

| Rang | Solution évaluée | Temps de calcul (RTF) | Révisions Word (Détail) | Observations linguistiques | Preuve PDF |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **1** | **Le Scribe Audio** *(2 passes, segments 20 min + overlap 5 s)* | **8 min 55 s** (`RTF 0,12`) | **47** *(15 ins. / 32 suppr.)* | Restitue sans faute *C2RMF*, *émaillage sur métaux*, *matières vitreuses* et les accords de participes passés. | [PDF (47 rév.)](https://lescribeaudio.com/docs/benchmark/comparatif-entretien-cnrs-le-scribe-audio-47-revisions.pdf) |
| **2** | **noScribe v0.8** *(Whisper Large local + Pyannote)* | **41 min 41 s** (`RTF 0,55`) | **123** *(58 ins. / 65 suppr.)* | Hésitations de ponctuation, erreurs d'accords pluriels muets et sigles phonétisés. | [PDF (123 rév.)](https://lescribeaudio.com/docs/benchmark/comparatif-entretien-cnrs-noscribe-123-revisions.pdf) |
| **3** | **Microsoft Word 365** *(Azure Speech-to-Text intégré)* | **2 min 18 s** (`RTF 0,03`) | **151** *(84 ins. / 67 suppr.)* | Confusions d'homophones (*« et maillage »* pour *émaillage*) et découpage haché des tours de parole. | [PDF (151 rév.)](https://lescribeaudio.com/docs/benchmark/comparatif-entretien-cnrs-microsoft-word-151-revisions.pdf) |

### 2.3 Impact Réel sur le Temps de Relecture Humaine

- **Frappe manuelle complète à partir de zéro** : **4 à 7 heures de travail au casque** par heure d'audio (`4 à 6 h` pour un rédacteur professionnel expérimenté, `5 à 7 h` pour un non-professionnel).
- **Réécoute intégrale et mise en forme finale après pré-transcription 2 passes (Le Scribe Audio)** : **2 à 3 heures de travail par heure d'audio** directement dans le fichier Word (`.docx`) standard **100 % modifiable**, soit un **temps de rédaction divisé par 2** (gain de 50 %).
- **Option de relecture humaine intégrale clé en main** : **60 € HT / heure d'enregistrement** (`1,00 € HT / min`) assurée par **deux transcripteurs successifs** (double réécoute croisée).

---

## 3. Structure du Dépôt

```text
french-transcription-benchmark-2026/
├── dataset/
│   ├── benchmark_10_moteurs_canalu_2026.csv        # Tableau principal (10 logiciels × 3 extraits Canal-U = 30 PDF)
│   ├── benchmark_longue_duree_cnrs_c2rmf_1h16.csv  # Étude longue durée 1h16 CNRS/C2RMF (3 systèmes = 3 PDF)
│   ├── benchmark_situations_terrain_2026.csv       # Inventaire par situation acoustique (9 logiciels × 3 = 27 PDF)
│   └── benchmark_complet_2026.json                 # Consolidation JSON complète + métadonnées méthodologiques (v1.1.0)
├── scripts/
│   └── evaluate_benchmark_reproducibility.py       # Script Python autonome reproductible (WER/CER jiwer + Révisions Word)
├── datapackage.json                                # Descripteur Frictionless Data (data.gouv.fr / OpenAIRE)
├── CITATION.cff                                    # Fichier de citation académique standard (CFF 1.2.0)
├── LICENSE                                         # Licence ouverte Creative Commons Attribution 4.0 (CC-BY-4.0)
└── README.md                                       # Documentation méthodologique FR/EN
```

---

## 4. Architecture & Protection des Données (RGPD / PGD Recherche)

- **Stockage des fichiers en France chez OVHcloud** (chiffrement **AES-256** au repos et TLS 1.3 en transit) avec **suppression immédiate et définitive en 1 clic** par l'utilisateur.
- **Inférence via Google Cloud Vertex AI (en région Europe)** sans conservation ni entraînement sur les données (*Zero Data Retention*).
- **Renommage / codage global des étiquettes d'intervenants (diarisation)** dans le lecteur interactif (ex. `Enquêteur`, `Enquêté P1`, `M. Martin`, `Mme Dubois`) avant l'export du document Word (`.docx`) 100 % modifiable, complété à la demande par une **synthèse exécutive** suivie d'un **développement chrono-thématique**.

---

## 5. Ressources Complémentaires & Citation

- **Hub des 60 rapports PDF & protocole complet** : [https://lescribeaudio.com/benchmarks-precision-transcription-ia-francais](https://lescribeaudio.com/benchmarks-precision-transcription-ia-francais)
- **Comparatif et tutoriel des logiciels de transcription automatique** : [https://lescribeaudio.com/logiciels-transcription-automatique-tutoriel-comparatif](https://lescribeaudio.com/logiciels-transcription-automatique-tutoriel-comparatif)
- **Guide méthodologique pour l'enquête qualitative en SHS** : [https://lescribeaudio.com/transcription-audio-enquete-qualitative](https://lescribeaudio.com/transcription-audio-enquete-qualitative)
- **Analyse technique OpenAI Whisper Large v3 vs architecture 2 passes** : [https://lescribeaudio.com/comparatif-whisper-le-scribe-audio](https://lescribeaudio.com/comparatif-whisper-le-scribe-audio)

### Référence bibliographique recommandée

> LE SCRIBE AUDIO (2026). *Benchmarks Officiels de Précision des IA de Transcription en Français (2026) — Corpus Canal-U & 60 Rapports de Suivi des Modifications Microsoft Word* (Version 1.1.0) [Jeu de données]. Zenodo / CERN. Licence CC-BY-4.0. https://doi.org/10.5281/zenodo.24215193
