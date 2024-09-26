import os


def setup():
    # ディレクトリが存在しない場合は作成
    if not os.path.exists('db'):
        os.makedirs('db')
