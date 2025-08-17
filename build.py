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

# Setup Jinja2 template environment
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('index.html')

# Generate HTML
html = template.render(
    name="Zhangxuan Gu",
    title="Researcher",
    affiliation="Ant Group",
    email="zhangxgu@126.com",
    bio="""
    <p>I received my Ph.D. in Computer Science from Shanghai Jiao Tong University in 2022, advised by Professor Liqing Zhang. Before that, I received my bachelor in Mathematics from SJTU in 2016. From 2022-now, I am a researcher at Ant Group.</p>
    """,
    papers_by_year=papers_by_year,
    sorted_years=sorted_years,
    current_year=datetime.datetime.now().year
)

# Output to file
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)