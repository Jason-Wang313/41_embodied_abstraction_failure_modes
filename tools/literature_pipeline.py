import csv
import dataclasses
import html
import json
import math
import os
import re
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import requests


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TMP = ROOT / "tmp"


QUERIES = [
    "robot abstraction learning",
    "robot world model planning control manipulation",
    "embodied intelligence physical reasoning robot",
    "latent state robot policy planning",
    "sim-to-real robot control abstraction",
    "robot representation learning control",
    "robotic manipulation planning latent dynamics",
    "offline robot learning planning control",
    "tactile perception robot manipulation",
    "multimodal robot world model",
    "active perception robotics world model",
    "model-based reinforcement learning robot control",
    "state abstraction robotics control",
    "hierarchical robot learning planning abstraction",
    "symbolic robot planning grounding",
    "closed-loop robot planning failure modes",
    "observability robotics latent representation",
    "physical reasoning robot learning",
]


KEYWORDS = {
    "abstraction": ["abstract", "abstraction", "symbolic", "hierarchical", "latent", "representation", "state"],
    "physical": ["physical", "embodied", "tactile", "force", "contact", "manipulation", "grasp", "control"],
    "planning": ["plan", "planning", "policy", "controller", "control", "trajectory", "decision"],
    "world_model": ["world model", "dynamics", "predict", "forecast", "model-based", "latent"],
}


