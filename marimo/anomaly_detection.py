import marimo

__generated_with = "0.5.2"
app = marimo.App(width="full")


@app.cell
def __(mo):
    mo.md("""
    # 次世代のJupyter notebook「marimo」で作るインタラクティブなデータ分析報告書~Pridictive Maintainance Dataset~
    * このアプリケーションではデータをアップロードすると前処理・手法を選択しながら異常検知を行うことができます。
    """)
    return


@app.cell
def __(mo):
    f = mo.ui.file_browser(multiple=False)
    mo.vstack([
        mo.md("""
            * 異常検知を行うcsvファイルをアップロードしてください。ただし以下の制限があります。
                * 100MBの容量制限があります。
                * .csvファイルに限ります。
                * 異常値のフラグが含まれている必要があります。"""),
               f])
    return f,


@app.cell
def __(e, f, mo, pd):
    _stack_mo_list = []
    READ_DATA = False
    if f.path() != None:
        if f.name().split('.')[-1] not in ['csv', 'CSV']:
            _stack_mo_list.append(mo.md('ファイルの拡張子がcsvまたはCSVではありません。').callout('alert'))
        else:
            try:
                df = pd.read_csv(f.path(), index_col=0)
                _stack_mo_list = [mo.md('正常にデータを読み込みました').callout('info'),
                                  mo.as_html(df.head())]
                READ_DATA = True
            except Exception() as e:
                _stack_mo_list.append(mo.md(f'ファイル読み込みエラー: {e}').callout('alert'))
    mo.vstack(_stack_mo_list)
    return READ_DATA, df


@app.cell
def __(mo):
    code = mo.ui.code_editor(label="Code Editor: データに対して必要な処理があればmain関数内に記入してください。", 
                             language="python",
                             value=
    """# 関数名は変えない
    def main(df):
      # ====== ここを編集する =====
      # 例: machine maintainance データだと[hoge]を削除する
      df.columns = [c.split('[')[0].strip() for c in df.columns]
      return df"""
    )
    mo.as_html(code)
    return code,


@app.cell
def __(READ_DATA, code, df, main):
    if READ_DATA:
        print(code.value)
        exec(code.value)
        code_prep_df = main(df)
    return code_prep_df,


@app.cell
def __(READ_DATA, code_prep_df, mo):
    _stack_mo_list = []
    if READ_DATA:
        transformed_df = mo.ui.dataframe(code_prep_df)
        _stack_mo_list.append(
            mo.md('## marimoの機能を用いた前処理').center())
        _stack_mo_list.append(
            mo.accordion(
                {'詳細を開く': mo.md("""
                * ここではmarimoのEDA機能である`mo.ui.dataframe`での前処理を実施できます。
                    * カラムの選択、フィルタリングが実施できます。
                    * 詳しくは公式サイトをご覧ください。
                """).callout('info')
                }
            ))
        _stack_mo_list.append(transformed_df)
    mo.vstack(_stack_mo_list)
    return transformed_df,


@app.cell
def __(READ_DATA, transformed_df):
    if READ_DATA:
        tdf = transformed_df.value.copy()
    return tdf,


@app.cell
def __(READ_DATA, mo, tdf):
    _stack_mo_list = []
    if READ_DATA:
        stats = tdf.describe()
        _stack_mo_list.append(mo.md(
            f"""
            {mo.vstack([mo.md('## データの統計量を可視化')], 'center')}
            {mo.as_html(stats)}"""
        ))
    mo.vstack(_stack_mo_list)
    return stats,


@app.cell
def __(READ_DATA, mo, tdf):
    select_anomaly = None
    _stack_mo_list = []
    if READ_DATA:
        select_anomaly = mo.ui.dropdown(
            [c for c in tdf.columns], value=None
        )
        
        _stack_mo_list = [
            mo.md('### 異常フラグの選択').center(),
            mo.hstack([
                mo.md(f'異常フラグ: {select_anomaly}')])
        ]
    mo.vstack(_stack_mo_list)
    return select_anomaly,


@app.cell
def __(select_anomaly):
    ANOMALY_COLUMN = None
    if select_anomaly is not None:
        ANOMALY_COLUMN = select_anomaly.value
    return ANOMALY_COLUMN,


