# 🟢 wordDrivesMeCrazy (Begüm Göktaş)

<p align="center">
  <img src="https://img.shields.io/badge/Status-Active-00FF00?style=for-the-badge&logo=matrix&logoColor=black" alt="Status">
  <img src="https://img.shields.io/badge/Python-FastAPI-00FF00?style=for-the-badge&logo=fastapi&logoColor=black" alt="FastAPI">
  <img src="https://img.shields.io/badge/Microsoft%20Word-VBA%20Macro-00FF00?style=for-the-badge&logo=microsoftword&logoColor=black" alt="Word VBA">
</p>

Writing multi-language documents or technical reports in Microsoft Word often feels like complete torture. Every time you insert a tech term like `backend`, `database`, or `refactor` into a non-English sentence, Word panics and litters your document with annoying red squiggly lines. 

Word's native "detect language automatically" feature frequently fails on word-level language switches (code-switching) and technical jargon. **wordDrivesMeCrazy** fixes this system flaw permanently.

With a single keyboard shortcut, it intelligently analyzes the sentence structure and individual foreign terms, mapping them to their proper language codes (LCID). The result is a clean, distraction-free document with correct language tagging and zero false red lines.

---

##  Features

* **Smart Word-Level Detection:** Analyzes the overall sentence context while recognizing individual foreign terms embedded within it.
* **Tech Jargon & Dictionary Support:** Powered by `pyspellchecker` and a custom tech-word registry (`TECH_WORDS`), accurately classifying software engineering jargon.
* **Dynamic Re-evaluation:** Add or edit foreign words inside an existing sentence and re-run the shortcut—the document updates instantly.
* **Distraction-Free Writing:** Keeps your document natively tagged without disabling spellcheck entirely.

---

## Prerequisites & Installation

### 1. Install Python Dependencies

Run the following command in your terminal to install the required packages:

```bash
pip install fastapi uvicorn langdetect pyspellchecker
```

### 2. Run the Local Language Server
Navigate to the project directory and start the server:

```bash
python app.py
```

You should see the startup confirmation in your terminal:
```bash
==================================================
🚀 LANGUAGE DETECTOR SERVER STARTED
👉 Press ALT + B in Microsoft Word to process text.
==================================================
```
##  Microsoft Word Setup (VBA Integration)

To make the shortcut available across all Word documents, save the VBA macro inside Word's global **`Normal.dotm`** template.

###  Option 1: Via the Developer Tab (Recommended)

1. **Enable the Developer Tab**
   - Go to **File → Options → Customize Ribbon**.
   - On the right panel, check **Developer** and click **OK**.

2. **Add the Macro**
   - Open the **Developer** tab and click **Visual Basic** (or press `ALT + F11`).
   - In the left **Project** panel, right-click **`Normal`** → **Insert → Module**.
   - Paste the project's VBA code into the new module.
   - Press **`Ctrl + S`** to save `Normal.dotm`, then close the editor.

###  Option 2: Without the Developer Tab

1. Open any Word document and press **`ALT + F11`**.
2. In the left panel, right-click **`Normal`** → **Insert → Module**.
3. Paste the VBA code, press **`Ctrl + S`**, and close the editor.

##  Assigning Your Chosen Shortcut

1. Open Word and go to **File → Options → Customize Ribbon**.
2. At the bottom, click **Keyboard shortcuts: Customize...**.
3. Select **Macros** from the **Categories** list.
4. Choose **`AutoDetectCurrentSentenceLanguage`** from the **Commands** list.
5. **Important:** Set **Save changes in:** to **`Normal.dotm`**.
6. Click **Press new shortcut key**, press **`youCanDecideYours,MineWas:ALT+B`**, then click **Assign**.

##  Testing the Setup

Make sure `app.py` is running in your terminal before testing.

### Mixed Tech-Jargon Sentence

> *"Toplantı başlamadan önce herkese привет deyip sunumu launch edeceğiz."*

- Place your cursor anywhere inside the sentence.
- Press **`ALT + B`**.

**Expected result:**

- The macro automatically detects the language of each part of the sentence.
- The sentence stays Turkish.
- Words like `привет`, `launch` are automatically marked as **Russian and English (US)** respectively.
- The incorrect red spell-check underlines disappear.

### Dynamic Word Additions

1. Write a sentence.
2. Press **`ALT + B(for me)`**.
3. Add new foreign-language words.
4. Press **`ALT + B(for me)`** again.

The sentence is re-analyzed and updated automatically each time.

## Active Development (`feature/batch-doc-fixer`)

A new feature branch is currently in development to support **external `.docx` processing**.

### Planned Features

- **Direct document ingestion** — Process an existing `.docx` file without manually selecting sentences.
- **Automatic sentence extraction** — Parse paragraphs and sentences sequentially.
- **Batch language detection** — Send extracted sentences to the `app.py` detection server automatically.
- **Clean output generation** — Produce a new `.docx` with correct proofing languages already applied.

> This feature is still under development. Stay tuned for batch document processing updates.




