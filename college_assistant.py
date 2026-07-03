"""
+============================================================================+
|              AI-POWERED COLLEGE ASSISTANT                                   |
|              LangChain Tool Calling Agent                                   |
|                                                                            |
|  Tools  : Attendance, Result, Fee Balance, Library Fine, Hostel Fee,       |
|           Student Info (Bonus)                                             |
|  LLM    : OpenAI GPT-4o-mini                                              |
|  Agent  : create_tool_calling_agent + AgentExecutor (verbose=True)         |
+============================================================================+
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from langchain_openai import ChatOpenAI
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

STUDENT_DB = {
    "STU001": {"name": "Yashwanth",  "branch": "CSE",   "year": 3, "cgpa": 8.9, "email": "yashwanth@college.edu"},
    "STU002": {"name": "Ananya",     "branch": "ECE",   "year": 2, "cgpa": 9.2, "email": "ananya@college.edu"},
    "STU003": {"name": "Rahul",      "branch": "MECH",  "year": 4, "cgpa": 7.5, "email": "rahul@college.edu"},
    "STU004": {"name": "Priya",      "branch": "IT",    "year": 1, "cgpa": 8.1, "email": "priya@college.edu"},
    "STU005": {"name": "Karthik",    "branch": "CIVIL", "year": 3, "cgpa": 6.8, "email": "karthik@college.edu"},
}

@tool
def attendance_calculator(total_classes: int, attended_classes: int) -> str:
    """Calculate attendance percentage and determine exam eligibility.
    Use this when the student provides total classes and attended classes
    and wants to know their attendance percentage or exam eligibility status.
    """
    percentage = (attended_classes / total_classes) * 100
    eligible = percentage >= 75

    status_line = "[+] Status : ELIGIBLE for Exam" if eligible else "[-] Status : NOT ELIGIBLE for Exam"
    note_line = "    (Attendance >= 75%)" if eligible else "    (Attendance < 75% -- Minimum required: 75%)"

    return (
        f"\n{'='*50}\n"
        f"       ATTENDANCE REPORT\n"
        f"{'='*50}\n"
        f"  Total Classes    : {total_classes}\n"
        f"  Classes Attended : {attended_classes}\n"
        f"  Attendance       : {percentage:.2f}%\n"
        f"  {status_line}\n"
        f"  {note_line}\n"
        f"{'='*50}\n"
    )

@tool
def result_calculator(subject1: float, subject2: float, subject3: float, subject4: float, subject5: float) -> str:
    """Calculate the average marks, grade, and pass/fail status from marks of 5 subjects.
    Use this when the student provides marks for 5 subjects and wants to know
    their average, grade (A/B/C/D), or pass/fail status.
    """
    marks = [subject1, subject2, subject3, subject4, subject5]
    average = sum(marks) / len(marks)

    if average >= 90:
        grade = "A"
    elif average >= 75:
        grade = "B"
    elif average >= 60:
        grade = "C"
    else:
        grade = "D"

    passed = average >= 50
    result_line = "[+] Result : PASS" if passed else "[-] Result : FAIL"

    return (
        f"\n{'='*50}\n"
        f"       RESULT CARD\n"
        f"{'='*50}\n"
        f"  Subject 1 : {marks[0]}\n"
        f"  Subject 2 : {marks[1]}\n"
        f"  Subject 3 : {marks[2]}\n"
        f"  Subject 4 : {marks[3]}\n"
        f"  Subject 5 : {marks[4]}\n"
        f"  {'-'*40}\n"
        f"  Average   : {average:.2f}\n"
        f"  Grade     : {grade}\n"
        f"  {result_line}\n"
        f"{'='*50}\n"
    )

@tool
def fee_balance_calculator(total_fee: float, amount_paid: float) -> str:
    """Calculate the pending fee balance.
    Use this when the student provides total course fee and the amount already paid,
    and wants to know how much fee is still pending.
    """
    pending = total_fee - amount_paid

    if pending == 0:
        note = "  All fees cleared!"
    else:
        note = "  Please clear the balance soon."

    return (
        f"\n{'='*50}\n"
        f"       FEE STATEMENT\n"
        f"{'='*50}\n"
        f"  Total Course Fee : Rs.{total_fee:,.2f}\n"
        f"  Amount Paid      : Rs.{amount_paid:,.2f}\n"
        f"  {'-'*40}\n"
        f"  Pending Fee      : Rs.{pending:,.2f}\n"
        f"  {note}\n"
        f"{'='*50}\n"
    )

@tool
def library_fine_calculator(delayed_days: int) -> str:
    """Calculate the library fine for delayed book return.
    Use this when the student mentions how many days late they returned a library book.
    Fine is calculated as Rs.5 per delayed day.
    """
    fine = 5 * delayed_days

    return (
        f"\n{'='*50}\n"
        f"       LIBRARY FINE RECEIPT\n"
        f"{'='*50}\n"
        f"  Days Delayed  : {delayed_days} day(s)\n"
        f"  Rate          : Rs.5 per day\n"
        f"  {'-'*40}\n"
        f"  Total Fine    : Rs.{fine:,.2f}\n"
        f"  Please pay at the library counter.\n"
        f"{'='*50}\n"
    )

@tool
def hostel_fee_calculator(monthly_fee: float, months_stayed: int) -> str:
    """Calculate total hostel fee based on monthly fee and duration of stay.
    Use this when the student provides monthly hostel fee and number of months stayed,
    and wants to know the total hostel fee payable.
    """
    total = monthly_fee * months_stayed

    return (
        f"\n{'='*50}\n"
        f"       HOSTEL FEE STATEMENT\n"
        f"{'='*50}\n"
        f"  Monthly Fee    : Rs.{monthly_fee:,.2f}\n"
        f"  Months Stayed  : {months_stayed}\n"
        f"  {'-'*40}\n"
        f"  Total Fee      : Rs.{total:,.2f}\n"
        f"{'='*50}\n"
    )

@tool
def student_info_lookup(student_id: str) -> str:
    """Retrieve student details from the database using their Student ID.
    Use this when the user asks for student information or details and provides
    a Student ID like STU001, STU002, etc.
    """
    student_id = student_id.upper().strip()
    student = STUDENT_DB.get(student_id)

    if not student:
        available = ", ".join(STUDENT_DB.keys())
        return (
            f"\n[!] Student ID '{student_id}' not found in the database.\n"
            f"    Available IDs: {available}\n"
        )

    return (
        f"\n{'='*50}\n"
        f"       STUDENT INFORMATION\n"
        f"{'='*50}\n"
        f"  Student ID  : {student_id}\n"
        f"  Name        : {student['name']}\n"
        f"  Branch      : {student['branch']}\n"
        f"  Year        : {student['year']}\n"
        f"  CGPA        : {student['cgpa']}\n"
        f"  Email       : {student['email']}\n"
        f"{'='*50}\n"
    )

import os
llm = ChatOpenAI(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a smart College Assistant AI. Your job is to help students "
        "with attendance checks, result calculations, fee queries, library fines, "
        "hostel fees, and student information lookups. "
        "Use the available tools to answer every query accurately. "
        "When the student asks multiple things in one message, invoke ALL "
        "the relevant tools and provide a consolidated response."
    ),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

tools = [
    attendance_calculator,
    result_calculator,
    fee_balance_calculator,
    library_fine_calculator,
    hostel_fee_calculator,
    student_info_lookup,
]

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

test_queries = [
    "I attended 72 classes out of 90. Am I eligible for exams?",
    "My marks are 95, 90, 88, 91 and 87. What is my grade?",
    "My course fee is 50000 and I have paid 35000. How much fee is pending?",
    "I returned a library book 8 days late. What is the fine amount?",
    "Hostel fee is 6000 per month and I stayed for 5 months. Calculate my hostel fee.",

    (
        "I attended 80 classes out of 100. "
        "My marks are 90, 85, 88, 92 and 95. "
        "My course fee is 60000 and I paid 45000. "
        "Provide: 1. Attendance Status 2. Grade 3. Pending Fee"
    ),

    "Get me the details of student with ID STU002",
]

def main():
    """Execute all test queries and display results."""
    print("\n" + "=" * 78)
    print("  AI-POWERED COLLEGE ASSISTANT -- LangChain Tool Calling Agent")
    print("  Tools: 6 | LLM: OpenAI-Compatible (Llama-3.1) | verbose=True")
    print("=" * 78)

    for i, query in enumerate(test_queries, 1):
        if i == 6:
            label = "MULTI-TOOL CHALLENGE"
        elif i == 7:
            label = "BONUS CHALLENGE"
        else:
            label = f"TEST CASE {i}"

        print(f"\n{'='*78}")
        print(f"  >> {label}")
        print(f"  Query: {query}")
        print(f"{'='*78}\n")

        response = agent_executor.invoke({"input": query})

        print(f"\n{'-'*78}")
        print(f"  Agent Response:")
        print(f"{'-'*78}")
        print(response["output"])
        print(f"{'-'*78}\n")

if __name__ == "__main__":
    main()