@app.cell
def __(eda_all_data, mo, plot_scatter, select_scatter_columns):
    mo.ui.tabs(
        {
            '⚜️ 異常と正常データの比較': mo.vstack([
                select_scatter_columns,
                plot_scatter
            ]),
            '💹 全てのデータに対するEDA': eda_all_data 
        }
    )
    return


@app.cell
def __(READ_DATA, mo, tdf):
    _stack_mo_list = []
    if READ_DATA:
        select_x = mo.ui.dropdown(
            [c for c in tdf.columns], value=tdf.columns[0]
        )
        select_y = mo.ui.dropdown(
            [c for c in tdf.columns], value=tdf.columns[1]
        )
        
        _stack_mo_list = [
            mo.md('### 異常と正常データの比較').center(),
            mo.hstack([
                mo.md(f'x軸: {select_x}'), mo.md(f'y軸: {select_y}')])
        ]
    select_scatter_columns = mo.vstack(_stack_mo_list)
    return select_scatter_columns, select_x, select_y


@app.cell
def __(ANOMALY_COLUMN, READ_DATA, alt, mo, select_x, select_y, tdf):
    chart = None

    _stack_mo_list = []
    if ANOMALY_COLUMN is None:
        _stack_mo_list.append(mo.md('異常フラグを示すカラムが選択されていません。前の設定で選択してください。').callout('warn'))
    elif READ_DATA & (ANOMALY_COLUMN is not None):
        chart = alt.Chart(tdf).mark_point().encode(
            x=alt.X(select_x.selected_key).scale(zero=False), # Encoding along the x-axis
            y=alt.Y(select_y.selected_key).scale(zero=False), # Encoding along the y-axis
            color=ANOMALY_COLUMN
        )
        
        chart = mo.ui.altair_chart(chart)
        _stack_mo_list.append(mo.md(f'{chart}'))
    plot_scatter = mo.vstack(_stack_mo_list)
    return chart, plot_scatter


@app.cell
def __(READ_DATA, mo, tdf):
    _stack_mo_list = []
    if READ_DATA:
        _stack_mo_list = [
            mo.md('## 全てのデータに対するEDA').center(),
            mo.ui.data_explorer(tdf)]
    eda_all_data = mo.vstack(_stack_mo_list)
    return eda_all_data,


@app.cell
def __(ANOMALY_COLUMN, mo):
    prep_switch = mo.ui.switch(label='前処理を実行する！', value=False)
    norm_checkbox = mo.ui.checkbox(value=True, label='正規化')
    onehot_checkbox = mo.ui.checkbox(value=True, label='One-Hot Encoding')
    pca_checkbox = mo.ui.checkbox(value=False, label='PCA（次元圧縮）')
    pca_compornents = mo.ui.slider(start=2, stop=10, step=1, label='PCAのパラメータ（n_compornents）')

    _stack_mo_list = [mo.md("""### 特別な前処理
    * ここでは事前に定義された特殊な前処理を選んで実施することができます。
    """)]

    if ANOMALY_COLUMN is None:
        _stack_mo_list.append(mo.md('異常フラグを示すカラムが選択されていないため、前処理が実施できません。前の設定で選択してください。').callout('warn'))
    else:
        _stack_mo_list += [
            mo.md('前処理を始める場合は設定を決めて下のSwitchを押してください。'),
            norm_checkbox,
            onehot_checkbox,
            mo.hstack([pca_checkbox,pca_compornents]).left(),
            prep_switch,
        ]
    mo.vstack(_stack_mo_list)
    return (
        norm_checkbox,
        onehot_checkbox,
        pca_checkbox,
        pca_compornents,
        prep_switch,
    )


