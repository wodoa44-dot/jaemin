import math

N = 168019
E = 65537


def main():
    n, e = N, E
    print(f"공개키: n = {n}, e = {e}")

    print("\n[1] n의 소인수 탐색")
    for p in range(2, math.isqrt(n) + 1):
        remainder = n % p
        print(f"{n} % {p} = {remainder}")

        if remainder == 0:
            q = n // p
            print(f"발견: p = {p}, q = {q}")
            break
    else:
        print("소인수를 찾지 못했습니다.")
        return

    print("\n[2] phi(n) 계산")
    phi = (p - 1) * (q - 1)
    print(f"phi(n) = ({p} - 1) × ({q} - 1) = {phi}")

    print("\n[3] 확장 유클리드 알고리즘")
    r0, r1 = phi, e
    t0, t1 = 0, 1

    while r1:
        quotient, remainder = divmod(r0, r1)
        print(f"{r0} = {quotient} × {r1} + {remainder}")
        r0, r1 = r1, remainder
        t0, t1 = t1, t0 - quotient * t1

    if r0 != 1:
        print("역원이 존재하지 않습니다.")
        return

    d = t0 % phi

    print("\n[4] 개인키 복원 결과")
    print(f"d = {d}")
    print(f"검증: ({e} × {d}) % {phi} = {(e * d) % phi}")
    print(f"RSA 개인키 (d, n) = ({d}, {n})")


if __name__ == "__main__":
    main()
