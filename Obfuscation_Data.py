# data_cloak_v2.py
import random
import string
from typing import Sequence, Tuple, List

def cloak_numbers(numbers: Sequence[str], seed: int = 5678) -> Tuple[List[str], List[str]]:
    """
    Insert random letters after digits to hide the original numbers.
    Returns a pair: (cloaked_strings, masks) where mask has '1' for original chars and '0' for filler.
    """
    rng = random.Random(seed)
    cloaked_list: List[str] = []
    mask_list: List[str] = []

    for number in numbers:
        temp = []
        mask = []
        for ch in number:
            temp.append(ch)
            mask.append("1")
            for _ in range(rng.randint(0, 3)):
                temp.append(rng.choice(string.ascii_letters))
                mask.append("0")
        cloaked_list.append("".join(temp))
        mask_list.append("".join(mask))

    return cloaked_list, mask_list


def decloak(cloaked: Sequence[str], masks: Sequence[str]) -> List[str]:
    """
    Recover original numbers using the masks.
    """
    recovered_list: List[str] = []
    for text, mask in zip(cloaked, masks):
        recovered_list.append("".join(ch for ch, flag in zip(text, mask) if flag == "1"))
    return recovered_list


if __name__ == "__main__":
    # New sample numbers
    phone_samples = ["0779988776", "0123456789", "0543210987"]
    hidden_numbers, masks = cloak_numbers(phone_samples, seed=99)
    print("Cloaked Numbers:", hidden_numbers)
    print("Recovered Numbers:", decloak(hidden_numbers, masks))
