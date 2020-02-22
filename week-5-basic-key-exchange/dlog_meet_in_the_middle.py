from gmpy2 import add, f_mod, invert, mpz, mul, powmod


_p = (
    "134078079299425970995740249982058461274793658205923933"
    "77723561443721764030073546976801874298166903427690031"
    "858186486050853753882811946569946433649006084171"
)

_g = (
    "11717829880366207009516117596335367088558084999998952205"
    "59997945906392949973658374667057217647146031292859482967"
    "5428279466566527115212748467589894601965568"
)

_h = (
    "323947510405045044356526437872806578864909752095244"
    "952783479245297198197614329255807385693795855318053"
    "2878928001494706097394108577585732452307673444020333"
)


"""
We are given h mod p such that h = g^x, where 1 <= x <= 2^40.
Let b = 2^20. Since x < b^2, x = x0*b + x1 where x0 and x1 are in the range [0, B-1].
Then h = g^(x0*b + x1) = (g^b)^x0 * g^x1 mod p.
=> h/g^x1 = (g^b)^x0 mod p.

We can find solution using meet in the middle:
- Build a hash table of left hand side values h/g^x1 for x1 = 0, 1, ..., 2^20.
- For each x0 = 0, 1, ..., 2^20 check if (g^b)^x0 is in this hash table.
  If so, then solution is (x0, x1) and x = x0*b + x1.
"""


def main():
    p = mpz(_p)
    g = mpz(_g)
    h = mpz(_h)

    x = dlog(p, g, h)

    print(x)


# non optimized implementation
def dlog(p, g, h):
    b = 2 ** 20
    table = build_table(p, g, h, b)
    x0, x1 = lookup_table(p, g, b, table)
    x = add(mul(x0, b), x1)
    return x


def build_table(p, g, h, b):
    table = dict()
    for x1 in range(b):
        left_side_value = f_mod(mul(h, invert(powmod(g, x1, p), p)), p)
        table[left_side_value] = x1
    return table


def lookup_table(p, g, b, table):
    for x0 in range(b):
        right_side_value = powmod(powmod(g, b, p), x0, p)
        if right_side_value in table:
            x1 = table[right_side_value]
            return x0, x1


if __name__ == "__main__":
    main()
