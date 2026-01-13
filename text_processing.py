import re

def generate_summary(text, num_sentences=3):
    """
    Jednoduchá extrakce shrnutí na základě četnosti slov.
    Vrátí 'num_sentences' nejdůležitějších vět.
    """
    if not text:
        return "Chyba: Nebyl zadán žádný text."
    
    # 1. Rozdělení na věty (jednoduché rozdělení podle tečky, vykřičníku, otazníku)
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s', text)
    
    if len(sentences) <= num_sentences:
        return text  # Text je příliš krátký, vrátíme ho celý
    
    # 2. Předzpracování textu a počítání slov
    stopwords = {'a', 'i', 'o', 'u', 'v', 's', 'k', 'z', 'se', 'si', 'je', 'to', 'co', 'na', 'do', 'od'}
    word_frequencies = {}
    
    clean_text = text.lower()
    words = re.findall(r'\w+', clean_text)
    
    for word in words:
        if word not in stopwords:
            if word not in word_frequencies:
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
                
    # Normalizace frekvencí
    max_frequency = max(word_frequencies.values()) if word_frequencies else 1
    for word in word_frequencies:
        word_frequencies[word] = (word_frequencies[word] / max_frequency)

    # 3. Ohodnocení vět
    sentence_scores = {}
    for sentence in sentences:
        for word in re.findall(r'\w+', sentence.lower()):
            if word in word_frequencies:
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = word_frequencies[word]
                else:
                    sentence_scores[sentence] += word_frequencies[word]

    # 4. Výběr nejlepších vět
    import heapq
    summary_sentences = heapq.nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    
    # Seřadit věty tak, jak šly v textu po sobě (pro čitelnost), ne podle skóre
    # Ale pro jednoduchost v MVP verzi vrátíme spojené top věty
    summary = ' '.join(summary_sentences)
    return summary