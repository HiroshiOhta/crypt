#!/usr/bin/env python

"""
AESの暗号処理で使用するキーを生成する。

Parameters
----------
None

Returns
-------
int
    0 : 正常終了
    1 : ランダムなバイト生成に失敗した時
    2 : キーファイル格納ディレクトリおよびファイルのパーミッションが正しくない時

See Also
--------
ユーザホームディレクトリに生成したキーを保存したファイルが作成されます。
ファイル名 : ~/.secret/keyfile
"""

# 標準ライブラリ
from os import chmod, mkdir
from pathlib import Path
from sys import exit

# サードパーティライブラリ
from Crypto.Random import get_random_bytes

# ローカルなライブラリ
from constants import KEY_STORE

# 変数定義
# ------------------------------------------------------------------------------
# keyfile のディレクトリ設定
KEY_STORE_PATH = str(Path(KEY_STORE).parent)

# ディレクトリ作成
# ------------------------------------------------------------------------------
if not Path(KEY_STORE_PATH).exists():
    mkdir(KEY_STORE_PATH, 0o0700)

# 暗号キーの生成
# ------------------------------------------------------------------------------
key = ""
key = get_random_bytes(32)

# 暗号キーの keyfile への書込
# ------------------------------------------------------------------------------
try:
    # 暗号キーの keyfile への書込
    with open(KEY_STORE, "wb") as key_out:
        key_out.write(key)

# get_random_bytes が NG のとき key のタイプが str の例外
except TypeError as err:
    print(err)
    exit(1)

# key_file のパーミッションが正しくない場合の例外
except PermissionError as err:
    print(err)
    exit(2)
else:
    # パーミッション変更
    chmod(KEY_STORE, 0o0600)

exit(0)
