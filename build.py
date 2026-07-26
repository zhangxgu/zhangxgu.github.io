from jinja2 import Environment, FileSystemLoader
import yaml
import datetime
import re

NAME = "Zhangxuan Gu"

VENUE_DISPLAY = {
    "NIPS": "NeurIPS",
    "ACMMM": "ACM MM",
    "ACMMM(oral)": "ACM MM",
    "Icassp": "ICASSP",
    "Icassp(oral)": "ICASSP",
    "ICML(oral)": "ICML",
    "Arxiv": "Arxiv",
}

CCF_A = {
    "CVPR", "ICCV", "NIPS", "NeurIPS", "AAAI", "ACMMM", "ICML",
    "TMM", "SCIS",
}
CCF_B = {"ECCV", "Icassp", "ICASSP", "TNNLS", "TCSVT"}


def bold_authors(authors: str, name: str) -> str:
    parts = []
    author_list = authors.split(", ")
    for i, author in enumerate(author_list):
        is_marked = bool(re.fullmatch(re.escape(name) + r"[\*^]+", author))
        is_plain_me = author == name
        if is_marked or (is_plain_me and i == 0):
            # 一作 / 共一(*) / 通讯(^) — same accent color
            parts.append(f'<b class="author-me-star">{author}</b>')
        elif is_plain_me:
            # 非一作、非共一、非通讯
            parts.append(f'<b class="author-me">{author}</b>')
        else:
            parts.append(author)
    return ", ".join(parts)


def enrich_paper(paper: dict) -> dict:
    p = dict(paper)
    raw = str(p.get("venue", ""))
    is_oral = bool(re.search(r"\(oral\)", raw, re.I))
    base = re.sub(r"\(oral\)", "", raw, flags=re.I).strip()
    display_base = VENUE_DISPLAY.get(raw, VENUE_DISPLAY.get(base, base))
    year = p["year"]
    # Match existing site style: "CVPR 2023" vs "Arxiv, 2026" / "TMM, 2020"
    if display_base.lower() in {"arxiv", "tmm", "tnnls", "tcsvt", "scis"}:
        venue_label = f"{display_base}, {year}"
    else:
        venue_label = f"{display_base} {year}"

    ccf = None
    if base in CCF_A or display_base in CCF_A or raw in CCF_A:
        ccf = "A"
    elif base in CCF_B or display_base in CCF_B:
        ccf = "B"

    p["authors_html"] = bold_authors(p["authors"], NAME)
    p["venue_label"] = venue_label
    p["ccf"] = ccf
    p["is_oral"] = is_oral
    return p


with open("papers.yml", encoding="utf-8") as f:
    papers = [enrich_paper(p) for p in yaml.safe_load(f)]

papers_by_year = {}
for paper in papers:
    year = paper["year"]
    papers_by_year.setdefault(year, []).append(paper)

sorted_years = sorted(papers_by_year.keys(), reverse=True)

now = datetime.datetime.now()
current_year = now.year

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("index.html")

html = template.render(
    name=NAME,
    papers_by_year=papers_by_year,
    sorted_years=sorted_years,
    current_year=current_year,
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Built index.html with {len(papers)} papers.")
