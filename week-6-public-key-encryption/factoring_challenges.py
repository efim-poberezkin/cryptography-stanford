import gmpy2
from gmpy2 import mpz


def main():
    p = factoring_challenge_1()
    print(f"---\nfactoring challenge #1:\n{p}")

    p = factoring_challenge_2()
    print(f"---\nfactoring challenge #2:\n{p}")

    # ! fix math
    p = factoring_challenge_3()
    print(f"---\nfactoring challenge #3:\n{p}")


def factoring_challenge_1():
    """
    By following assumption that |p - q| < 2N^(1/4), it can be shown that A - sqrt(N) < 1,
    where A = (p + q)/2. A is an integer, hence A = ceil(sqrt(N)). x is an integer
    such that p = A - x and q = A + x. It can be shown that x = sqrt(A^2 - N).
    Now, given x and A we can factor N by computing p and q.
    """
    modulus = mpz(
        "17976931348623159077293051907890247336179769789423065727343008115"
        "77326758055056206869853794492129829595855013875371640157101398586"
        "47833778606925583497541085196591615128057575940752635007475935288"
        "71082364994994077189561705436114947486504671101510156394068052754"
        "0071584560878577663743040086340742855278549092581"
    )
    a, rem = gmpy2.isqrt_rem(modulus)
    if rem > 0:
        a += 1
    x = gmpy2.isqrt(a ** 2 - modulus)
    p, q = a - x, a + x
    assert gmpy2.mul(p, q) == modulus
    return p


def factoring_challenge_2():
    """
    |p - q| < 2^11 * N^(1/4)
    in this case: A - sqrt(N) < 2^20
    """
    modulus = mpz(
        "6484558428080716696628242653467722787263437207069762630604390703787"
        "9730861808111646271401527606141756919558732184025452065542490671989"
        "2428844841839353281972988531310511738648965962582821502504990264452"
        "1008852816733037111422964210278402893076574586452336833570778346897"
        "15838646088239640236866252211790085787877"
    )
    a = gmpy2.isqrt(modulus) + 1

    while True:
        x, rem = gmpy2.isqrt_rem(a ** 2 - modulus)
        if rem == 0:
            p, q = a - x, a + x
            if gmpy2.mul(p, q) == modulus:
                return p
        a += 1


# ! fix math
def factoring_challenge_3():
    """
    Given |3p - 2q| < N^(1/4) and considering A = (3p + 2q) / 2 we can show that
    A - sqrt(6N) < 1 => A = ceil(sqrt(6N)).
    Let x be equal distance from A to 3p and 2q, then x = sqrt(A^2 - 6N)
    => we can calculate p and q based on this.
    """
    modulus = mpz(
        "72006226374735042527956443552558373833808445147399984182665305798191"
        "63556901883377904234086641876639384851752649940178970835240791356868"
        "77441155132015188279331812309091996246361896836573643119174094961348"
        "52463970788523879939683923036467667022162701835329944324119217381272"
        "9276147530748597302192751375739387929"
    )
    a, rem = gmpy2.isqrt_rem(6 * modulus)
    if rem > 0:
        a += 1
    x = gmpy2.isqrt(a ** 2 - 6 * modulus)
    a_minus_x, a_plus_x = a - x, a + x

    # either p = (A - x) / 3 and q = (A + x) / 2
    p, rem = gmpy2.f_divmod(a_minus_x, 3)
    if rem == 0:
        q, rem = gmpy2.f_divmod(a_plus_x, 2)
        if gmpy2.mul(p, q) == modulus:
            return p if p < q else q

    # or p = (A + x) / 3 and q = (A - x) / 2
    p, rem = gmpy2.f_divmod(a_plus_x, 3)
    if rem == 0:
        q = gmpy2.f_div(a_minus_x, 2)
        if gmpy2.mul(p, q) == modulus:
            return p if p < q else q


if __name__ == "__main__":
    main()
