#!/usr/bin/env python3
"""Europe PMC search for Option B+ auditability survey (2026-09-05 freeze)."""
from __future__ import annotations

import csv
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw"
LOGS = ROOT / "logs"
RAW.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)

SEARCH_DATE = "2026-09-05"
BASE = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"

# Year filter via Europe PMC syntax
YEAR = 'FIRST_PDATE:[2020-01-01 TO 2026-12-31]'

QUERIES = {
    "Q1_protocol_broad": (
        f'({YEAR}) AND '
        f'(microbial OR bacterium OR bacterial OR "antimicrobial resistance" OR AMR OR pathogen) AND '
        f'(genome OR genomic OR WGS OR "whole genome") AND '
        f'("machine learning" OR "deep learning" OR "neural network" OR "random forest" OR "gradient boosting") AND '
        f'("leave-one" OR LOSO OR LOLO OR "cross-validation" OR "held out" OR hold-out OR "group" OR lineage OR species OR clade OR phylogenetic OR "domain generalization")'
    ),
    # Tighter primary working set: explicit hold-out / LOSO language
    "Q2_block_holdout_focus": (
        f'({YEAR}) AND '
        f'(microbial OR bacterium OR bacterial OR "antimicrobial resistance" OR AMR OR pathogen) AND '
        f'(genome OR genomic OR WGS OR "whole genome") AND '
        f'("machine learning" OR "deep learning" OR "neural network" OR "random forest" OR "gradient boosting") AND '
        f'("leave-one-out" OR "leave-one-species" OR "leave one species" OR LOSO OR LOLO OR '
        f'"leave-one-lineage" OR "species hold" OR "lineage hold" OR "held-out species" OR '
        f'"held out species" OR "cross-species" OR "across species" OR "phylogenetic split" OR '
        f'"phylogeny-aware" OR "group-aware" OR GroupKFold OR "blocked cross-validation" OR '
        f'"domain generalization" OR ("external validation" AND (species OR lineage OR clade)))'
    ),
    "Q3_amr_core": (
        f'({YEAR}) AND '
        f'("antimicrobial resistance" OR AMR OR "antibiotic resistance") AND '
        f'(genome OR genomic OR WGS) AND '
        f'("machine learning" OR "deep learning" OR "random forest") AND '
        f'("leave-one" OR LOSO OR LOLO OR "cross-species" OR lineage OR "phylogenetic" OR "held out" OR "external validation")'
    ),
}


def fetch_page(query: str, cursor: str = "*", page_size: int = 100) -> dict:
    params = {
        "query": query,
        "format": "json",
        "pageSize": str(page_size),
        "cursorMark": cursor,
        "resultType": "core",
    }
    url = BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "GenomeML-ReportCard-survey/0.1"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def harvest(query_id: str, query: str, max_records: int = 2000) -> tuple[int, list[dict]]:
    rows: list[dict] = []
    cursor = "*"
    hit_count = None
    while len(rows) < max_records:
        data = fetch_page(query, cursor=cursor)
        if hit_count is None:
            hit_count = int(data.get("hitCount") or 0)
        results = (data.get("resultList") or {}).get("result") or []
        if not results:
            break
        for r in results:
            rows.append(
                {
                    "query_id": query_id,
                    "search_date": SEARCH_DATE,
                    "pmid": r.get("pmid") or "",
                    "pmcid": r.get("pmcid") or "",
                    "doi": r.get("doi") or "",
                    "title": (r.get("title") or "").replace("\n", " ").strip(),
                    "authorString": (r.get("authorString") or "")[:300],
                    "journalTitle": r.get("journalTitle") or "",
                    "pubYear": r.get("pubYear") or "",
                    "firstPublicationDate": r.get("firstPublicationDate") or "",
                    "isOpenAccess": r.get("isOpenAccess") or "",
                    "source": r.get("source") or "",
                }
            )
        next_cursor = data.get("nextCursorMark")
        if not next_cursor or next_cursor == cursor:
            break
        cursor = next_cursor
        time.sleep(0.35)
        if len(rows) >= hit_count:
            break
    return hit_count or len(rows), rows


