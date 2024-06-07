import marimo

__generated_with = "0.5.2"
app = marimo.App()


@app.cell
def __(mo):
    mo.md('# marimoを使ってみよう！')
    return


@app.cell
def __(mo):
    mo.md("""## リアクティブなプログラム実行環境
    marimoではセルで定義された変数を変化させると、別のセルで参照されたその変数も即時で自動的に更新するため、セルの実行を行わないと参照先の変数の値を更新しないJupyterと比べて、実行し忘れによるデータの不整合を減らすことができます。
    """)
    return


@app.cell
def __(x):
    y = x + 1
    y
    return y,


@app.cell
def __(y):
    z = y * 2
    z
    return z,


@app.cell
def __(mo):
    x = 17
    mo.md(f'ここで x={x} を変更して実行すると、y, zも変更されます。')
    return x,


@app.cell
def __():
    #x=10 # 再代入しようとするとエラー
    return


@app.cell
def __(mo):
    button = mo.ui.button(
        value=0, 
        on_click=lambda value: value + 1) # インクリメントボタン
    text_area = mo.ui.text_area() # テキストエリア
    switch = mo.ui.switch() # スイッチ
    return button, switch, text_area


@app.cell
def __(button, mo, switch, text_area):
    mo.md(f"""marimoでは自由にボタンやテキストエリアを配置できます。色々遊んでみましょう！

    ボタンはここ: {button}

    テキストエリアに何かを書こう: {text_area}

    スイッチ切り替え: {switch}

    詳しくは[こちらの公式ドキュメント](https://docs.marimo.io/api/inputs/index.html)
    """)
    return


@app.cell
def __(button, mo, switch, text_area):
    mo.md(f"""得られた内容は.valueで参照可能で、UI Elementsを操作するとここの値もリアルタイムに変更されます！

    ボタンの結果: {button.value}

    テキストエリアに書いたもの: {text_area.value}

    スイッチの結果: {switch.value}

    """)
    return


@app.cell
def __():
    import marimo as mo
    return mo,


if __name__ == "__main__":
    app.run()
