import fitz

# Open the text file
with open('input.txt', 'r') as file:
    text = file.read()

# Create a new PDF document
doc = fitz.open()

# Add a new page to the document
page = doc.new_page()

# Add the text to the page
page.insert_text(point = (1,23), text = text, fontsize=12)

# Save the document as a PDF file
doc.save('output.pdf')

# Close the document
doc.close()
