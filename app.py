# =====================================================================
# Word Multi-Language Dynamic Server (Sözlük Destekli)
# Kurulum: pip install fastapi uvicorn langdetect pyspellchecker
# =====================================================================

from fastapi import FastAPI
from pydantic import BaseModel
from langdetect import detect_langs, LangDetectException, DetectorFactory
from spellchecker import SpellChecker
import uvicorn
import re

DetectorFactory.seed = 0
app = FastAPI(title="Word Language Server")

# Microsoft Word Dil Kodları (LCID)
LANG_MAP = {
    'tr': 1055,  # Türkçe
    'en': 1033,  # İngilizce
    'de': 1031,  # Almanca
    'fr': 1036,  # Fransızca
    'ru': 1049,  # Rusça
}
DEFAULT_LANG_ID = 1055

# Sözlükleri başlatıyoruz (İlk açılışta hafızaya yüklenir)
print("Dil sözlükleri yükleniyor, lütfen bekleyin...")
spell_en = SpellChecker(language='en')
spell_de = SpellChecker(language='de')
spell_fr = SpellChecker(language='fr')
spell_ru = SpellChecker(language='ru')

# Kontrol edilecek yabancı diller sözlük haritası
FOREIGN_CHECKERS = [
    (spell_en, 1033),  # İngilizce
    (spell_de, 1031),  # Almanca
    (spell_fr, 1036),  # Fransızca
    (spell_ru, 1049),  # Rusça
]

class WordListRequest(BaseModel):
    sentence_text: str
    words: list[str]

def detect_single_word_lang(word: str, sentence_main_lang: int) -> int:
    clean = re.sub(r'[^\w\s]', '', word).strip().lower()

    # 3 harften kısa kelimeler veya sayılar cümlenin ana dilini korusun
    if len(clean) < 3 or clean.isdigit():
        return sentence_main_lang

    #Sözlük Kontrolü
    for checker, lcid in FOREIGN_CHECKERS:
        # Eğer cümlenin ana dili zaten bu dil değilse ve kelime bu sözlükte varsa:
        if lcid != sentence_main_lang:
            if clean in checker:
                return lcid

    # 2. ÖNCELİK: Sözlükte bulunamadıysa cümlenin ana diline sadık kal
    return sentence_main_lang

@app.post("/analyze-sentence")
def analyze_sentence(req: WordListRequest):
    sentence = req.sentence_text.strip()
    words = req.words

    # 1. Cümlenin GENEL Ana Dilini Tespiti
    sentence_main_lang = DEFAULT_LANG_ID
    try:
        sentence_candidates = detect_langs(sentence)
        if sentence_candidates and sentence_candidates[0].prob >= 0.50:
            sentence_main_lang = LANG_MAP.get(sentence_candidates[0].lang, DEFAULT_LANG_ID)
    except LangDetectException:
        pass

    # 2. Her kelime için dinamik dil tespiti
    lcids = []
    for w in words:
        word_lcid = detect_single_word_lang(w, sentence_main_lang)
        lcids.append(str(word_lcid))

    print(f"➜ [ANALİZ] Cümle: '{sentence[:30]}...' | Ana Dil: {sentence_main_lang} | İşlenen Kelime: {len(words)}")

    return {"lcids": "|".join(lcids)}

if __name__ == "__main__":
    print("\n" + "="*50)
    print("DİL TESPİT SUNUCUSU BAŞLATILDI (SÖZLÜK ENTEGRELİ)")
    print("Word üzerinde ALT + B basarak test edebilirsiniz.") # ALT + B kısayolunu ben belirledim
    print("="*50 + "\n")
    uvicorn.run(app, host="127.0.0.1", port=8000)