@app.cell
def __(
    ANOMALY_COLUMN,
    PCA,
    StandardScaler,
    norm_checkbox,
    onehot_checkbox,
    pca_checkbox,
    pca_compornents,
    pd,
    prep_switch,
    tdf,
):
    normal_data = None

    if prep_switch.value: 
      # 前処理実行スイッチがONならばチェックボックスに従って以下を実施

        if onehot_checkbox.value:
          # On-hot Encordingの処理
            tf_df = pd.get_dummies(tdf)
            print('One-hot Encoding')
        
        # 正規化やPCAは正常データのみを用いるので取り出す
        machine_failure = tf_df[ANOMALY_COLUMN]
        normal_data = tf_df.loc[tf_df[ANOMALY_COLUMN] != 1].drop(ANOMALY_COLUMN, axis=1)
        tf_df = tf_df.drop(ANOMALY_COLUMN, axis=1)

        if norm_checkbox.value:
            # 正規化
            scl = StandardScaler()
            # 正常データだけで正規化
            normal_data = pd.DataFrame(
                scl.fit_transform(normal_data), columns=normal_data.columns, index=normal_data.index
            )
            # 全データを正規化
            tf_data = scl.transform(tf_df)
            tf_df = pd.DataFrame(tf_data, columns=tf_df.columns, index=tf_df.index)                      
            print('正規化')

        if pca_checkbox.value:
          # PCAの処理
            pca = PCA(n_components=pca_compornents.value)
            normal_data = pca.fit_transform(normal_data)
            _columns = tf_df.columns
            tf_data = pca.transform(tf_df)
            tf_df = pd.DataFrame(tf_data, columns=[f'Col_{n}' for n in range(pca_compornents.value)], index=tf_df.index)
        
        # あとで使う
        all_data = tf_df
    else:
        print('停止中')
    return all_data, machine_failure, normal_data, pca, scl, tf_data, tf_df


@app.cell
def __(all_data, machine_failure, mo, pd, prep_switch):
    # EDAにはdata_explorerを使う。前処理が行われていない場合はお知らせ
    _stack_mo_list = []
    if prep_switch.value: # 前処理実行スイッチがONならばEDAを表示
        _stack_mo_list.append(mo.md('## 前処理後のEDA').center())
        _stack_mo_list.append(
            mo.ui.data_explorer(pd.concat([all_data, machine_failure], axis=1))
        )
    else: # 前処理実行スイッチがOFFならばお知らせを表示
        _stack_mo_list.append(mo.md('前処理後ここにEDA Cellが表示されます。').callout('neutral'))
    prep_after_eda = mo.vstack(_stack_mo_list)
    return prep_after_eda,


@app.cell
def __(all_data, mo, prep_switch):
    _stack_mo_list = []
    if prep_switch.value:
        _obj_data = all_data.select_dtypes(include=object)
        if _obj_data.empty:
            _stack_mo_list.append(
                mo.md('入力バリデーション：数字のみでデータが構成されているため、学習に進むことができます！').callout(kind="info")
            )
        else:
            _stack_mo_list.append(
                mo.md(f'入力バリデーション：数字以外が含まれています！: {_obj_data}').callout(kind="error")
            )
    else:
        _stack_mo_list.append(
                mo.md('入力バリデーション：前処理実行後、ここで入力チェックが行われます。').callout(kind="warn")
            )
    validation = mo.vstack(_stack_mo_list)
    return validation,


@app.cell
def __(mo, prep_after_eda, validation):
    mo.ui.tabs({
        '✅前処理後のValidationチェック': validation,
        '💡前処理後のEDA': prep_after_eda
    })
    return


@app.cell
def __(mo):
    mo.md('---------------------------------')
    return


@app.cell
def __(mo):
    mo.md(
        """# 異常検知のプロット
        """
    )
    return


@app.cell
def __(kmeans_setting, knn_setting, mo):
    mo.vstack(
        [
            mo.md('### 学習の設定').center(),
            mo.ui.tabs(
                {
                '🧞‍♂️ KMeans': kmeans_setting,
                '🧜‍♀️ KNN':knn_setting
                }
            ),
            mo.md('--------')
        ]
    )
    return


@app.cell
def __(mo, n_clusters_max_slider, n_neighbors_slider):
    kmeans_setting = mo.md(
        f"""
        * KMeansではn_clustersでクラスタ数を選択することができます。
        * このアプリケーションでは以下の論文で最適なクラスタ数を探索します。探索するクラスタ数の最大値を以下の`n_clusters_max`で設定してください。
            * Stop using the elbow criterion for k-means and how to choose the number of clusters instead (https://arxiv.org/abs/2212.12189)
        {mo.hstack([
            n_clusters_max_slider, 
            mo.md(f'設定値: {n_clusters_max_slider.value}')]).left()
        }
        """
    )

    knn_setting = mo.md(
        f"""
        * KNNではn_neighborsで距離を測る近傍点の数を決定することができます。

        {mo.hstack([
            n_neighbors_slider, 
            mo.md(f'設定値: {n_neighbors_slider.value}')]).left()
            }
        """
    )
    return kmeans_setting, knn_setting


