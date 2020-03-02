from gmpy2 import mpz
import gmpy2

gmpy2.get_context().precision = 1500


def main():
    factoring_challenge_1()


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
    a = gmpy2.ceil(gmpy2.sqrt(modulus))
    x = gmpy2.sqrt(a ** 2 - modulus)
    p, q = a - x, a + x
    assert gmpy2.mul(p, q) == modulus
    print(p)


if __name__ == "__main__":
    main()
