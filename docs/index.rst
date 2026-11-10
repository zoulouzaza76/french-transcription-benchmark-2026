=========================================================================================================
Le Scribe Audio — Documentation Technique, Benchmarks ASR Francophones 2026 & Intégrations Open-Source
=========================================================================================================

Bienvenue sur la documentation technique et scientifique ouverte de `Le Scribe Audio <https://lescribeaudio.com>`_, plateforme française de transcription audio et vidéo en texte par Intelligence Artificielle multimodale en 2 passes et service de relecture humaine professionnelle.

* **Site officiel :** `https://lescribeaudio.com <https://lescribeaudio.com>`_
* **Étude Benchmark ASR Francophone 2026 :** `https://lescribeaudio.com/benchmarks-precision-transcription-ia-francais <https://lescribeaudio.com/benchmarks-precision-transcription-ia-francais>`_
* **Baromètre & Référentiel Juridique PV de CSE & AI Act 2026 :** `https://lescribeaudio.com/barometre-referentiel-pv-cse-enregistrement-ai-act-2026 <https://lescribeaudio.com/barometre-referentiel-pv-cse-enregistrement-ai-act-2026>`_
* **Serveur MCP Officiel :** `https://lescribeaudio.com/integrations-mcp <https://lescribeaudio.com/integrations-mcp>`_
* **Outils Audio & Sous-Titres Gratuits :** `https://lescribeaudio.com/outils <https://lescribeaudio.com/outils>`_

.. contents:: Sommaire de la documentation
   :depth: 2
   :local:

1. Identifiants Scientifiques Permanents (DOI Harvard Dataverse, CERN / Zenodo & OSF)
=====================================================================================

Nos protocoles expérimentaux, jeux de données d'évaluation (WER, DER, révisions Microsoft Word) et référentiels juridiques sont publiés sous licence ouverte ``CC-BY-4.0`` :

* **Harvard Dataverse Collection :** `https://dataverse.harvard.edu/dataverse/lescribeaudio <https://dataverse.harvard.edu/dataverse/lescribeaudio>`_
* **DOI Harvard Dataverse (Benchmark ASR Francophone) :** `doi:10.7910/DVN/EKCBKM <https://doi.org/10.7910/DVN/EKCBKM>`_
* **DOI Center for Open Science — OSF (Benchmark ASR) :** `doi:10.17605/OSF.IO/HYZXD <https://doi.org/10.17605/OSF.IO/HYZXD>`_ (`Projet OSF hyzxd <https://osf.io/hyzxd/>`_)
* **DOI Center for Open Science — OSF (Baromètre PV de CSE & AI Act 2026) :** `doi:10.17605/OSF.IO/VP7EM <https://doi.org/10.17605/OSF.IO/VP7EM>`_ (`Projet OSF vp7em <https://osf.io/vp7em/>`_)
* **DOI CERN / Zenodo (Benchmark ASR 10 logiciels) :** `doi:10.5281/zenodo.24087383 <https://doi.org/10.5281/zenodo.24087383>`_
* **DOI CERN / Zenodo (Librairie srt-vtt-cleaner-fr) :** `doi:10.5281/zenodo.24087394 <https://doi.org/10.5281/zenodo.24087394>`_
* **DOI CERN / Zenodo (Serveur MCP lescribeaudio-mcp) :** `doi:10.5281/zenodo.24092283 <https://doi.org/10.5281/zenodo.24092283>`_
* **DOI CERN / Zenodo (Baromètre PV de CSE 2026) :** `doi:10.5281/zenodo.24092285 <https://doi.org/10.5281/zenodo.24092285>`_
* **Identifiant chercheur ORCID :** `0009-0005-9574-5236 <https://orcid.org/0009-0005-9574-5236>`_

2. Architecture Multimodale en 2 Passes & Temps Réaliste de Relecture Humaine
=============================================================================

Pourquoi une architecture en 2 passes ?
---------------------------------------

