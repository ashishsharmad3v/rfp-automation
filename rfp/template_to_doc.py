from docxtpl import DocxTemplate, InlineImage
from docx.shared import Cm
from docx2pdf import convert
import datetime
import os
import io

def generate_rfp_pdf(template_path="rfp_template.docx", output_docx_path="ABC_Trust_RFP.docx", output_pdf_path="ABC_Trust_RFP.pdf", logo_url="https://placehold.co/200x200/DDDDDD/666666?text=ABC+Trust+Logo"):
    """
    Generates an RFP document in DOCX and then converts it to PDF.

    Args:
        template_path (str): Path to the Jinja2-enabled .docx template.
                            NOTE: This template file should be created manually
                            with the desired base formatting (like the light
                            gradient background on all pages) and appropriate
                            header/footer sections.
        output_docx_path (str): Path to save the generated .docx file.
        output_pdf_path (str): Path to save the converted .pdf file.
        logo_url (str): URL for the logo image to be included on the first page header.
    """
    try:
        # 1. Prepare Context Data for the Template
        # This data would typically come from your FastAPI backend after processing
        # uploaded RFPs and synthesizing information.
        context = {
            "current_date": datetime.date.today().strftime("%B %d, %Y"),
            "executive_summary_content": (
                "ABC Trust invites proposals from qualified investment service providers "
                "to manage our growing endowment fund. We seek a partner who can "
                "demonstrate a robust investment philosophy, a strong commitment to "
                "fiduciary responsibility, and a proven track record of aligning "
                "investment strategies with the unique needs of non-profit organizations. "
                "This RFP outlines our requirements and evaluation criteria."
            ),
            "firm_overview_content": (
                "This section requests fundamental information about your firm, including "
                "its legal structure, history, and overall scope of services that would "
                "be relevant to ABC Trust. Understanding your firm's foundation is crucial."
            ),
            "firm_overview_questions": [
                "Provide full legal name, contact info for main and servicing offices, and primary representative.",
                "Describe firm's background, history, and ownership structure.",
                "Outline the scope of investment services your firm would provide to ABC Trust.",
                "Detail your firm's total Assets Under Management (AUM) and client base composition (types, nonprofit clients, length of service, asset value range for nonprofits).",
                "Highlight key strengths distinguishing your firm from competitors.",
                "Describe any other value-added services beneficial to ABC Trust."
            ],
            "client_servicing_content": (
                "Detail your approach to client relationship management, emphasizing the structure "
                "and philosophy behind the team dedicated to servicing our organization."
            ),
            "client_servicing_questions": [
                "Describe the structure of the team supporting ABC Trust and provide biographies for key individuals.",
                "Articulate your firm's customer service philosophy.",
                "Specify frequency and typical topics for meetings with ABC Trust's investment committee."
            ],
            "investment_philosophy_content": (
                "This section is critical to understanding your firm's core beliefs and methodologies "
                "in managing investments. Provide insights into your strategic approach, policy development, "
                "and risk management framework."
            ),
            "investment_philosophy_questions": [
                "Explain your investment philosophy and provide an overview of your investment process.",
                "Describe your approach to developing/revising investment policy statements for non-profit organizations and monitoring compliance.",
                "Outline your process for developing an asset allocation model.",
                "Detail your firm's approach to risk management.",
                "Describe your portfolio construction methodology."
            ],
            "investment_manager_content": (
                "We seek to understand your rigorous process for identifying, evaluating, and selecting "
                "investment managers. Your due diligence capabilities are of paramount importance."
            ),
            "investment_manager_questions": [
                "Briefly describe your research organization and the number of individuals dedicated to investment manager due diligence.",
                "Provide a detailed description of your firm's investment manager evaluation and selection process.",
                "Describe the database used for manager search and selection (in-house/third-party, number of managers, update frequency, fee for inclusion).",
                "Explain your process for placing a manager on 'watch' and/or terminating a manager."
            ],
            "performance_reporting_content": (
                "Transparency and clarity in performance reporting are essential for ABC Trust. "
                "This section addresses your capabilities in providing accurate and timely reports."
            ),
            "performance_reporting_questions": [
                "Describe your standard performance reporting package for institutional clients.",
                "How frequently are performance reports provided, and what is the typical turnaround time?",
                "Do your reports comply with GIPS standards or other industry benchmarks?",
                "Can you customize reports to include specific metrics or analyses as requested by ABC Trust?"
            ],
            "compliance_content": (
                "Compliance with regulatory standards and a robust framework for managing conflicts of interest "
                "are non-negotiable for ABC Trust. Detail your policies and historical compliance."
            ),
            "compliance_questions": [
                "Describe how your firm manages conflicts of interest.",
                "Confirm RIA registration under the Investment Advisers Act of 1940 and willingness to accept fiduciary responsibility.",
                "Disclose any non-routine SEC/regulatory inquiries, investigations, or litigation concerning fiduciary responsibility in the past five years.",
                "Provide levels for Errors and Omissions (E&O) insurance and any other fiduciary or professional liability insurance."
            ],
            "fees_content": (
                "Provide a comprehensive breakdown of all fees associated with your investment services, "
                "including management fees, administrative costs, and any other potential charges. "
                "Transparency in pricing is highly valued by ABC Trust."
            ),
            "fees_questions": [
                "Outline your proposed fee structure for the services described in this RFP.",
                "Provide a detailed breakdown of all fees, including management fees, administrative fees, performance fees (if any), and any other potential charges.",
                "Are there any additional fees for specific services (e.g., special reporting, ad-hoc meetings)?",
                "Describe your invoicing process and payment terms.",
                "Are your fees negotiable based on AUM or scope of services?"
            ]
        }

        # Handle logo image for the first page header
        # Fetch the image (simulate for a URL, or use a local path)
        # Note: python-docx-template's InlineImage expects a path to a local file.
        # For a URL, you'd download it first. Here, using a placeholder URL directly.
        context['logo_path'] = logo_url # The template will call {% image logo_path %}

        # 2. Load the template and render
        doc = DocxTemplate(template_path)
        doc.render(context)

        # 3. Save the generated DOCX file
        doc.save(output_docx_path)
        print(f"DOCX document generated: {output_docx_path}")

        # 4. Convert DOCX to PDF
        # Ensure that LibreOffice or Microsoft Word is installed on the system
        # where docx2pdf is run, as it relies on these applications for conversion.
        convert(output_docx_path, output_pdf_path)
        print(f"PDF document generated: {output_pdf_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure 'rfp_template.docx' exists and has the necessary Jinja2 placeholders.")
        print("Also, ensure LibreOffice or Microsoft Word is installed for docx2pdf conversion.")