@app.cell
def __(mo):
    n_clusters_max_slider = mo.ui.slider(start=1, stop=100, step=5, label='n_clusters_max')
    n_neighbors_slider = mo.ui.slider(start=1, stop=30, step=1, label='n_neighbors')
    return n_clusters_max_slider, n_neighbors_slider


@app.cell
def __(mo, normal_data):
    train_switch = mo.ui.switch(value=False)

    _stack_mo_list = [mo.md('## 学習の実施').center()]

    if normal_data is None:
        _stack_mo_list.append(mo.md('前処理が実施されていないので、学習を実施できません。前処理を実施してください。').callout('warn'))
    else:
        _stack_mo_list = [
                    mo.md('学習を始める場合は設定を決めて下のRun Switchを押してください。'),
                    train_switch]
    mo.vstack(_stack_mo_list)
    return train_switch,


@app.cell
def __(kmeans_expect_sse_plot, kmeans_scatter_plot, knn_scatter_plot, mo):
    mo.ui.tabs(
        {
            '🧞‍♂️ KMeans': mo.vstack([mo.md(
                """## KMeansで異常検知
                * 一番近いクラスタからの距離で計算する
                """), 
                                   mo.hstack([kmeans_scatter_plot, kmeans_expect_sse_plot])
                                  ]),
            '🧜‍♀️ KNN': mo.vstack([mo.md('## KNNで異常検知'), knn_scatter_plot])
        }
    )
    return


@app.cell
def __(
    mo,
    n_clusters_max_slider,
    normal_data,
    plot_expect_sse,
    train_switch,
):
    # 学習の実施とexpect SSEの表示。
    _stack_mo_list = []
    if train_switch.value:
        n_compornents = n_clusters_max_slider.value
        # 内部は省略するが、plot_expect_sseで最適なクラスタ数と
        # 散布図が返るようになっている
        ax, last_idx = plot_expect_sse(n_compornents, normal_data)
        _stack_mo_list.append(mo.as_html(ax))
    else:
        _stack_mo_list.append(mo.md('学習実行後にここに最適なクラスタ数が表示されます。').callout('neutral'))

    kmeans_expect_sse_plot = mo.vstack(_stack_mo_list)
    return ax, kmeans_expect_sse_plot, last_idx, n_compornents


@app.cell
def __(
    KMeans,
    all_data,
    last_idx,
    machine_failure,
    mo,
    normal_data,
    np,
    pd,
    plt,
    train_switch,
):
    _stack_mo_list = []
    if train_switch.value: # 学習スイッチがONになったら
        # expect SSEで計算されたクラスタ数で学習
        kmeans = KMeans(n_clusters=last_idx, random_state=225)
        kmeans.fit(normal_data)
        # 各クラスタの重心からの距離を計算
        distance = kmeans.transform(all_data)
        # 各データのクラスタ番号を予測
        predict_labels = kmeans.predict(all_data)
        # 最も近いクラスタ番号との距離を計算し、各サンプルの異常度スコアを得る
        kmeans_anomaly_scores = pd.DataFrame(
            np.array([a[i] for a, i in zip(distance, predict_labels)]), index=all_data.index
        )

        #　正常データのプロット
        _normal_index = list(machine_failure.loc[machine_failure == 0].index)
        plt.scatter(_normal_index, kmeans_anomaly_scores.loc[_normal_index])
        # 異常データのプロット
        _anomaly_index = list(machine_failure.loc[machine_failure == 1].index)
        _ax = plt.scatter(_anomaly_index, kmeans_anomaly_scores.loc[_anomaly_index])
        plt.title('Anomaly Score plot')
        plt.legend(['normal', 'anomaly'])
        # 結果をリストに入れる
        _stack_mo_list.append(mo.as_html(_ax))
    else:
        _stack_mo_list.append(mo.md('学習実行後にここにプロットが表示されます。').callout('neutral'))
    # 結果をUI Elementsとして定義
    kmeans_scatter_plot = mo.vstack(_stack_mo_list)
    return (
        distance,
        kmeans,
        kmeans_anomaly_scores,
        kmeans_scatter_plot,
        predict_labels,
    )


