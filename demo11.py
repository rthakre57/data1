import streamlit as st
import speech_recognition as sr
import pandas as pd
import time

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Define storage for Q&A
qa_data = {"Question": [], "Answer": []}

st.title("🎤 Marathi Speech-to-Text Q&A Collector")

st.write("👋 Click the button below and speak in Marathi!")

# Function to record speech
def record_speech():
    with sr.Microphone() as source:
        st.write("🎙️ बोलायला सुरुवात करा (Start Speaking)...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=36000)
            text = recognizer.recognize_google(audio, language="mr-IN")
            return text
        except sr.UnknownValueError:
            st.error("⚠️ आवाज समजला नाही, कृपया पुन्हा प्रयत्न करा!")
            return None
        except sr.RequestError:
            st.error("⚠️ Google Speech API शी कनेक्ट होऊ शकले नाही!")
            return None

# Record Question
if st.button("🔴 प्रश्न विचारा"):
    question = record_speech()
    if question:
        st.success(f"✅ प्रश्न: {question}")
        qa_data["Question"].append(question)

# Record Answer
if st.button("🟢 उत्तर द्या"):
    answer = record_speech()
    if answer:
        st.success(f"✅ उत्तर: {answer}")
        qa_data["Answer"].append(answer)

# Convert to Excel
if st.button("💾 Excel मध्ये सेव्ह करा"):
    if qa_data["Question"] and qa_data["Answer"]:
        df = pd.DataFrame(qa_data)
        df.to_excel("marathi_qa_data.xlsx", index=False)
        st.success("✅ डेटा यशस्वीरित्या सेव्ह केला!")
    else:
        st.warning("⚠️ कृपया किमान एक प्रश्न आणि उत्तर द्या!")

# Download Excel
with open("marathi_qa_data.xlsx", "rb") as file:
    st.download_button(label="⬇️ Excel डाउनलोड करा", data=file, file_name="marathi_qa_data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
