import enum


@enum.unique
class Tags(enum.Enum):
    FIRMS = "firms"
    INVOICES = "invoices"
    CASH_BOX = "cash_box"
    EXPENSES = "expenses"
    REPORTS = "reports"
    DEBTORS = "debtors"
    SHOPPING = "shopping"

