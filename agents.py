from typing import Dict, List, Any, Optional
import os
import json
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Constants for prompts
LEGAL_ANALYSIS_PROMPT = """
You are an expert legal analyst. Review the following contract and provide a thorough legal analysis:

CONTRACT:
{contract_text}

Your analysis should cover:
1. Overall contract structure and completeness
2. Key terms and definitions
3. Obligations and responsibilities of each party
4. Rights and remedies
5. Risk allocation between parties
6. Regulatory compliance
7. Missing or problematic elements

Format your response with clear headings and provide specific references to sections where relevant.
Conclude with an overall legal risk assessment (Low, Medium, or High).
"""

RISK_ASSESSMENT_PROMPT = """
You are a risk assessment specialist. Based on this contract, provide a comprehensive risk assessment:

CONTRACT:
{contract_text}

LEGAL ANALYSIS:
{legal_analysis}

Your assessment should:
1. Identify and categorize all potential risks (legal, financial, operational, reputational)
2. Rate each risk on a scale of Low, Medium, or High
3. Explain the potential impact of each risk
4. Prioritize the most serious risks that require attention

Format your response with clear categories and use bullet points where appropriate.
"""

RECOMMENDATIONS_PROMPT = """
You are a contract optimization specialist. Based on the analysis of this contract, provide specific recommendations:

CONTRACT:
{contract_text}

LEGAL ANALYSIS:
{legal_analysis}

RISK ASSESSMENT:
{risk_assessment}

Your recommendations should:
1. Suggest specific alternative language for problematic clauses
2. Propose additional clauses to address identified gaps
3. Recommend structural improvements for clarity
4. Prioritize recommendations by importance (Critical, Important, Advisable)

Focus on practical, implementable changes that address the highest priority issues.
"""

SUMMARY_PROMPT = """
Create a concise executive summary of this contract analysis:

LEGAL ANALYSIS:
{legal_analysis}

RISK ASSESSMENT:
{risk_assessment}

RECOMMENDATIONS:
{recommendations}

Your summary should:
1. Highlight the 3-5 most critical findings
2. Summarize the overall risk level (Low, Medium, High)
3. Provide key recommendations
4. Use clear, non-technical language suitable for executives

Keep your summary to 300-500 words.
"""

EXTRACT_CLAUSES_PROMPT = """
Identify and extract the 5-7 most important clauses from this contract:

CONTRACT:
{contract_text}

For each clause:
1. Extract the exact text of the clause (or a concise version if very long)
2. Identify the type of clause (e.g., Indemnification, Termination, Liability)
3. Rate its importance (High, Medium, Low)
4. Provide a brief explanation of why this clause is important or potentially problematic

Format each clause as a separate section with clear headings.
"""

def load_document(file_path: str) -> str:
    """
    Load a document from file path and extract its text.
    
    Args:
        file_path: Path to the document file
        
    Returns:
        str: The text content of the document
        
    Raises:
        ValueError: If the file type is not supported
    """
    # Determine file type and use appropriate loader
    if file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith('.docx'):
        loader = Docx2txtLoader(file_path)
    elif file_path.endswith('.txt'):
        loader = TextLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")
    
    # Load the document
    documents = loader.load()
    
    # Extract text
    text = ""
    for doc in documents:
        text += doc.page_content + "\n\n"
    
    return text.strip()

