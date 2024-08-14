from PyPDF2 import PdfReader, PdfWriter

# Open the original PDF
reader = PdfReader(r'C:/Users/Ramesh/Downloads/screencapture-docs-uat-us-oracle-en-learn-oracle-integration-msentraid-2024-08-09-18_34_56.pdf')
writer = PdfWriter()

for page in reader.pages:
    page.cropbox.lower_left = (72, 132)  # Adjust as needed
    page.cropbox.upper_right = (page.mediabox.right - 135, page.mediabox.top)  # Adjust as needed
    writer.add_page(page)

# Save the cropped PDF
with open('cropped.pdf', 'wb') as output_pdf:
    writer.write(r'C:\Security\utput_pdf.pdf')