@app.cell
def __(
    NearestNeighbors,
    all_data,
    machine_failure,
    mo,
    n_neighbors_slider,
    normal_data,
    pd,
    plt,
    train_switch,
):
    _stack_mo_list = []
    if train_switch.value: # 学習スイッチがONなら
        # 設定した近傍数で学習
        n_neighbors = n_neighbors_slider.value
        knn = NearestNeighbors(n_neighbors=n_neighbors)
        knn.fit(normal_data)
        # 設定した近傍との距離を計算し、その平均値を異常度スコアとする
        distances, indexes = knn.kneighbors(all_data)
        knn_anomaly_scores = pd.DataFrame(
            distances.mean(axis=1), index=all_data.index)

        # 正常データのプロット
        _normal_index = list(machine_failure.loc[machine_failure == 0].index)
        plt.scatter(_normal_index, knn_anomaly_scores.loc[_normal_index])
        # 異常データのプロット
        _anomaly_index = list(machine_failure.loc[machine_failure == 1].index)
        _ax = plt.scatter(_anomaly_index, knn_anomaly_scores.loc[_anomaly_index])
        plt.title('Anomaly Scores')
        plt.legend(['normal', 'anomaly'])
        _stack_mo_list.append(mo.as_html(_ax))
    else:
        _stack_mo_list.append(mo.md('学習実行後にここにプロットが表示されます。').callout('neutral'))
    # 結果をUI Elementsとして定義
    knn_scatter_plot = mo.vstack(_stack_mo_list)
    return (
        distances,
        indexes,
        knn,
        knn_anomaly_scores,
        knn_scatter_plot,
        n_neighbors,
    )


@app.cell
def __():
    from io import StringIO

    import marimo as mo
    import pandas as pd
    import altair as alt
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.cluster import KMeans
    from sklearn.neighbors import NearestNeighbors
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    return (
        KMeans,
        NearestNeighbors,
        PCA,
        StandardScaler,
        StringIO,
        alt,
        mo,
        np,
        pd,
        plt,
    )


@app.cell
def __(KMeans, np, plt):
    def plot_expect_sse(n_compornents, df):
        # https://arxiv.org/abs/2212.12189
        # いい感じのクラスタ数を見る
        sse_list = []
        sse_exp_list = []

        N = df.shape[0]

        for k in range(1, n_compornents+1):

            kmeans = KMeans(n_clusters=k, random_state=18).fit(df)

            # k番目の時の期待値を格納
            if k > 1:
                sse_k_hat = ((N-k)/k) * np.min(np.array(sse_list))
            else:
                sse_k_hat = kmeans.inertia_
            sse_exp_list.append(np.sqrt(kmeans.inertia_ / sse_k_hat))

            # k番目のSSEを格納
            sse_list.append((k/(N-k)) * kmeans.inertia_)

        print(sse_exp_list)

        last_reduction_idx = explore_last_reduction(sse_exp_list)

        # 可視化
        plt.hlines(1.0, xmin=0, xmax=n_compornents+1, color="black", linestyle='dashed')
        plt.vlines(last_reduction_idx+1, ymin=sse_exp_list[last_reduction_idx], 
                   ymax=1.0, color="red")
        ax = plt.scatter(range(1, n_compornents+1), sse_exp_list)
        plt.title(f'Expected SSE plot: Optimal n_cluster is {last_reduction_idx+1}')

        print('last reduction: ', last_reduction_idx+1)

        return ax, last_reduction_idx+1

    def explore_last_reduction(sse_exp_list):
        # 1.0を超える直前のindexを返す
        last_index = 0
        for i, e in enumerate(sse_exp_list):
            if (i > 1) & (e > 1.0) & (sse_exp_list[i-1] < 1.0):
                last_index = i-1
        return last_index
    return explore_last_reduction, plot_expect_sse


if __name__ == "__main__":
    app.run()
