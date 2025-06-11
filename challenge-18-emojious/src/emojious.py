def main():
    cp = '🙧😏🙮🙸🙌🙄😮🙀🙕🙞🙒😜🙎🙍🙒🙾😱🙊🙞🙛🙍😺🙰🙌🙇🙄😠🙆🙞🙛🙾😷🙇🙚🙄🙄😜🙋🙞🙎🙒😾'
    print(f"This is interesting: {cp}")
    mkey = input("Type the magic key: ")
    pt = ''.join([chr(ord(c) ^ ord(mkey[i % len(mkey)])) for i, c in enumerate(cp)])
    print(f"And this is what you've got: {pt}")

    # Hint: The key is the flag and the flag format is FLAG{....}

main()
