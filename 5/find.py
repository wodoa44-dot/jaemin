import ast
import math


def recover_rsa(n, e):
    for p in range(2, math.isqrt(n) + 1):
        if n % p == 0:
            q = n // p
            phi = p * (p - 1) if p == q else (p - 1) * (q - 1)
            d = pow(e, -1, phi)
            return p, q, d
    raise ValueError("n을 소인수분해하지 못했습니다.")


def main():
    n = int(input("공개키 n: "))
    e = int(input("공개키 e: "))

    if not 400**2 <= n <= 500**2:
        raise ValueError("과제의 소수 범위(400~500)에 해당하는 n을 입력하세요.")
    if not 1 < e < n:
        raise ValueError("e는 1보다 크고 n보다 작아야 합니다.")

    p, q, d = recover_rsa(n, e)

    print(f"\np = {p}")
    print(f"q = {q}")
    print(f"RSA 개인 지수 d = {d}")
    print(f"RSA 개인키 (d, n) = ({d}, {n})")

    raw = input("\nencrypted_key 리스트 (없으면 Enter): ").strip()
    if not raw:
        return

    encrypted_key = ast.literal_eval(raw)
    if (
        not isinstance(encrypted_key, list)
        or len(encrypted_key) != 32
        or any(type(c) is not int or not 0 <= c < n for c in encrypted_key)
    ):
        raise ValueError("encrypted_key는 32개 정수의 리스트여야 합니다.")

    values = [pow(c, d, n) for c in encrypted_key]
    if any(value > 255 for value in values):
        raise ValueError("키 복원 실패: n, e, encrypted_key가 같은 통신의 값인지 확인하세요.")

    aes_key = bytes(values)
    print(f"\nAES-256 키 (16진수): {aes_key.hex()}")
    print(f"AES 키 길이: {len(aes_key)}바이트")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, SyntaxError) as error:
        print(f"오류: {error}")