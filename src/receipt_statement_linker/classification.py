from enum import StrEnum


DEFAULT_CLASSIFICATIONS = [
    "GROCERIES",
    "EATING_OUT",
    "TRANSPORTATION",
    "HOUSING",
    "HEALTHCARE",
    "PERSONAL_CARE",
    "ENTERTAINMENT",
    "SAVINGS_AND_INVESTMENTS",
    "DEBT_PAYMENT",
    "MISC",
]


def set_classifications_enum(
    classifications_list: list[str] | None = None,
) -> type[StrEnum]:
    return StrEnum("Classifications", classifications_list or DEFAULT_CLASSIFICATIONS)
