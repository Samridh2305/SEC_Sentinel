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
    r"\bItem\s+\d+\.\d+",
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
    "item 1.": "Financial Statements",
    "item 2.": "Management Discussion and Analysis",
    "item 3.": "Market Risk",
    "item 4.": "Controls and Procedures",
    "item 1a.": "Risk Factors",
    "item 5.": "Other Information",
    "item 6.": "Exhibits",
}

EIGHT_K_SECTIONS = {
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

        "toc_marker": "Business"

    },

    "10-Q": {

        "pattern": TEN_Q_PATTERN,

        "sections": TEN_Q_SECTIONS,

        "toc_marker": "PART I"

    },

    "8-K": {

        "pattern": EIGHT_K_PATTERN,

        "sections": EIGHT_K_SECTIONS,

        "toc_marker": None

    }

}