import re
import random

def generate_questions(text, num_questions=3):
    """
    Vygeneruje doplňovací otázky z textu.
    Najde delší slova a nahradí je podtržítky.
    """
    if not text or len(text) < 20:
        return "Text je příliš krátký pro generování otázek."

    # Rozdělení na věty
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s', text)
    valid_sentences = [s for s in sentences if len(s) > 20] # Použijeme jen delší věty
    
    questions = []
    
    # Vybereme náhodné věty pro otázky
    selected_sentences = random.sample(valid_sentences, min(num_questions, len(valid_sentences)))
    
    for sentence in selected_sentences:
        # Najdeme slova delší než 5 znaků
        words = re.findall(r'\b[a-zA-ZáčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ]{6,}\b', sentence)
        
        if words:
            # Vybereme jedno náhodné klíčové slovo k odstranění
            keyword = random.choice(words)
            # Nahradíme slovo v textu
            question_text = sentence.replace(keyword, "______", 1)
            questions.append(f"Otázka: {question_text}\n(Odpověď: {keyword})\n")
    
    if not questions:
        return "Nepodařilo se najít vhodná slova pro otázky."
        
    return "\n".join(questions)