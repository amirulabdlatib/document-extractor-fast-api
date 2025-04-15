from typing import Optional, Type
from pydantic import BaseModel, Field

class BorrowerInformation(BaseModel):
    """Contains information about the borrower."""
    borrower_name: Optional[str] = Field(None, description="The full name of the SAINT IMAGE GRAPHICS SDN. BHD., if more than one seperate them by commas ")
    borrower_registration_number: Optional[str] = Field(None, description="The full Malaysian Registration No. or Malaysian NRIC or passport number or old IC number of the borrower or joint borrowers, if more than one seperate them by commas")
    borrower_address: Optional[str] = Field(None, description="The full address of the SAINT IMAGE GRAPHICS SDN. BHD. ")
    borrower_postcode: Optional[str] = Field(None, description="The 5 digit postcode of address for example 68100")


class BankInformation(BaseModel):
    """Contains information about the bank."""
    bank_name: Optional[str] = Field(None, description="The official name of a bank operating in Malaysia. Must be one of the following: ""'CIMB', 'UOB', 'Maybank', 'ALLIANCE', 'Public Bank', or 'Standard Chartered'. ""If the extracted name is different or informal, map it to the closest valid Malaysian bank name.")
    bank_address: Optional[str] = Field(None, description="The address of the bank. Hint: look for branch keywords to identify the full address")
    bank_registeration_number: Optional[str] = Field(None, description="The registeration number of the bank.")


class LoanInformation(BaseModel):
    """Contains information about the loan."""
    loan_amount: Optional[str] = Field(None, description="The mentioned total approved limit in RM, hint: the largest number found")
    letter_offer_date: Optional[str] = Field(None, description="Look for the date closest to the subject of 'Letter of Offer' or a phrase like 'Our Reference' or 'Our Ref' or 'Date:'."
                                                                "Stricly only one complete date allowed. Hint: it label as Date:")


class FacilityInformation(BaseModel):
    facility: Optional[str] = Field(
        None,
        description=(
            "Extract ONLY the full and exact wording of all approved banking facilities listed in Section 1. "
            "Do not extract any information from other sections. "
            "The extracted text must match the original text **verbatim**, including all monetary values, phrases, and formatting. "
            "Do not rephrase, summarize, correct, or alter any part of the facility descriptions. "
            "Each facility (e.g., Term Loan, Overdraft, Bank Guarantee, Housing Loan) must be captured with full details including any specified amount, purpose, interest rate, limit, tenure, repayment terms, or usage conditions. "
            "If multiple facilities are listed, concatenate all of them into one string and separate them strictly with a **single comma** followed by a space. "
            "Use **only** commas and full stops as separators—remove semicolons, bullet points, special characters, or any other formatting symbols. "
            "Do not add explanatory phrases or annotations. "
            "Example output 1: 'Housing Loan ('HL') of Ringgit Malaysia Eight Hundred Thirty Five Thousand Ninety One only'"
            "Example output 2, example for multiple: 'Cashline Facility-i (CLF-i) - RM 1,000,000.00, Cashline Facility-i (CLF-i2) - RM 2,000,000.00, Commodity Murabahah Term Financing-i 1 - RM 3,543,566.23, Commodity Murabahah Term Financing-i 2 - RM 270,431.86, Commodity Murabahah Term Financing-i 3 - RM 51,704.87, Commodity Murabahah Term Financing-i 4 - RM 11,000,000.00, and Commodity Murabahah Term Financing-i 5 - RM 113,907.00. Total loan amount - RM 17,979,609.96.' "
        )
    )


class PropertyInformation(BaseModel):
    property_address: Optional[str] = Field(
        None,
        description=(
            "Extract ONLY the full and exact wording of the property address as mentioned in the security section, "
            "typically after phrases like 'a/an CONDOMINIUM known as'. "
            "Ignore surrounding information such as loan amount, car-park details, accessory parcels, or legal terms. "
            "Do not include quotation marks, bullet points, or section numbers. "
            "The address must be captured exactly as it appears, including all words, punctuation, and formatting. "
            "Example: 'UNIT NO 28-06 TYPE B BLOCK 1, RESIDENSI TANGEN, SEGAMBUT WP KUALA LUMPUR, WP KUALA LUMPUR, MALAYSIA'."
        )
    )


class TitleInformation(BaseModel):
    """Contains information for land title."""
    title_description: Optional[str] = Field(
        None,
        description=("Extract the land title starting from 'PN' (or similar title prefix) after the phrase 'held under', and stop at the first full stop.")
    )


class GuarantorInformation(BaseModel):
    """Contains information about the guarantor."""
    guarantor_name: Optional[str] = Field(None, description="The full name of all guarantors (individuals or companies or corporate) mentioned in the document. Look for names that follow phrases like 'executed by', 'guarantee by', or appear in guarantee clauses." 
                                          "Include all guarantors when multiple are listed with conjunctions like 'and' or separated by commas. Extract complete names without titles or identification numbers."
                                          "If it is confusing, identify first all mentioned individuals and companies that are surrounded by the guarantee word, then discard any guarantees names that has incomplete information as it should be a pair of name with its identification.")
    guarantor_registration_number: Optional[str] = Field(None, description="The identification numbers (NRIC, passport, company registration) of guarantors, typically appearing in parentheses or with prefixes like 'NRIC No.', 'New IC No.', 'Company No.' near guarantor names. Separate multiple numbers by commas.")
    guarantor_address: Optional[str] = Field(None, description="The full business or individual guarantors' address")
    guarantor_postcode: Optional[str] = Field(None, description="The 5 digit postcode of business address for example 68100. 68100 is example not the actual postcode in my description")


class LawFirmInformation(BaseModel):
    """Contains information about the law firm."""
    law_firm_name: Optional[str] = Field(None, description="The full name of Abraham Ooi not including its address")
    law_firm_address: Optional[str] = Field(None, description="The address of the Abraham Ooi & Partners law firm.")
    law_firm_city: Optional[str] = Field(None, description="The malaysia's city from Abraham Ooi & Partners' full address ")
    law_firm_postcode: Optional[str] = Field(None, description="The 5 digit postcode of Abraham Ooi & Partners' address for example 68100")