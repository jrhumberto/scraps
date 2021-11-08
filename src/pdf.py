#
# https://python.plainenglish.io/searching-for-text-in-those-annoying-pdfs-d95b6dc7a055
#
result_list = []
reader = PyPDF2.PdfFileReader(file)
for page_number in range(0, reader.numPages):
     page = reader.getPage(page_number)
     page_content = page.extractText()
     if search_term in page_content:
          result = {
               "page": page_number,
               "content": page_content
          }
          result_list.append(result)
reader.close()