def normalize(text: str) -> str:
    text = html.unescape(text or "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def safe_ascii(text: str) -> str:
    return (
        text.replace("–", "-")
        .replace("—", "-")
        .replace("’", "'")
        .replace("“", '"')
        .replace("”", '"')
        .encode("ascii", "ignore")
        .decode("ascii")
    )


def crossref_search(session: requests.Session, query: str, rows: int = 100) -> List[dict]:
    url = "https://api.crossref.org/works"
    params = {
        "query.bibliographic": query,
        "rows": rows,
        "select": "DOI,title,author,container-title,issued,abstract,type,URL,is-referenced-by-count",
    }
    r = session.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json()["message"]["items"]


def arxiv_search(session: requests.Session, query: str, max_results: int = 50) -> List[dict]:
    url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    r = session.get(url, params=params, timeout=30)
    r.raise_for_status()
    text = r.text
    entries = []
    for block in re.findall(r"<entry>(.*?)</entry>", text, re.S):
        title = normalize(re.sub(r"<[^>]+>", " ", re.search(r"<title>(.*?)</title>", block, re.S).group(1))) if re.search(r"<title>(.*?)</title>", block, re.S) else ""
        summary = normalize(re.sub(r"<[^>]+>", " ", re.search(r"<summary>(.*?)</summary>", block, re.S).group(1))) if re.search(r"<summary>(.*?)</summary>", block, re.S) else ""
        idm = re.search(r"<id>(.*?)</id>", block, re.S)
        year = re.search(r"<published>(\d{4})-", block)
        entries.append({
            "title": title,
            "abstract": summary,
            "url": idm.group(1).strip() if idm else "",
            "year": int(year.group(1)) if year else None,
            "source": "arxiv",
        })
    return entries


def year_from_crossref(item: dict) -> Optional[int]:
    try:
        return int(item["issued"]["date-parts"][0][0])
    except Exception:
        return None


def authors_string(item: dict) -> str:
    authors = item.get("author") or []
    names = []
    for a in authors[:8]:
        family = a.get("family", "")
        given = a.get("given", "")
        if family or given:
            names.append(f"{given} {family}".strip())
    return "; ".join(names)


def abstract_text(item: dict) -> str:
    abs_text = item.get("abstract") or ""
    abs_text = re.sub(r"<[^>]+>", " ", abs_text)
    return normalize(abs_text)


def classify(title: str, abstract: str) -> dict:
    text = f"{title} {abstract}".lower()
    scores = {k: sum(text.count(w) for w in ws) for k, ws in KEYWORDS.items()}
    top = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
    topic = top[0][0] if top and top[0][1] > 0 else "other"
    return {
        "topic": topic,
        "score_abstraction": scores["abstraction"],
        "score_physical": scores["physical"],
        "score_planning": scores["planning"],
        "score_world_model": scores["world_model"],
    }


def extract_fields(title: str, abstract: str) -> dict:
    text = f"{title}. {abstract}".lower()
    hidden = []
    if any(k in text for k in ["latent", "representation", "state abstraction", "symbolic"]):
        hidden.append("state variables")
    if any(k in text for k in ["contact", "force", "tactile", "grasp", "manipul"]):
        hidden.append("contact geometry")
    if any(k in text for k in ["vision", "image", "camera"]):
        hidden.append("perception quality")
    if any(k in text for k in ["policy", "planning", "controller"]):
        hidden.append("control actionability")
    if any(k in text for k in ["sim-to-real", "sim2real", "transfer"]):
        hidden.append("domain shift")
    if any(k in text for k in ["world model", "predict", "forecast", "dynamics"]):
        hidden.append("dynamics fidelity")
    fixed = []
    if "abstract" in text or "abstraction" in text:
        fixed.append("variables discarded by abstraction")
    if "offline" in text:
        fixed.append("dataset support")
    if "hierarchical" in text:
        fixed.append("task decomposition")
    failures = []
    if "contact" in text or "manipul" in text:
        failures.append("contact discontinuities")
    if "sim-to-real" in text or "transfer" in text:
        failures.append("distribution shift")
    if "latent" in text or "representation" in text:
        failures.append("aliasing / observability limits")
    if "planning" in text:
        failures.append("long-horizon compounding error")
    return {
        "hidden_assumptions": "; ".join(dict.fromkeys(hidden)) or "not explicit",
        "fixed_variables": "; ".join(dict.fromkeys(fixed)) or "not explicit",
        "failure_modes": "; ".join(dict.fromkeys(failures)) or "not explicit",
    }


def paper_id(item: dict) -> str:
    doi = item.get("DOI") or item.get("doi") or ""
    url = item.get("URL") or ""
    if doi:
        return "doi:" + doi.lower()
    if url:
        return "url:" + url.lower()
    return "title:" + normalize((item.get("title") or [""])[0]).lower()


def main():
    DOCS.mkdir(exist_ok=True)
    TMP.mkdir(exist_ok=True)
    session = requests.Session()
    session.headers.update({"User-Agent": "codex-literature-sweep/1.0"})

    rows = []
    seen = set()
    source_counts = Counter()

    for q in QUERIES:
        try:
            items = crossref_search(session, q, rows=120)
        except Exception as e:
            items = []
            print(f"crossref failed for {q}: {e}")
        for item in items:
            title = normalize(" ".join(item.get("title") or []))
            if not title:
                continue
            pid = paper_id(item)
            if pid in seen:
                continue
            seen.add(pid)
            abstract = abstract_text(item)
            cls = classify(title, abstract)
            fields = extract_fields(title, abstract)
            year = year_from_crossref(item)
            rows.append({
                "paper_id": pid,
                "title": safe_ascii(title),
                "year": year or "",
                "venue": safe_ascii(" ".join(item.get("container-title") or [])),
                "source": "crossref",
                "query": q,
                "doi": item.get("DOI", ""),
                "url": item.get("URL", ""),
                "authors": safe_ascii(authors_string(item)),
                "abstract": safe_ascii(abstract),
                "topic": cls["topic"],
                "score_abstraction": cls["score_abstraction"],
                "score_physical": cls["score_physical"],
                "score_planning": cls["score_planning"],
                "score_world_model": cls["score_world_model"],
                "hidden_assumptions": safe_ascii(fields["hidden_assumptions"]),
                "fixed_variables": safe_ascii(fields["fixed_variables"]),
                "failure_modes": safe_ascii(fields["failure_modes"]),
            })
            source_counts["crossref"] += 1
            if len(rows) >= 1400:
                break
        if len(rows) >= 1400:
            break

    if len(rows) < 1000:
        for q in QUERIES[:8]:
            try:
                items = arxiv_search(session, q, max_results=80)
            except Exception as e:
                print(f"arxiv failed for {q}: {e}")
                continue
            for item in items:
                title = normalize(item.get("title") or "")
                if not title:
                    continue
                pid = paper_id(item)
                if pid in seen:
                    continue
                seen.add(pid)
                abstract = normalize(item.get("abstract") or "")
                cls = classify(title, abstract)
                fields = extract_fields(title, abstract)
                rows.append({
                    "paper_id": pid,
                    "title": safe_ascii(title),
                    "year": item.get("year", ""),
                    "venue": "arXiv",
                    "source": "arxiv",
                    "query": q,
                    "doi": "",
                    "url": item.get("url", ""),
                    "authors": "",
                    "abstract": safe_ascii(abstract),
                    "topic": cls["topic"],
                    "score_abstraction": cls["score_abstraction"],
                    "score_physical": cls["score_physical"],
                    "score_planning": cls["score_planning"],
                    "score_world_model": cls["score_world_model"],
                    "hidden_assumptions": safe_ascii(fields["hidden_assumptions"]),
                    "fixed_variables": safe_ascii(fields["fixed_variables"]),
                    "failure_modes": safe_ascii(fields["failure_modes"]),
                })
                source_counts["arxiv"] += 1
                if len(rows) >= 1400:
                    break
            if len(rows) >= 1400:
                break

    rows = rows[:1400]
    rows.sort(key=lambda r: (
        -(r["score_abstraction"] + r["score_physical"] + r["score_planning"] + r["score_world_model"]),
        -(int(r["year"]) if str(r["year"]).isdigit() else 0),
        r["title"],
    ))

    matrix_path = DOCS / "related_work_matrix.csv"
    with matrix_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [])
        writer.writeheader()
        writer.writerows(rows)

    meta = {
        "count": len(rows),
        "source_counts": dict(source_counts),
        "queries": QUERIES,
    }
    (DOCS / "literature_pipeline_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
