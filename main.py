from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

def translate_text(text):
    translator = GoogleTranslator(source='auto', target='en')
    return translator.translate(text)

def chunk_text(text, max_chars=5000):
    # Split text into chunks no larger than max_chars
    chunks = []
    while len(text) > max_chars:
        # Find the last space within the max_chars limit
        split_index = text[:max_chars].rfind(' ')
        # If no space is found, split at max_chars
        if split_index == -1:
            split_index = max_chars
        chunks.append(text[:split_index])
        text = text[split_index:]
    chunks.append(text)
    return chunks

# Load the HTML file
with open('index.html', 'r') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

# Translate all text nodes
for element in soup.find_all(text=True):
    stripped_text = element.strip()
    if stripped_text:  # Only process non-empty text nodes
        translated_chunks = [translate_text(chunk) for chunk in chunk_text(stripped_text)]
        translated_text = ''.join(translated_chunks)
        element.replace_with(translated_text)

# Save the translated HTML to a new file
with open('/Users/anishsoni/Desktop/translator/new_index.html', 'w') as file:
    file.write(str(soup.prettify()))

print("Translation completed and saved to new file.")
