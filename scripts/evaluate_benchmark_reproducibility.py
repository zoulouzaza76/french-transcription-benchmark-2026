#!/usr/bin/env python3
"""
Protocole de Reproductibilité & Évaluation Ouverte — Benchmark ASR Français 2026 (v1.1.0)
Éditeur : LE SCRIBE AUDIO (https://lescribeaudio.com/benchmarks-precision-transcription-ia-francais)
Licence : MIT (code d'évaluation) / CC-BY-4.0 (données du benchmark — DOI 10.5281/zenodo.24215193)

Ce script autonome (zéro dépendance externe obligatoire ; compatible `jiwer` s'il est installé) permet :
  1. D'auditer et vérifier localement les données ouvertes du Benchmark 2026 (`benchmark_complet_2026.json`)
     ainsi que la grille complète des hyperparamètres d'inférence (Whisper large-v3, PyAnnote, 2 passes) :
       python3 evaluate_benchmark_reproducibility.py --audit

  2. D'évaluer n'importe quelle sortie ASR (ex. faster-whisper, WhisperX, P2AC Whisper, noScribe) face à une
     transcription de référence humaine selon DEUX métriques complémentaires :
       - WER & CER académiques normalisés (minuscules, sans ponctuation, standard ASR)
       - Révisions orthographiques & syntaxiques strictes (Insertions + Suppressions + 2 × Substitutions sur
         tokens ponctués et sensibles à la casse, reproduisant le comportement de `Révision > Comparer` sous
         Microsoft Word sur le français écrit) :
       python3 evaluate_benchmark_reproducibility.py --ref verite_terrain.txt --hyp sortie_whisper.txt
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

CANONICAL_BENCHMARK_JSON_URL = (
    "https://lescribeaudio.com/docs/benchmark/zenodo-metadata.json"
)
CANONICAL_TEXTS_JSON_URL = (
    "https://lescribeaudio.com/docs/benchmark/full_benchmark_texts.json"
)


def tokenize_normalized_asr(text: str) -> List[str]:
    """Tokenisation académique ASR standard (minuscules, apostrophes unifiées, hors ponctuation)."""
    cleaned = text.lower().replace("’", "'").replace("œ", "oe").replace("æ", "ae")
    cleaned = re.sub(r"[^\w\s'-]", " ", cleaned, flags=re.UNICODE)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned.split(" ") if cleaned else []


def tokenize_strict_word_revisions(text: str) -> List[str]:
    """
    Tokenisation stricte sensible à la casse, aux traits d'union et à la ponctuation,
    modélisant le découpage mot/ponctuation de `Révision > Comparer` sous Microsoft Word.
    """
    normalized_quotes = text.replace("’", "'")
    tokens = re.findall(r"\w+(?:['-]\w+)*|[^\w\s]", normalized_quotes, flags=re.UNICODE)
    return tokens


def levenshtein_counts(ref: Sequence[str], hyp: Sequence[str]) -> Tuple[int, int, int, int]:
    """
    Calcule par programmation dynamique (Wagner-Fischer en mémoire O(min(N, M))) :
      (substitutions, deletions, insertions, hits)
    """
    n, m = len(ref), len(hyp)
    prev = [(j, 0, 0, j) for j in range(m + 1)]
    for i in range(1, n + 1):
        curr = [(i, 0, i, 0)] + [(0, 0, 0, 0)] * m
        r_tok = ref[i - 1]
        for j in range(1, m + 1):
            if r_tok == hyp[j - 1]:
                curr[j] = prev[j - 1]
            else:
                sub_c, sub_s, sub_d, sub_i = prev[j - 1]
                del_c, del_s, del_d, del_i = prev[j]
                ins_c, ins_s, ins_d, ins_i = curr[j - 1]

                c_sub = (sub_c + 1, sub_s + 1, sub_d, sub_i)
                c_del = (del_c + 1, del_s, del_d + 1, del_i)
                c_ins = (ins_c + 1, ins_s, ins_d, ins_i + 1)
                curr[j] = min(c_sub, c_del, c_ins, key=lambda x: x[0])
        prev = curr

    _, subs, dels, ins = prev[m]
    hits = max(0, n - subs - dels)
    return subs, dels, ins, hits


def evaluate_pair(ref_text: str, hyp_text: str) -> Dict[str, float | int]:
    """Calcule le WER normalisé, le CER normalisé et l'équivalent Révisions Word strictes."""
    ref_norm = tokenize_normalized_asr(ref_text)
    hyp_norm = tokenize_normalized_asr(hyp_text)

    try:
        import jiwer  # type: ignore

        out = jiwer.process_words(" ".join(ref_norm), " ".join(hyp_norm))
        s_w, d_w, i_w, h_w = out.substitutions, out.deletions, out.insertions, out.hits
        wer = float(out.wer)
        cer = float(jiwer.cer(" ".join(ref_norm), " ".join(hyp_norm)))
    except Exception:
        s_w, d_w, i_w, h_w = levenshtein_counts(ref_norm, hyp_norm)
        wer = (s_w + d_w + i_w) / max(1, len(ref_norm))
        ref_chars = list(" ".join(ref_norm))
        hyp_chars = list(" ".join(hyp_norm))
        s_c, d_c, i_c, _ = levenshtein_counts(ref_chars, hyp_chars)
        cer = (s_c + d_c + i_c) / max(1, len(ref_chars))

    ref_strict = tokenize_strict_word_revisions(ref_text)
    hyp_strict = tokenize_strict_word_revisions(hyp_text)
    s_st, d_st, i_st, _ = levenshtein_counts(ref_strict, hyp_strict)
    word_style_revisions = i_st + d_st + (2 * s_st)

    return {
        "ref_words_normalized": len(ref_norm),
        "hyp_words_normalized": len(hyp_norm),
        "wer_normalized_pct": round(wer * 100.0, 2),
        "cer_normalized_pct": round(cer * 100.0, 2),
        "normalized_substitutions": s_w,
        "normalized_deletions": d_w,
        "normalized_insertions": i_w,
        "normalized_hits": h_w,
        "strict_tokens_ref": len(ref_strict),
        "strict_insertions": i_st,
        "strict_deletions": d_st,
        "strict_substitutions": s_st,
        "word_compare_equivalent_revisions": word_style_revisions,
    }


