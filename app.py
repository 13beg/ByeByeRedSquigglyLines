# =====================================================================
# Word Auto-Language Detector Server
# Kurulum: pip install fastapi uvicorn langdetect
# Begüm Göktaş - 14.08.2026
# =====================================================================

from fastapi import FastAPI
from pydantic import BaseModel
from langdetect import detect_langs, LangDetectException, DetectorFactory
import uvicorn

# Tutarlı sonuçlar üretsin diye başta sıfırladım
DetectorFactory.seed = 0

app = FastAPI(title="Word Language Detector")

# Microsoft Word OpenXML Dil Numaralandırma Sistemi (LCID Codes)
LANG_MAP = {
    'tr': 1055,  # Turkish
    'en': 1033,  # English (US)
    'de': 1031,  # German
    'fr': 1036,  # French
    'ru': 1049,  # Russian
}

DEFAULT_LANG_ID = 1055  # Şüpheye düşüldüğünde varsayılan dil :Türkçe
MIN_LENGTH = 10         # Çok kısa kelimelerde yanlış dil atamasını engelleme sınırı
MIN_CONFIDENCE = 0.60   # Güven Eşiği (%60 olasılığın altındakileri varsayılan dil yap)


class TextRequest(BaseModel):
    text: str


@app.post("/detect-language")
def detect_language(req: TextRequest):
    text = req.text.strip()

    # 1. Metin çok kısa ise hemen varsayılan dili döndür
    if len(text) < MIN_LENGTH:
        return {"lang_id": DEFAULT_LANG_ID, "confidence": None, "reason": "too_short"}

    try:
        # 2. Olasılık tabanlı dil analizi yap
        candidates = detect_langs(text)
        best = candidates[0]  # En yüksek olasılıklı dil tahmini

        # 3. Güven seviyesi %60'ın altındaysa riske girme, varsayılana düş
        if best.prob < MIN_CONFIDENCE:
            return {
                "lang_id": DEFAULT_LANG_ID, 
                "confidence": best.prob, 
                "reason": "low_confidence"
            }

        # 4. Tespit edilen dil haritasında var mı bak, yoksa İngilizce (1033) ata
        lang_id = LANG_MAP.get(best.lang, 1033)
        return {"lang_id": lang_id, "confidence": best.prob, "reason": "ok"}

    except LangDetectException:
        # Kütüphane metni çözemezse varsayılan dile dön
        return {"lang_id": DEFAULT_LANG_ID, "confidence": None, "reason": "error"}


@app.get("/ping")
def ping():
    return {"status": "ok"}


if __name__ == "__main__":
    # Uvicorn sunucusunu 127.0.0.1:8000 adresinde ayağa kaldırır
    uvicorn.run(app, host="127.0.0.1", port=8000)
