from typing import Any


def convert_to_int(number: float) -> tuple[int, Any]:

    rate = 10 ** len(str(number).split(".")[-1])
    return rate, round(number * rate)



