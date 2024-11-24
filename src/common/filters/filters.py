from dataclasses import dataclass


@dataclass(eq=False)
class PaginationFilters:
    limit: int = 10
    offset: int = 0
