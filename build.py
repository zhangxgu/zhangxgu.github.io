from jinja2 import Environment, FileSystemLoader
import yaml
import datetime

# Load paper data
with open('papers.yml',encoding='utf-8') as f:
    papers = yaml.safe_load(f)

# Group papers by year in descending order
papers_by_year = {}
for paper in papers:
    year = paper['year']
    if year not in papers_by_year:
        papers_by_year[year] = []
    papers_by_year[year].append(paper)

# Sort years from newest to oldest
sorted_years = sorted(papers_by_year.keys(), reverse=True)

# "Recent" badge in Publications: year >= current_year - 1 (calendar window; YAML has no month).
now = datetime.datetime.now()
current_year = now.year
highlight_min_year = current_year - 1

# Setup Jinja2 template environment
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('index.html')

education = [
    {
        "degree": "Ph.D. in Computer Science",
        "institution": "Shanghai Jiao Tong University",
        "period": "2016 – 2022",
        "detail": "Advisor: Professor Liqing Zhang",
    },
    {
        "degree": "B.Sc. in Mathematics",
        "institution": "Shanghai Jiao Tong University",
        "period": "2012 – 2016",
    },
]

work_experience = [
    {
        "role": "Researcher",
        "organization": "Ant Group",
        "period": "2022 – present",
    },
]

# Generate HTML
html = template.render(
    name="Zhangxuan Gu",
    title="Researcher",
    affiliation="Ant Group",
    email="zhangxgu@126.com",
    bio="""
    <p>I work on computer vision, multimodal learning, and GUI agents. I received my Ph.D. from Shanghai Jiao Tong University and am now a researcher at Ant Group.</p>
    """,
    education=education,
    work_experience=work_experience,
    papers_by_year=papers_by_year,
    sorted_years=sorted_years,
    current_year=current_year,
    highlight_min_year=highlight_min_year,
)

# Output to file
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)