# Example usage:
if __name__ == "__main__":
    # Create a dummy template.docx file for demonstration.
    # In a real scenario, you would create this manually in Word with the
    # Jinja2 placeholders from the markdown immersive and save it as rfp_template.docx
    dummy_template_content = """
    {% comment %}
    This is a dummy DOCX template content.
    For a real application, create a DOCX file in Word and paste the Jinja2 template content
    from the markdown immersive into it, then save it as 'rfp_template.docx'.
    Ensure headers, footers, and page number fields are properly set up in Word.
    The header/footer image and page number fields require specific Word XML for proper rendering
    by python-docx-template. This example focuses on the Jinja2 logic.
    {% endcomment %}

    {{ super_context }}

    {# Main content sections will go here #}
    {{ executive_summary_content }}
    
    1. Firm Overview
    {{ firm_overview_content }}
    {% for question in firm_overview_questions %}
    - {{ question }}
    {% endfor %}

    2. Client Servicing Team
    {{ client_servicing_content }}
    {% for question in client_servicing_questions %}
    - {{ question }}
    {% endfor %}

    3. Investment Philosophy and Process
    {{ investment_philosophy_content }}
    {% for question in investment_philosophy_questions %}
    - {{ question }}
    {% endfor %}

    4. Investment Manager Research and Selection
    {{ investment_manager_content }}
    {% for question in investment_manager_questions %}
    - {{ question }}
    {% endfor %}

    5. Performance Reporting
    {{ performance_reporting_content }}
    {% for question in performance_reporting_questions %}
    - {{ question }}
    {% endfor %}

    6. Compliance and Conflict of Interest
    {{ compliance_content }}
    {% for question in compliance_questions %}
    - {{ question }}
    {% endfor %}

    7. Fees
    {{ fees_content }}
    {% for question in fees_questions %}
    - {{ question }}
    {% endfor %}

    {# The header, footer, and disclaimer logic for specific pages (first/last)
       must be set up within the actual Word document's header/footer sections
       using Word's built-in "Different First Page" and "Different Odd & Even Pages"
       features, combined with Jinja2 for conditional content.
       The page numbering fields need to be Word's native PAGE/NUMPAGES fields.
       For the logo: Insert a placeholder image in the first page header in Word,
       then set its alt text or a custom property to "logo_path" so docxtpl can find it.
       Alternatively, use {% render_docx_image(logo_path) %} as shown in the markdown.
       This dummy content cannot replicate that complexity.
    #}
    """
    
    # Save dummy template content to a file to be used by DocxTemplate
    # In a real scenario, you would have a pre-formatted DOCX file
    # with the Jinja2 syntax for headers/footers and content.
    if not os.path.exists("rfp_template.docx"):
        # This is a very basic dummy. For full functionality, you need a .docx
        # created in MS Word or LibreOffice with proper headers/footers/page numbers.
        # This basic save will not create the advanced header/footer features.
        from docx import Document
        doc = Document()
        doc.add_paragraph(dummy_template_content)
        doc.save("rfp_template_basic_dummy.docx")
        print("A basic dummy template 'rfp_template_basic_dummy.docx' has been created.")
        print("For advanced header/footer/image/page numbering, please manually create 'rfp_template.docx' in Word/LibreOffice with the Jinja2 content provided in the markdown immersive.")
        template_file_to_use = "rfp_template_basic_dummy.docx"
    else:
        template_file_to_use = "rfp_template.docx"
        print("Using existing 'rfp_template.docx'. Ensure it's correctly set up with Jinja2 and Word features.")

    # Call the generation function
    generate_rfp_pdf(template_path=template_file_to_use)

