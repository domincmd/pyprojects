import requests
from bs4 import BeautifulSoup, Comment
from weasyprint import HTML

def formatpdf(soup): # this function applies custom formating to the soup. change at will.
    #this formats h2, h3 and h4 to contain numbers.

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
    
    return soup

def createpdf(url, output): # this needs to be an archlinux wiki page for the script to work, output is the name of the output file

    html_doc = requests.get(url).text #just the plain text of the website

    scrapedsoup = BeautifulSoup(html_doc, 'html.parser')

    with open("pdfpage.html", "r", encoding="utf-8") as f: #this will be the base for the pdf
        htmlfile = f.read()

    main = scrapedsoup.find("main")

    if not main:
        print("NO MAIN FOUND")
        print("no main section found. this script cannot format the pdf correctly")
        return None

    # create a fresh document (soup) with only <main>
    soup = BeautifulSoup(htmlfile, "html.parser")
    soup.body.append(main)

    selectors = [ #these selectors are removed on execution
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

    soup = formatpdf(soup) # apply formatting

    HTML(string=soup.prettify()).write_pdf(f"{output}.pdf")

    return f"Successfully created pdf {output}.pdf"



createpdf("https://wiki.archlinux.org/title/Installation_guide", "output")