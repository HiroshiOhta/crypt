#!/usr/bin/env python

# 標準ライブラリ
from os import chmod, makedirs
from pathlib import Path
from sys import exit

# サードパーティライブラリ
from Crypto.Random import get_random_bytes

# ローカルなライブラリ
from constants import KEY_STORE


def gen_crypt_key(key_store_file: str = KEY_STORE) -> int:
    """
    AESの暗号処理で使用するキーを生成する。

    Parameters
    ----------
    str
        AES暗号処理で使用するキーを保存するファイルパス

    Returns
    -------
    int
        0 : 正常終了
        1 : 引数に指定されたパスがディレクトリとして存在する場合
        2 : ランダムなバイト生成に失敗した時
        3 : キーファイル格納ディレクトリおよびファイルのパーミッションが正しくない時

    See Also
    --------
        ユーザホームディレクトリに生成したキーを保存したファイルが作成されます。
        ファイル名 : ~/.secret/keyfile
    """

    # 変数定義
    # --------------------------------------------------------------------------
    # keyfile のディレクトリ設定
    KEY_STORE_DIR = str(Path(key_store_file).parent)

    # 指定パス確認
    # --------------------------------------------------------------------------
    if Path(key_store_file).is_dir():
        # TODO: logging で出力するように変更する。要学習。
        print("キーを保存するファイルのパスを指定して下さい。")
        return 1

    # ディレクトリ作成
    # --------------------------------------------------------------------------
    if not Path(KEY_STORE_DIR).exists():
        makedirs(KEY_STORE_DIR, mode=0o0700)

    # 暗号キーの生成
    # --------------------------------------------------------------------------
    key = ""
    key = get_random_bytes(32)

    # 暗号キーの keyfile への書込
    # --------------------------------------------------------------------------
    try:
        # 暗号キーの keyfile への書込
        with open(key_store_file, "wb") as key_out:
            key_out.write(key)

    # get_random_bytes が NG のとき key のタイプが str の例外
    except TypeError as err:
        # TODO: logging で出力するように変更する。要学習。
        print(err)
        return 2

    # key_file のパーミッションが正しくない場合の例外
    except PermissionError as err:
        # TODO: logging で出力するように変更する。要学習。
        print(err)
        return 3

    else:
        # パーミッション変更
        chmod(key_store_file, 0o0600)

    return 0


if __name__ == "__main__":

    return_code = gen_crypt_key()
    exit(return_code)
