<h1 align="center">🎓 AI-Powered College Assistant</h1>

<p align="center">
  <strong>A LangChain Tool-Calling Agent designed to automate and assist with student queries!</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/LangChain-Enabled-green?logo=langchain&logoColor=white" alt="LangChain">
  <img src="https://img.shields.io/badge/LLM-Llama--3.1-orange?logo=openai&logoColor=white" alt="LLM">
</p>

---

## 📖 Overview

The **AI-Powered College Assistant** is an intelligent agent built using Python and the `langchain_classic.agents` module. It seamlessly interprets natural language student queries and dynamically routes them to the correct, specialized tools to compute attendance, results, fees, fines, and student details. 

When a user asks complex or multi-part questions, the agent is smart enough to invoke multiple tools in a single execution loop and consolidate the final response!

## 🛠️ Features & Tools

The Assistant is equipped with **6 specialized tools** (defined via LangChain's `@tool` decorator):

1. **📊 Attendance Calculator** - Calculates attendance percentage and determines exam eligibility (Minimum 75% required).
2. **🎓 Result Calculator** - Takes marks from 5 subjects to compute the average, determine the grade (A/B/C/D), and evaluate Pass/Fail status.
3. **💰 Fee Balance Calculator** - Calculates pending course fees based on total fees and the amount paid.
4. **📚 Library Fine Calculator** - Automatically computes fines for late book returns (₹5 per delayed day).
5. **🏠 Hostel Fee Calculator** - Computes total hostel fees based on the monthly rate and stay duration.
6. **🧑‍🎓 Student Info Lookup** *(Bonus)* - Looks up detailed student profiles from a simulated database using their Student ID.

## 🚀 Technical Stack

- **Framework**: LangChain (`create_tool_calling_agent`, `AgentExecutor`, `ChatPromptTemplate`)
- **LLM**: Groq's blazing-fast OpenAI-compatible API (`llama-3.1-8b-instant`)
- **Language**: Python 3.x
- **Output**: Beautifully formatted terminal outputs using UTF-8 ASCII-style cards.

## 💻 How to Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/samyashwanth7/AI-College-Assistant.git
   cd AI-College-Assistant
   ```

2. **Install the dependencies:**
   ```bash
   pip install langchain langchain-openai langchain-classic python-docx
   ```

3. **Set your API Key:**
   Get a free API key from [Groq](https://console.groq.com/keys) and set it as an environment variable.
   *Windows (PowerShell):*
   ```powershell
   $env:GROQ_API_KEY="your-api-key-here"
   ```

4. **Run the Assistant:**
   ```bash
   python college_assistant.py
   ```

## 🧪 Test Cases Supported

The script includes a comprehensive test suite covering 7 distinct cases, ranging from single-tool invocations to a **Multi-Tool Challenge** where the agent flawlessly executes three tools concurrently to answer a combined query!

---
*Created as part of an AI Agent assignment.*