def run_dataset_audit(dataset_json_path: Path | None = None) -> int:
    """Vérifie et affiche la synthèse reproductible du jeu de données ouvert v1.1.0."""
    candidates = [
        dataset_json_path,
        Path(__file__).resolve().parent.parent / "dataset" / "benchmark_complet_2026.json",
        Path("open-science/french-transcription-benchmark-2026/dataset/benchmark_complet_2026.json"),
    ]
    resolved = next((p for p in candidates if p is not None and p.exists()), None)

    if resolved is None:
        print(
            "Info : fichier local `benchmark_complet_2026.json` non trouvé, "
            f"téléchargement des métadonnées publiques depuis {CANONICAL_BENCHMARK_JSON_URL}..."
        )
        with urllib.request.urlopen(CANONICAL_BENCHMARK_JSON_URL, timeout=15) as resp:
            meta = json.loads(resp.read().decode("utf-8"))
        print(f"Titre : {meta['metadata']['title']}")
        print(f"Fichiers PDF référencés : {len(meta.get('files_manifest', []))}")
        return 0

    data = json.loads(resolved.read_text(encoding="utf-8"))
    print("=" * 84)
    print(f"AUDIT DE REPRODUCTIBILITÉ — {data['dataset_id']} (v{data['version']})")
    print(f"Licence : {data['license']} | URL : {data['publisher']['canonical_benchmark_url']}")
    print("=" * 84)

    print("\n1. HYPERPARAMÈTRES D'INFÉRENCE DOCUMENTÉS :")
    hyper = data.get("methodology", {}).get("inference_hyperparameters", {})
    for group_key, params in hyper.items():
        print(f"  - [{group_key}]")
        for pk, pv in params.items():
            print(f"      {pk}: {pv}")

    print("\n2. RÉSULTATS SUR LES 3 CORPUS SCIENTIFIQUES CANAL-U (30 RAPPORTS PDF WORD) :")
    header = f"{'Rang':<5} {'Logiciel':<18} {'Éch.1':>7} {'Éch.2':>7} {'Éch.3':>7} {'Moyenne':>9} {'Ratio':>7}"
    print(header)
    print("-" * len(header))
    for row in data.get("benchmark_10_engines_canalu", []):
        print(
            f"{row['rank']:<5} {row['software']:<18} "
            f"{row['sample_1_medical_arapi_revisions']:>7} "
            f"{row['sample_2_physics_cnrs_cea_revisions']:>7} "
            f"{row['sample_3_ecology_univ_tours_revisions']:>7} "
            f"{row['mean_word_revisions']:>9.1f} "
            f"{row['error_ratio_vs_leader']:>6.2f}x"
        )
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Évaluateur reproductible WER / CER / Révisions Word — Benchmark ASR Français 2026"
    )
    parser.add_argument(
        "--audit",
        action="store_true",
        help="Audite le fichier benchmark_complet_2026.json et affiche les hyperparamètres d'inférence.",
    )
    parser.add_argument(
        "--dataset-json",
        type=Path,
        default=None,
        help="Chemin optionnel vers benchmark_complet_2026.json.",
    )
    parser.add_argument(
        "--ref",
        type=Path,
        default=None,
        help="Fichier texte (.txt, UTF-8) contenant la vérité terrain humaine.",
    )
    parser.add_argument(
        "--hyp",
        type=Path,
        default=None,
        help="Fichier texte (.txt, UTF-8) contenant la sortie brute du moteur ASR à évaluer.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Affiche les métriques au format JSON sur la sortie standard.",
    )
    args = parser.parse_args(argv)

    if args.ref and args.hyp:
        ref_text = args.ref.read_text(encoding="utf-8")
        hyp_text = args.hyp.read_text(encoding="utf-8")
        metrics = evaluate_pair(ref_text, hyp_text)
        if args.json:
            print(json.dumps(metrics, ensure_ascii=False, indent=2))
        else:
            print("Résultats d'évaluation reproductible (v1.1.0) :")
            print(f"  - Mots (référence normalisée)          : {metrics['ref_words_normalized']}")
            print(f"  - WER académique normalisé             : {metrics['wer_normalized_pct']:.2f} %")
            print(f"  - CER académique normalisé             : {metrics['cer_normalized_pct']:.2f} %")
            print(
                f"  - Détail WER (S / D / I)               : "
                f"{metrics['normalized_substitutions']} / {metrics['normalized_deletions']} / {metrics['normalized_insertions']}"
            )
            print(
                f"  - Équivalent Révisions Word strictes   : {metrics['word_compare_equivalent_revisions']} "
                f"(ponctuation, casse et accords inclus)"
            )
        return 0

    return run_dataset_audit(args.dataset_json)


if __name__ == "__main__":
    sys.exit(main())