def analyze_contract(
    contract_text: str, 
    model_name: str = "gpt-4", 
    max_tokens: int = 2000
) -> Dict[str, Any]:
    """
    Analyze a contract using LangChain and OpenAI models.
    
    Args:
        contract_text: The text content of the contract
        model_name: Name of the OpenAI model to use
        max_tokens: Maximum tokens to use for analysis
        
    Returns:
        Dict: Analysis results including legal analysis, risk assessment, etc.
        
    Raises:
        ValueError: If contract_text is empty or too short
        Exception: For any errors during analysis
    """
    # Validate input
    if not contract_text or len(contract_text.strip()) < 100:
        raise ValueError("Contract text is too short or empty")
    
    try:
        # Initialize the language model
        llm = ChatOpenAI(
            model_name=model_name,
            temperature=0.1,
            max_tokens=max_tokens
        )
        
        # Prepare contract text - trim if too long
        # Get roughly first 80% of the document to fit in context window
        contract_for_analysis = contract_text[:int(len(contract_text) * 0.8)]
        
        # Step 1: Legal Analysis
        legal_analysis_prompt = PromptTemplate(
            input_variables=["contract_text"],
            template=LEGAL_ANALYSIS_PROMPT
        )
        legal_analysis_chain = LLMChain(llm=llm, prompt=legal_analysis_prompt)
        legal_analysis = legal_analysis_chain.run(contract_text=contract_for_analysis)
        
        # Step 2: Risk Assessment
        risk_assessment_prompt = PromptTemplate(
            input_variables=["contract_text", "legal_analysis"],
            template=RISK_ASSESSMENT_PROMPT
        )
        risk_assessment_chain = LLMChain(llm=llm, prompt=risk_assessment_prompt)
        risk_assessment = risk_assessment_chain.run(
            contract_text=contract_for_analysis,
            legal_analysis=legal_analysis
        )
        
        # Step 3: Recommendations
        recommendations_prompt = PromptTemplate(
            input_variables=["contract_text", "legal_analysis", "risk_assessment"],
            template=RECOMMENDATIONS_PROMPT
        )
        recommendations_chain = LLMChain(llm=llm, prompt=recommendations_prompt)
        recommendations = recommendations_chain.run(
            contract_text=contract_for_analysis,
            legal_analysis=legal_analysis,
            risk_assessment=risk_assessment
        )
        
        # Step 4: Summary
        summary_prompt = PromptTemplate(
            input_variables=["legal_analysis", "risk_assessment", "recommendations"],
            template=SUMMARY_PROMPT
        )
        summary_chain = LLMChain(llm=llm, prompt=summary_prompt)
        summary = summary_chain.run(
            legal_analysis=legal_analysis,
            risk_assessment=risk_assessment,
            recommendations=recommendations
        )
        
        # Step 5: Extract Key Clauses
        clauses_prompt = PromptTemplate(
            input_variables=["contract_text"],
            template=EXTRACT_CLAUSES_PROMPT
        )
        clauses_chain = LLMChain(llm=llm, prompt=clauses_prompt)
        clauses_text = clauses_chain.run(contract_text=contract_for_analysis)
        
        # Process the clauses text into structured format
        clauses = extract_structured_clauses(clauses_text)
        
        # Compile the results
        results = {
            "legal_analysis": legal_analysis,
            "risk_assessment": risk_assessment,
            "recommendations": recommendations,
            "summary": summary,
            "clauses": clauses
        }
        
        return results
        
    except Exception as e:
        print(f"Error in contract analysis: {str(e)}")
        raise Exception(f"Contract analysis failed: {str(e)}")

def extract_structured_clauses(clauses_text: str) -> List[Dict[str, str]]:
    """
    Extract structured clauses from the text output of the clause analysis.
    
    Args:
        clauses_text: Text containing clause analysis
        
    Returns:
        List of dictionaries, each representing a clause
    """
    import re
    
    # Initialize list for structured clauses
    structured_clauses = []
    
    # Split text into sections for each clause
    # Look for patterns like numbered sections or headings
    clause_sections = re.split(r'(?:\d+\.|\*\*|\#|\n\n)', clauses_text)
    
    for section in clause_sections:
        section = section.strip()
        if not section:
            continue
            
        # Extract information using regex patterns
        clause_text_match = re.search(r'(?:clause text|text|clause):\s*(.+?)(?:\n|$)', 
                                    section, re.IGNORECASE | re.DOTALL)
        
        clause_type_match = re.search(r'(?:type|clause type):\s*(.+?)(?:\n|$)', 
                                    section, re.IGNORECASE)
        
        importance_match = re.search(r'(?:importance):\s*(high|medium|low)', 
                                    section, re.IGNORECASE)
        
        explanation_match = re.search(r'(?:explanation|analysis):\s*(.+?)(?:\n\n|$)', 
                                    section, re.IGNORECASE | re.DOTALL)
        
        # If we found a clause text, create a clause entry
        if clause_text_match or (clause_type_match and importance_match):
            clause = {}
            
            # Get clause text, or use first paragraph if not found
            if clause_text_match:
                clause["clause_text"] = clause_text_match.group(1).strip()
            else:
                # Use first paragraph as fallback
                paragraphs = [p for p in section.split('\n') if p.strip()]
                if paragraphs:
                    clause["clause_text"] = paragraphs[0].strip()
                else:
                    continue  # Skip if no content
            
            # Get clause type
            if clause_type_match:
                clause["clause_type"] = clause_type_match.group(1).strip()
            else:
                clause["clause_type"] = "Unspecified Clause"
            
            # Get importance
            if importance_match:
                clause["importance"] = importance_match.group(1).capitalize()
            else:
                clause["importance"] = "Medium"
            
            # Get explanation if available
            if explanation_match:
                clause["explanation"] = explanation_match.group(1).strip()
            
            structured_clauses.append(clause)
    
    # If no clauses were extracted, create a generic one
    if not structured_clauses:
        # Try to extract meaningful paragraphs
        paragraphs = [p for p in clauses_text.split('\n\n') if len(p.strip()) > 50]
        
        if paragraphs:
            # Use paragraphs as clauses
            for i, paragraph in enumerate(paragraphs[:5]):
                structured_clauses.append({
                    "clause_text": paragraph.strip(),
                    "clause_type": f"Contract Section {i+1}",
                    "importance": "Medium",
                    "explanation": "Automatically extracted from contract text"
                })
        else:
            # Fallback if nothing could be extracted
            structured_clauses.append({
                "clause_text": "No specific clauses could be identified in this contract",
                "clause_type": "General Contract",
                "importance": "Medium",
                "explanation": "Please review the full contract for details"
            })
    
    return structured_clauses