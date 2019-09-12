#!/usr/bin/env python

# 標準ライブラリ
# from os import chmod, mkdir
from pathlib import Path
from base64 import b64encode, b64decode
from sys import exit, argv

# サードパーティライブラリ
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util import Counter

# ローカルなライブラリ
from constants import KEY_STORE
from generate_crypt_keyfile import gen_crypt_key


def get_crypt_key(crypt_key_file: str = KEY_STORE) -> str:
    """
    暗号処理で使用するキーを指定されたキーファイルから取得する。

    Parameters
    ----------
    crypt_key_file : str, optional
        暗号処理で使用するキーが保存されたファイルパス (default KEY_STORE)

    Returns
    -------
    str
        暗号処理で使用するキー
    """

    # 暗号キーの key への設定
    # ------------------------------------------------------------------------------
    try:
        # 暗号キーの keyfile への書込
        with open(KEY_STORE, "rb") as key_file:
            crypt_key = key_file.read()

    except FileNotFoundError as err:
        # TODO: logging で出力するように変更する。要学習。
        print(err)

    except PermissionError as err:
        # TODO: logging で出力するように変更する。要学習。
        print(err)

    else:
        return crypt_key


def encrypt_strigs(crypt_string: str, crypt_key_file: str = KEY_STORE) -> str:
    """
    指定された文字列をAESのCounTeR modeを用いて暗号化を行う。
    暗号化したデータをbase64エンコードした文字列を返す。

    Parameters
    ----------
    crypt_string : str
        暗号化を行う文字列
    crypt_key_file : str, optional
        暗号処理で使用するキーが保存されたファイルパス (default KEY_STORE)

    Returns
    -------
    str
        暗号化しbase64エンコードされた文字列
    """

    if not Path(crypt_key_file).is_file():
        return_code = gen_crypt_key(crypt_key_file)

        if return_code > 0:
            exit(return_code)

    # 暗号キーの取得
    # ------------------------------------------------------------------------------
    key = get_crypt_key(crypt_key_file)

    # CTR方式による暗号化
    # ------------------------------------------------------------------------------
    # 初期化ベクトルとカウンタの作成
    iv = get_random_bytes(AES.block_size)
    ctr = Counter.new(AES.block_size * 8,
                      initial_value=int.from_bytes(iv, byteorder='big'))
    # CTRモードのAES暗号の作成
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    # 暗号化
    cipher_text = cipher.encrypt(crypt_string.encode())
    # 初期化ベクトルと暗号化されたデータをBase64エンコードする
    encrypt_strig = b64encode(iv + cipher_text).decode('utf-8')

    return encrypt_strig


def decrypt_strings(encrypted_string: str,
                    crypt_key_file: str = KEY_STORE) -> str:
    """
    暗号化しbase64エンコードされた文字列のデコードを行う。
    デコードされたデータの復号化を行う。

    Parameters
    ----------
    encrypted_string : str
        暗号化しbase64エンコードされた文字列
    crypt_key_file : str, optional
        暗号処理で使用するキーが保存されたファイルパス (default KEY_STORE)

    Returns
    -------
    str
        復号化された文字列
    """

    # 暗号キーの取得
    # ------------------------------------------------------------------------------
    key = get_crypt_key(crypt_key_file)

    # CTR方式による複合化
    # ------------------------------------------------------------------------------
    # 指定された文字列をBase64デコードする
    cipher_text = b64decode(encrypted_string)
    # デコードされたデータから初期ベクトルと暗号化データを取得
    iv = cipher_text[:16]
    encrypted_data = cipher_text[16:]
    # カウンタの作成
    ctr = Counter.new(AES.block_size * 8,
                      initial_value=int.from_bytes(iv, byteorder='big'))
    # CTRモードのAES暗号の作成
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    # 復号化
    decrypt_string = cipher.decrypt(encrypted_data).decode()

    return decrypt_string


if __name__ == "__main__":

    # 入力された文字列の暗号化を行う
    encrypt_strig = encrypt_strigs(argv[1])
    print(encrypt_strig)
