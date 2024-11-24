

def convert_to_int(number: float) -> dict[str, int]:

    rate = 10 ** len(str(number).split(".")[-1])
    return {"rate": rate, "number_after_convert": int(number * rate)}
