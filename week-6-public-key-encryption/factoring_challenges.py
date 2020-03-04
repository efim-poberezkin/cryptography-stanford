import gmpy2
from gmpy2 import mpz


def main():
    p = factoring_challenge_1()
    print(f"---\nfactoring challenge #1:\n{p}")

    p = factoring_challenge_2()
    print(f"---\nfactoring challenge #2:\n{p}")


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


if __name__ == "__main__":
    main()
