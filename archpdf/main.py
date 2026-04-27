from utils.createpdf import createpdf
from utils.pdfutils import merge_pdfs, add_page_numbers

"""
list of pages to include:
"https://wiki.archlinux.org/title/Arch_Linux"
"https://wiki.archlinux.org/title/Installation_guide"
"https://wiki.archlinux.org/title/GRUB"
"https://wiki.archlinux.org/title/General_recommendations"
"https://wiki.archlinux.org/title/Arch_boot_process"
"https://wiki.archlinux.org/title/Users_and_groups"
"""

pages_to_include = ["https://wiki.archlinux.org/title/Arch_Linux", 
                    "https://wiki.archlinux.org/title/Installation_guide", 
                    "https://wiki.archlinux.org/title/GRUB"]
i = 0
for page in pages_to_include:
    createpdf(page, f"temp/{i}.pdf")
    i += 1

list_of_pdfs = [f"temp/{str(x)}.pdf" for x in range(i)]

print(list_of_pdfs)

merge_pdfs(list_of_pdfs, "temp/output_not_numbered.pdf")

add_page_numbers("temp/output_not_numbered.pdf", "temp/output.pdf", "bottom-right")