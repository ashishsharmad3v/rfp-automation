import openai
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches
import json

# --- 1. Set up OpenAI API Key ---
# Make sure to securely store your API key
openai.api_key = 'your_openai_api_key_here'

# --- 2. Load Data from Knowledge Base ---
# In a real app, this would be a database query.
# Here, we use a JSON file for simplicity.
with open('knowledge_base.json', 'r', encoding='utf-8') as f:
    knowledge_base = json.load(f)

def get_fund_data(fund_name):
    """Fetches data for a specific fund from the knowledge base."""
    return knowledge_base['funds'].get(fund_name)

def get_qa_by_topic(topic):
    """Fetches Q&A pairs for a given topic."""
    return knowledge_base['questions'].get(topic, [])

# --- 3. Define AI Prompting Function ---
def generate_ai_text(prompt, context_data):
    """
    Sends a prompt to OpenAI's API with context data for customization.
    """
    full_prompt = f"""
    You are an expert financial proposal writer for a leading Indian mutual fund.
    Generate a professional and compelling text based on the following context and instructions.
    Ensure all content is factual and compliant with standard disclaimers.

    Context: {json.dumps(context_data, indent=2, ensure_ascii=False)}

    Instruction: {prompt}

    Output:
    """
    
    response = openai.chat.completions.create(
        model="gpt-4o", # Recommended for its advanced capabilities
        messages=[
            {"role": "system", "content": "You are a professional financial proposal writer."},
            {"role": "user", "content": full_prompt}
        ],
        temperature=0.7, # Adjust for creativity (0.0 for factual)
        max_tokens=1500 # Control output length
    )
    return response.choices[0].message.content.strip()

# --- 4. Main Proposal Generation Logic ---
def generate_proposal(fund_name, client_profile, emphasis_keywords):
    # Load your Jinja2-enabled template from a .docx file
    doc = DocxTemplate('proposal_template.docx')

    # Get data from your knowledge base
    fund_data = get_fund_data(fund_name)
    firm_data = knowledge_base['firm_info']
    
    if not fund_data:
        raise ValueError(f"Fund '{fund_name}' not found in knowledge base.")
        
    # --- Use OpenAI to generate custom content ---
    # Generate an executive summary tailored to the client and emphasis
    executive_summary_prompt = f"""
    Write a 250-word executive summary for a proposal to a {client_profile['type']} client.
    The client is particularly interested in {' and '.join(emphasis_keywords)}.
    Highlight key facts from the fund data.
    """
    executive_summary = generate_ai_text(executive_summary_prompt, {'fund': fund_data, 'firm': firm_data})

    # Generate a tailored risk management section if requested
    risk_management_section = ""
    if 'Risk Management' in emphasis_keywords:
        risk_management_prompt = f"""
        Elaborate on our risk management philosophy using the following details: {fund_data['risk_management_details']}.
        Explain how our process provides robust downside protection for a client like a {client_profile['type']}.
        """
        risk_management_section = generate_ai_text(risk_management_prompt, {'fund': fund_data})
        
    # Get Q&A for the compliance section
    compliance_qa = get_qa_by_topic('Compliance')
    # You can even use OpenAI to rephrase answers for better flow
    
    # --- 5. Populate the template with data and generated content ---
    context = {
        'fund_name': fund_data['name'],
        'client_name': client_profile['name'],
        'executive_summary': executive_summary,
        'firm_history': firm_data['history'],
        'fund_objective': fund_data['objective'],
        'fund_manager_name': fund_data['fund_manager'],
        'performance_table': fund_data['performance_data'], # Pass as a table-like structure for Jinja2
        'risk_management_section': risk_management_section,
        'compliance_qa': compliance_qa,
        # ... and all other data points
    }

    # Render the document
    doc.render(context)
    
    # Save the final document
    output_filename = f"Proposal_for_{client_profile['name']}_{fund_name}_{datetime.now().strftime('%Y%m%d')}.docx"
    doc.save(output_filename)
    
    print(f"Proposal generated successfully: {output_filename}")
    return output_filename

# --- Example Usage ---
# You would get this from your UI
client_info = {
    'name': 'Kurukshetra Pension Fund',
    'type': 'Pension Fund'
}
emphasis = ['Risk Management', 'ESG']

# Run the generation process
generated_file = generate_proposal('ABC Equity Fund', client_info, emphasis)