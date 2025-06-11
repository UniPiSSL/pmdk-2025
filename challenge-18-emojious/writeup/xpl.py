cp = '🙧😏🙮🙸🙌🙄😮🙀🙕🙞🙒😜🙎🙍🙒🙾😱🙊🙞🙛🙍😺🙰🙌🙇🙄😠🙆🙞🙛🙾😷🙇🙚🙄🙄😜🙋🙞🙎🙒😾'
flag = "FLAG{"

key = ''.join([chr(ord(cp[j]) ^ ord(flag[j % len(flag)])) for j in range(len(flag))])
plaintext = ''.join([chr(ord(c) ^ ord(key[j % len(flag)])) for j, c in enumerate(cp)])

print("Key: ", key)
print("Flag: ", plaintext)
