from typing import Any


def convert_to_int(number: float) -> tuple[int, Any]:
    # считает числа если они не меньше 0.00001

    rate = 10 ** len(str(number).split(".")[-1])
    return rate, round(number * rate)



