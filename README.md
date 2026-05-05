# 🧠 PIPO – AI Voice Assistant  

**PIPO (Personal Intelligent Processing Operator)** is a **multilingual AI-powered voice assistant** designed for real-time task automation using advanced Natural Language Processing (NLP), Automatic Speech Recognition (ASR), and Text-to-Speech (TTS) systems.

Built with a **multimodal architecture leveraging BERT, SpaCy, and GPT-2**, PIPO delivers intelligent, fast, and context-aware interactions with an impressive **~94% accuracy** and **~1.2s response latency**.

---

## 🚀 Features  

- 🎙️ **Voice Command Processing (ASR)**  
  Converts speech into text using high-accuracy speech recognition systems  

- 🗣️ **Text-to-Speech (TTS)**  
  Natural voice responses using `pyttsx3`  

- 🌍 **Multilingual Support**  
  Language detection powered by **mBERT**  

- 🧠 **Advanced NLP Pipeline**  
  - **BERT** → Intent classification  
  - **SpaCy** → Grammar & entity parsing  
  - **Regex + Rules** → Pattern matching  
  - **GPT-2 Small** → Dynamic response generation  

- ⚡ **Low Latency System**  
  ~1.2 seconds average response time  

- 💻 **System Automation**  
  Execute tasks like:
  - Opening applications  
  - Searching the web  
  - Playing media  
  - Fetching real-time data  

---

## 🏗️ System Architecture  

PIPO follows a **modular multimodal pipeline**:

1. **User Input Module**
   - Voice (ASR) or Text input  

2. **Language Detection**
   - Multilingual BERT (mBERT)  

3. **Intent Understanding**
   - SpaCy + Regex + BERT  

4. **Query Classification**
   - General queries → BERT  
   - Logical/math → Python modules  
   - Real-time → Web scraping  

5. **Response Generation**
   - GPT-2 + TTS output  

---

## 📊 Performance  

| Model        | Role                      | Performance |
|-------------|---------------------------|------------|
| **BERT**     | Intent Classification     | ~94% accuracy |
| **SpaCy**    | NLP & Text Categorization | Strong classification (low loss) |
| **GPT-2 Small** | Response Generation     | Rapid convergence, low loss |
| **Overall System** | End-to-End Assistant | ⚡ ~1.2s latency |

---

## 🛠️ Tech Stack  

**Languages & Frameworks**
- Python 3  
- PyTorch / TensorFlow  

**Libraries**
- transformers  
- spaCy  
- scikit-learn  
- SpeechRecognition  
- pyttsx3  
- gTTS  
- PyAudio  

**Models**
- BERT (Intent Detection)  
- GPT-2 Small (Response Generation)  
- mBERT (Language Detection)  

---

## ⚙️ Installation  

```bash
# Clone the repository
git clone https://github.com/mayankbhagat/PIPO-AI-VOICE-ASSISTTANT.git

# Navigate into the project
cd PIPO-AI-VOICE-ASSISTTANT

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Usage  

```bash
python main.py
```

Then:
- Speak your command 🎤  
- Or input text manually  

---

## 💡 Example Commands  

- "Open Chrome"  
- "Play music"  
- "What’s the weather today?"  
- "Search Wikipedia for AI"  

---

## 📚 Research & Background  

This project is based on a structured approach combining:
- Natural Language Processing  
- Intent Classification  
- Speech Recognition  
- Transformer-based Models  

---

## 📈 Comparison with Existing Systems  

| Feature | PIPO | Traditional Assistants |
|--------|------|----------------------|
| Multilingual Support | ✅ | Limited |
| Multimodal NLP | ✅ | Partial |
| Latency | ⚡ Fast (~1.2s) | Moderate |
| Customizability | High | Low |
| Accuracy | ~94% | Varies |

---

## 🔮 Future Improvements  

- Integration with IoT devices  
- Cloud-based deployment  
- Improved conversational memory  
- Advanced LLM integration  
- Mobile & cross-platform support  

---

## 📜 License  

This project is licensed under the **MIT License**.

---

## ⭐ Support  

If you found this project useful, consider giving it a ⭐ on GitHub!