Les pipelines ASR mono-passe (tels que Whisper *large-v3* brut) découpent l'audio par fenêtres de 30 secondes sans mémoire globale de la séance. Sur des réunions francophones de 1 h à 4 h (`Comité Social et Économique — CSE <https://lescribeaudio.com/transcription-cse>`_, `Conseil Municipal <https://lescribeaudio.com/compte-rendu-conseil-municipal>`_, `Entretien de recherche qualitative SHS / CNRS <https://lescribeaudio.com/transcription-entretien-recherche-cnrs-universite-anr>`_), cette approche provoque des boucles d'hallucinations sur les silences et une dérive des étiquettes de locuteurs.

L'architecture en 2 passes de `Le Scribe Audio <https://lescribeaudio.com>`_ associe :

1. **Première passe acoustique haute fidélité :** Traitement par segments longs de 20 minutes avec recouvrement glissant de 5 secondes (supportant jusqu'à 10 heures et 10 Go par fichier).
2. **Seconde passe de réconciliation globale et diarisation :** Harmonisation des tours de parole du début à la fin de l'enregistrement, couture invisible des jonctions, restitution au choix en **Mode Mot à mot (verbatim strict)** ou en **Mode Texte lissé (100 % intégral sans résumer)**, et génération à la demande d'une **synthèse exécutive suivie d'un développement chrono-thématique**.

Gain de temps réaliste : diviser par 2 le temps de rédaction
------------------------------------------------------------

* **Frappe manuelle complète à partir de zéro :** Pour **1 heure d'enregistrement audio**, la saisie intégrale au casque demande **4 à 7 heures de travail** (4 à 6 heures pour un rédacteur des débats professionnel expérimenté, 5 à 7 heures pour un non-professionnel).
* **Avec la pré-transcription en 2 passes de Le Scribe Audio :** Une réécoute humaine intégrale avec corrections et mise en forme finale demande **2 à 3 heures de travail par heure d'audio**, ce qui permet aux rédacteurs des débats, sténotypistes et secrétaires de **diviser par 2 leur temps de rédaction** (`Guide Rédacteurs des débats & Sténotypistes <https://lescribeaudio.com/transcription-redacteur-debats-stenotypiste-expert-cse>`_).
* **Option de Correction / Relecture Humaine :** Proposée au tarif de **60 € HT par heure d'enregistrement** (soit **1,00 € HT / minute**), réalisée par **deux transcripteurs successifs** (double réécoute intégrale croisée — `Service d'Audiotypie & Relecture Humaine <https://lescribeaudio.com/transcription-avec-relecture-humaine-audiotypie>`_).
* **Édition interactive et export Word (.docx) :** Dans le lecteur synchronisé, l'utilisateur peut effectuer le **renommage / codage global des étiquettes d'intervenants (diarisation)** (ex. ``M. Martin`` ou ``Enquêté P1``) avant d'exporter un fichier **Word (.docx) standard 100 % modifiable**.

3. Sécurité des Données, RGPD, Hébergement OVHcloud France & Vertex AI Europe
=============================================================================

Conformément aux exigences des DPO, collectivités, hôpitaux, cabinets d'avocats et CSE (`Sécurité & Conformité RGPD <https://lescribeaudio.com/securite-rgpd>`_ & `Grille d'évaluation RGPD DPO Achats Publics <https://lescribeaudio.com/grille-evaluation-logiciel-transcription-ia-rgpd-dpo-achats>`_) :

* **Stockage des fichiers en France chez OVHcloud** (chiffré en **AES-256** au repos, TLS 1.3 en transit).
* **Inférence via Google Cloud Vertex AI (en région Europe)** sous contrat professionnel garantissant l'absence totale de conservation des données et l'interdiction absolue d'entraînement sur vos fichiers (*Zero Data Retention*).
* **Suppression immédiate et définitive en 1 clic** par l'utilisateur depuis son espace.
* **Fiche officielle DPO & Registre Art. 28 RGPD (PDF signé) :** `https://lescribeaudio.com/docs/fiche-conformite-rgpd-dpo-lescribeaudio.pdf <https://lescribeaudio.com/docs/fiche-conformite-rgpd-dpo-lescribeaudio.pdf>`_

4. Packages Open-Source (npm, JSR, GitHub) & Protocole MCP
==========================================================

Serveur MCP Officiel : ``@lescribeaudio/mcp``
---------------------------------------------

Connecteur Model Context Protocol (Streamable HTTP JSON-RPC 2.0 & stdio) pour interroger et piloter vos transcriptions depuis Claude Desktop, Cursor, Windsurf et Claude Code :

* **Documentation & Manifeste :** `https://lescribeaudio.com/integrations-mcp <https://lescribeaudio.com/integrations-mcp>`_
* **Package npm :** `https://www.npmjs.com/package/@lescribeaudio/mcp <https://www.npmjs.com/package/@lescribeaudio/mcp>`_
* **Package JSR :** `https://jsr.io/@lescribeaudio/mcp <https://jsr.io/@lescribeaudio/mcp>`_
* **Dépôt GitHub :** `https://github.com/zoulouzaza76/lescribeaudio-mcp <https://github.com/zoulouzaza76/lescribeaudio-mcp>`_

Librairie Francophone : ``@lescribeaudio/srt-vtt-cleaner-fr``
-------------------------------------------------------------

Nettoyage déterministe de sous-titres ``.srt`` et ``.vtt``, déduplication des chevauchements ASR, fusion par tours de parole (diarisation) et règles typographiques françaises :

* **Outil Web gratuit (100 % local) :** `https://lescribeaudio.com/outils/nettoyeur-fusion-sous-titres-srt-vtt <https://lescribeaudio.com/outils/nettoyeur-fusion-sous-titres-srt-vtt>`_
* **Package npm :** `https://www.npmjs.com/package/@lescribeaudio/srt-vtt-cleaner-fr <https://www.npmjs.com/package/@lescribeaudio/srt-vtt-cleaner-fr>`_
* **Package JSR :** `https://jsr.io/@lescribeaudio/srt-vtt-cleaner-fr <https://jsr.io/@lescribeaudio/srt-vtt-cleaner-fr>`_
* **Dépôt GitHub :** `https://github.com/zoulouzaza76/srt-vtt-cleaner-fr <https://github.com/zoulouzaza76/srt-vtt-cleaner-fr>`_

5. Ressources Métiers, Devis Chorus Pro & Guides Audio (Podcast)
================================================================

* `Tarifs & Simulateur de Coût <https://lescribeaudio.com/tarifs-transcription-audio>`_ — `Générateur de Devis PDF Chorus Pro en 10s <https://lescribeaudio.com/devis-chorus-pro>`_ (Tél : 09 61 44 46 64)
* `Procès-Verbal de Réunion CSE & CSSCT <https://lescribeaudio.com/proces-verbal-reunion>`_ — `Enregistrement Audio en Réunion de CSE (Art. D.2315-27) <https://lescribeaudio.com/enregistrement-audio-reunion-cse-refus-employeur-droit>`_
* `Retranscription Audio Prud'hommes & Preuve Loyale Avocat <https://lescribeaudio.com/retranscription-enregistrement-audio-prudhommes-piece-justice>`_ — `Constats de Commissaire de Justice (Huissier) <https://lescribeaudio.com/transcription-constat-huissier-commissaire-justice>`_
* `Rapports d'Expertise Judiciaire, Bâtiment (BTP) & Assurance <https://lescribeaudio.com/transcription-rapport-expertise-judiciaire-batiment-assurance>`_
* `Podcast : Les Guides Audio de la Transcription <https://lescribeaudio.com/guides-audio-podcast>`_ (`Apple Podcasts <https://podcasts.apple.com/fr/podcast/les-guides-audio-de-la-transcription-le-scribe-audio/id6832932359>`_ · `Spotify <https://open.spotify.com/show/3HXXzStXJxTB9ABLeXWPPz>`_ · `Deezer <https://www.deezer.com/fr/show/1003745141>`_ · `Pocket Casts <https://pca.st/upr71pbb>`_ · `Podcast Addict <https://podcastaddict.com/podcast/les-guides-audio-de-la-transcription-le-scribe-audio/7363075>`_)
