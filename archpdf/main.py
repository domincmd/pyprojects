import requests
from bs4 import BeautifulSoup, Comment
from weasyprint import HTML

r = requests.get('https://wiki.archlinux.org/title/Frequently_asked_questions') #this scrapes the entire website
html_doc = r.text #just the plain text of the website

soup = BeautifulSoup(html_doc, 'html.parser')

main = soup.find("main")

if main:
    # Create a fresh document with only <main>
    print("FOUND MAIN")
    soup = BeautifulSoup("""
<html>
<style>
body {
    font-family: sans-serif;
}

span.section-number, span.subsection-number {
    font-style: italic;
    color: #6b3e26;
}

p {
    text-align: justify;
    margin-top: 10px;
}

pre {
    background-color: #ebf1f5;
    padding: 1em;
    border: 1px solid #bcd;
    white-space: pre-wrap;      /* allow wrapping */
    word-wrap: break-word;      /* older support */
    overflow-wrap: break-word;  /* modern standard */
}

code {
    background-color: #ebf1f5;
}

.archwiki-template-meta-related-articles {
    border: 1px solid #333;
    max-width: 40%;
}

.archwiki-template-meta-related-articles > p {
    width: 100%;
    background-color: #333;
    border-bottom: 5px #08c solid;
    color: white;
    font-weight: bold;
    margin: 0;
    padding: 5px;
    box-sizing: border-box;
}

.archwiki-template-box {
    margin: 1em 0;
    padding: 0.5em 1em;
}



.archwiki-template-box strong::after {
  content: "\\A";
  white-space: pre;
}

.archwiki-template-box-warning {
    background-color: #fdd;
    border: 1px solid #ff5757;
    border-left: 5px solid #ff5757;
}

.archwiki-template-box-note {
    background-color: #dff0ff;
    border: 1px solid #08c;
    border-left: 5px solid #08c;
}

.archwiki-template-box-tip {
    background-color: #dfd;
    border: 1px solid #4dcb4d;
    border-left: 5px solid #4dcb4d;
}


h2 {
  margin: 0;
}

h3 {
  margin-top: 25px;
  margin-bottom: 0px;
}

h2::after {
  content: "";
  display: inline-block;
  width: 100%;
  height: 1px;
  background: #333;
  margin-right: 8px;
  margin-bottom: 10px;
}

table {
    border-collapse: collapse; /* prevents double borders */
    width: 100%;
}

table th,
table td {
    border: 1px solid #a2a9b1; /* same color everywhere */
    padding: 8px;
    background-color: #f9faff;
}

table > * > tr > th {
    background-color: #eaecf0;
    color: #202122;
    text-align: center;
}

table > caption {
    width: 100%;
    text-align: center;
}
</style>
<body>
</body>
</html>
""", "html.parser")
    soup.body.append(main)

selectors = [
    "#p-lang-btn",
    ".vector-sticky-pinned-container",
    ".vector-page-toolbar",
    "nav",
    ".vector-body-before-content",
    "#catlinks",
    ".printfooter",
    ".archwiki-template-meta-related-articles"
]

for sel in selectors:
    for tag in soup.select(sel):
        tag.decompose()

# remove comments
for comment in soup.find_all(string=lambda t: isinstance(t, Comment)):
    comment.extract()

h2_count = 0
h3_count = 0
h4_count = 0

for tag in soup.find_all(["h2", "h3", "h4"]):
    if tag.name == "h2":
        h2_count += 1
        h3_count = 0
        h4_count = 0

        num = soup.new_tag("span", **{"class": ["section-number"]})
        num.string = f"{h2_count} "

        tag.insert(0, num)

    elif tag.name == "h3":
        h3_count += 1
        h4_count = 0

        num = soup.new_tag("span", **{"class": ["subsection-number"]})
        num.string = f"{h2_count}.{h3_count} "

        tag.insert(0, num)
    
    elif tag.name == "h4":
        h4_count += 1

        num = soup.new_tag("span", **{"class": ["subsection-number"]})
        num.string = f"{h2_count}.{h3_count}.{h4_count} "

        tag.insert(0, num)

HTML(string=soup.prettify()).write_pdf("output.pdf")



print(soup.prettify())