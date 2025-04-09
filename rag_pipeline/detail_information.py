from typing import Optional, Type
from pydantic import BaseModel, Field

class BorrowerInformation(BaseModel):
    """Contains information about the borrower."""
    borrower_name: Optional[str] = Field(None, description="The full name of the AH CHENG LAKSA TRADING SDN. BHD.")
    borrower_registeration_number: Optional[str] = Field(None, description="The full Registration No. of the AH CHENG LAKSA TRADING SDN. BHD.")
    borrower_address: Optional[str] = Field(None, description="The full bussiness address of the AH CHENG LAKSA TRADING SDN. BHD.")
    borrower_postcode: Optional[str] = Field(None, description="The 5 digit postcode of bussiness address for example 68100")

class BankInformation(BaseModel):
    """Contains information about the bank."""
    bank_name: Optional[str] = Field(None, description="The official name of a bank operating in Malaysia. Must be one of the following: ""'CIMB', 'UOB', 'Maybank', 'ALLIANCE', 'Public Bank', or 'Standard Chartered'. ""If the extracted name is different or informal, map it to the closest valid Malaysian bank name.")
    bank_address: Optional[str] = Field(None, description="The address of the bank.")
    bank_registeration_number: Optional[str] = Field(None, description="The registeration number of the bank.")

class LoanInformation(BaseModel):
    """Contains information about the loan."""
    loan_amount: Optional[str] = Field(None, description="The mentioned approved limit in RM")
    letter_offer: Optional[str] = Field(None, description="The full letter offer date in format DD/MM/YYYY or DD-MM-YYYY")

class GuarantorInformation(BaseModel):
    """Contains information about the guarantor."""
    guarantor_name: Optional[str] = Field(None, description="The full name of the several guarantees seperated by commas")
    guarantor_registeration_number: Optional[str] = Field(None, description="The full Malaysian Registration No. or NRIC or passport number or old IC number of the joint guarantees, if more than one seperate them by commas")
    guarantor_address: Optional[str] = Field(None, description="The full bussiness or individuals guarantees' address")
    guarantor_postcode: Optional[str] = Field(None, description="The 5 digit postcode of bussiness address for example 68100")

class LawFirmInformation(BaseModel):
    """Contains information about the law firm."""
    law_firm_name: Optional[str] = Field(None, description="The full name of Abraham Ooi not including its address")
    law_firm_address: Optional[str] = Field(None, description="The address of the Abraham Ooi & Partners law firm.")
    law_firm_city: Optional[str] = Field(None, description="The malaysia's city from Abraham Ooi & Partners' full address ")
    law_firm_postcode: Optional[str] = Field(None, description="The 5 digit postcode of Abraham Ooi & Partners' address for example 68100")