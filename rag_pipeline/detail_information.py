from typing import Optional, Type
from pydantic import BaseModel, Field

class BorrowerInformation(BaseModel):
    """Contains information about the borrower."""
    borrower_name: Optional[str] = Field(None, description="The full name of the SHINJING AUTO PARTS SDN. BHD.")
    borrower_registeration_number: Optional[str] = Field(None, description="The full Registration No. of the SHINJING AUTO PARTS SDN. BHD.")
    borrower_address: Optional[str] = Field(None, description="The full bussiness address of the SHINJING AUTO PARTS SDN. BHD.")
    borrower_postcode: Optional[str] = Field(None, description="The 5 digit postcode of bussiness address for example 68100")

class BankInformation(BaseModel):
    """Contains information about the bank."""
    bank_name: Optional[str] = Field(None, description="The official name of a bank operating in Malaysia. Must be one of the following: ""'CIMB', 'UOB', 'Maybank', 'ALLIANCE', 'Public Bank', or 'Standard Chartered'. ""If the extracted name is different or informal, map it to the closest valid Malaysian bank name.")
    bank_address: Optional[str] = Field(None, description="The address of the bank. Hint: look for branch keywords to identify the full address")
    bank_registeration_number: Optional[str] = Field(None, description="The registeration number of the bank.")

class LoanInformation(BaseModel):
    """Contains information about the loan."""
    loan_amount: Optional[str] = Field(None, description="The mentioned total approved limit in RM, hint: the largest number found")
    letter_offer_date: Optional[str] = Field(None, description="Look for the date closest to the subject of 'Letter of Offer' or a phrase like 'Our Reference' or 'Our Ref' or 'Date:'."
                                                                "Stricly only one complete date allowed")
    subject_matter: Optional[str] = Field(
        None,
        description=(
            "Extract the full detailed descriptions of all approved banking facilities or forms of facilities."
            "Look for sections or tables labeled 'Banking Facilities', 'Form of Facilities', or similar."
            "For each facility (e.g., Term Loan, Overdraft, Bank Guarantee), capture the complete detail including interest rates, limits, and repayment or usage conditions. "
            "The output should contain the full description for each facility exactly as provided in the source, and if multiple facilities are present, they should be concatenated into one string, with each full description separated by commas."
            "Omit any weird symbols or any seperators except the commas and full stop"
            "For example, if detailed information is present, do not reduce it to just the facility names."
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
    guarantor_name: Optional[str] = Field(None, description="The full name of the several guarantees seperated by commas")
    guarantor_registeration_number: Optional[str] = Field(None, description="The full Malaysian Registration No. or NRIC or passport number or old IC number of the guarantees or joint guarantees, if more than one seperate them by commas")
    guarantor_address: Optional[str] = Field(None, description="The full bussiness or individuals guarantees' address")
    guarantor_postcode: Optional[str] = Field(None, description="The 5 digit postcode of bussiness address for example 68100")

class LawFirmInformation(BaseModel):
    """Contains information about the law firm."""
    law_firm_name: Optional[str] = Field(None, description="The full name of Abraham Ooi not including its address")
    law_firm_address: Optional[str] = Field(None, description="The address of the Abraham Ooi & Partners law firm.")
    law_firm_city: Optional[str] = Field(None, description="The malaysia's city from Abraham Ooi & Partners' full address ")
    law_firm_postcode: Optional[str] = Field(None, description="The 5 digit postcode of Abraham Ooi & Partners' address for example 68100")