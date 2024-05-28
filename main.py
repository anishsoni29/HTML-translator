from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

def translate_text(text):
    try:
        translator = GoogleTranslator(source='auto', target='en')
        return translator.translate(text)
    except Exception as e:
        print(f"Error translating text: {e}")
        return text  # Return the original text if translation fails

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
with open('index.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

# Translate all text nodes
for element in soup.find_all(string=True):
    stripped_text = element.strip()
    if stripped_text:  # Only process non-empty text nodes
        translated_chunks = [translate_text(chunk) for chunk in chunk_text(stripped_text)]
        translated_chunks = [chunk for chunk in translated_chunks if chunk is not None]
        translated_text = ''.join(translated_chunks)
        element.replace_with(translated_text)

# Manually change the <html lang to "en">
html_tag = soup.find('html')
if html_tag:
    html_tag['lang'] = 'en'

# Manually add the <!DOCTYPE html> line
new_soup = BeautifulSoup("<!DOCTYPE html>", 'html.parser')
new_soup.append(soup)

# Save the translated HTML to a new file
with open('new_index.html', 'w', encoding='utf-8') as file:
    file.write(str(new_soup.prettify()))

print("Translation completed and saved to new file.")