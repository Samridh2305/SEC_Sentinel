import re

TEN_K_PATTERN = re.compile(
    r"\bItem\s+\d+[A-Z]?\.",
    re.IGNORECASE
)

TEN_Q_PATTERN = re.compile(
    r"\bItem\s+\d+[A-Z]?\.",
    re.IGNORECASE
)

EIGHT_K_PATTERN = re.compile(
    r"\bItem\s+(?:\d+\.\d+|\d+\.)",
    re.IGNORECASE
)
PART_PATTERN = re.compile(
    r"\bPART\s+(I|II)\b",
    re.IGNORECASE
)

TEN_K_SECTIONS = {
    "item 1.": "Business",
    "item 1a.": "Risk Factors",
    "item 1b.": "Unresolved Staff Comments",
    "item 1c.": "Cybersecurity",
    "item 2.": "Properties",
    "item 3.": "Legal Proceedings",
    "item 4.": "Mine Safety Disclosures",
    "item 5.": "Market for Registrant's Common Equity",
    "item 6.": "Selected Financial Data",
    "item 7.": "Management Discussion and Analysis",
    "item 7a.": "Market Risk",
    "item 8.": "Financial Statements",
    "item 9.": "Changes in Accountants",
    "item 9a.": "Controls and Procedures",
    "item 9b.": "Other Information",
    "item 9c.": "Foreign Jurisdictions",
    "item 10.": "Directors and Executive Officers",
    "item 11.": "Executive Compensation",
    "item 12.": "Security Ownership",
    "item 13.": "Related Party Transactions",
    "item 14.": "Principal Accounting Fees",
    "item 15.": "Exhibits",
    "item 16.": "Form 10-K Summary",
}

TEN_Q_SECTIONS = {
    "part i item 1.": "Financial Statements",
    "part i item 2.": "Management Discussion and Analysis",
    "part i item 3.": "Market Risk",
    "part i item 4.": "Controls and Procedures",

    "part ii item 1.": "Legal Proceedings",
    "part ii item 1a.": "Risk Factors",
    "part ii item 2.": "Unregistered Sales of Equity Securities and Use of Proceeds",
    "part ii item 3.": "Defaults Upon Senior Securities",
    "part ii item 4.": "Mine Safety Disclosures",
    "part ii item 5.": "Other Information",
    "part ii item 6.": "Exhibits",
}

EIGHT_K_SECTIONS = {
    # Older 8-K filings used whole-number item headings.
    "item 2.": "Acquisition or Disposition of Assets",
    "item 7.": "Financial Statements and Exhibits",
    "item 1.01": "Entry into a Material Definitive Agreement",
    "item 1.02": "Termination of a Material Definitive Agreement",
    "item 2.01": "Completion of Acquisition or Disposition",
    "item 2.02": "Results of Operations and Financial Condition",
    "item 5.02": "Departure of Directors or Officers",
    "item 7.01": "Regulation FD Disclosure",
    "item 8.01": "Other Events",
    "item 9.01": "Financial Statements and Exhibits",
}

FORM_CONFIG = {
    "10-K": {
        "pattern": TEN_K_PATTERN,
        "sections": TEN_K_SECTIONS,
    },
    "10-Q": {
        "pattern": TEN_Q_PATTERN,
        "sections": TEN_Q_SECTIONS,
    },
    "8-K": {
        "pattern": EIGHT_K_PATTERN,
        "sections": EIGHT_K_SECTIONS,
    }
}