def main():
    log_lines = [f"search_date={SEARCH_DATE}", f"database=Europe PMC"]
    all_by_key: dict[str, dict] = {}
    summary = []

    for qid, q in QUERIES.items():
        print(f"Running {qid} ...")
        hit_count, rows = harvest(qid, q)
        out_json = RAW / f"{qid}_europepmc.json"
        out_csv = RAW / f"{qid}_europepmc.csv"
        out_json.write_text(json.dumps({"query": q, "hitCount": hit_count, "retrieved": len(rows), "results": rows}, indent=2), encoding="utf-8")
        with out_csv.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["query_id"])
            w.writeheader()
            w.writerows(rows)
        summary.append((qid, hit_count, len(rows)))
        log_lines.append(f"{qid}\thitCount={hit_count}\tretrieved={len(rows)}")
        print(f"  hitCount={hit_count} retrieved={len(rows)}")
        for r in rows:
            key = (r.get("doi") or r.get("pmid") or r.get("title") or "").lower()
            if not key:
                continue
            if key not in all_by_key:
                all_by_key[key] = {**r, "query_ids": qid}
            else:
                prev = all_by_key[key]["query_ids"]
                if qid not in prev.split("|"):
                    all_by_key[key]["query_ids"] = prev + "|" + qid

    # Dedup union of Q2+Q3 as working screen set (Q1 may be huge; still logged)
    working = []
    for r in all_by_key.values():
        qids = r.get("query_ids", "")
        if "Q2_" in qids or "Q3_" in qids or qids.startswith("Q2") or "Q2_block" in qids or "Q3_amr" in qids:
            working.append(r)
        # also include if only in Q1? No — keep Q1 as sensitivity log only for screen file from Q2∪Q3
    # Fix: query_ids format
    working = [r for r in all_by_key.values() if ("Q2_block_holdout_focus" in r["query_ids"] or "Q3_amr_core" in r["query_ids"])]

    screen_path = ROOT / "screening" / "title_abstract_screen_queue.csv"
    fields = [
        "evidence_source_id",
        "pmid",
        "doi",
        "title",
        "pubYear",
        "journalTitle",
        "query_ids",
        "screen_decision",
        "screen_reason",
        "screener",
        "screen_date",
        "notes",
    ]
    with screen_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for i, r in enumerate(sorted(working, key=lambda x: (x.get("pubYear") or "", x.get("title") or "")), start=1):
            w.writerow(
                {
                    "evidence_source_id": f"EPMC-{i:04d}",
                    "pmid": r.get("pmid", ""),
                    "doi": r.get("doi", ""),
                    "title": r.get("title", ""),
                    "pubYear": r.get("pubYear", ""),
                    "journalTitle": r.get("journalTitle", ""),
                    "query_ids": r.get("query_ids", ""),
                    "screen_decision": "pending",
                    "screen_reason": "",
                    "screener": "",
                    "screen_date": "",
                    "notes": "",
                }
            )

    log_lines.append(f"dedup_keys_all_queries={len(all_by_key)}")
    log_lines.append(f"working_screen_queue_Q2_union_Q3={len(working)}")
    (LOGS / "search_run_log.txt").write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    (LOGS / "search_summary.json").write_text(
        json.dumps(
            {
                "search_date": SEARCH_DATE,
                "database": "Europe PMC",
                "queries": {qid: {"hitCount": h, "retrieved": n} for qid, h, n in summary},
                "dedup_all": len(all_by_key),
                "working_queue": len(working),
                "note": "Primary screen queue = Q2 ∪ Q3 deduped. Q1 logged for sensitivity; if Q1>>Q2, report both.",
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print("Wrote", screen_path, "n=", len(working))


if __name__ == "__main__":
    main()
