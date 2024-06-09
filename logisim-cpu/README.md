# マウスぽちぽちでできる！2週間で作って理解するCPU

書籍本体はこちら: [機械学習の炊いたん９。](https://techbookfest.org/product/aS0LEeuYmv20msS2tKHDi6)

## 章の概要

LLM や生成 AI 隆盛の今、GPU、AI アクセラレータなどのハードウェア 、計算資源についてよく耳にするようになりました。ただ、それらが通常の CPU と何が違い、どう嬉しいのか。一度助走として CPU 自体を知ることで、記事や本を読むにしても理解の解像度が上がります。今回は 2 週間強、GUI のマウスぽちぽちで CPU を自作しながら、ハンズオンでそのメカニズムを体得してみましょう。

## 2週間あまりでCPUを自作する

logisimを使い、以下のステップでCPUを作ってみましょう。各日の完成ファイル、および動作動画へのリンクは、GitHub: [https://github.com/ml-titans/titan9-codes](https://github.com/ml-titans/titan9-codes)から確認いただけます。

- **Week 1**
    - **Day 1** logisim-evolutionのインストール
    - **Day 2** 論理ゲートを試してlogisimの操作に慣れる
    - **Day 3** 真理値表を知り、回路の自動生成を試す
    - **Day 4** 組合せ回路 - 桁上がりを考慮しない半加算器を作ってみよう
    - **Day 5** 組合せ回路 - 4 bitの加算回路を作ってみよう
    - **Day 6** 組合せ回路 - 3 bit加算回路と10進数の7セグLED表示で簡易電卓に仕上げる
    - **Day 7** 順序回路 - Dフリップフロップに挑戦 (失敗)
- **Week 2**
    - **Day 8** 順序回路 - SRラッチ、DラッチからDフリップフロップまでをおさらい
    - **Day 9** 組合せ回路 + 順序回路 - 3bit加算回路の電卓にメモリ機能を加える
    - **Day 10** 命令セット (ISA) に想いを馳せる
    - **Day 11** ADD, NOP 2命令を持つCPUみたいなものができた
    - **Day 12** レジスタ2つの入出力を、マルチプレクサで切り替える (失敗)
    - **Day 13** 2つの命令、4つのステップで「111-11」の引き算をする
    - **Day 14** プログラムの手動実行から自動実行へ - ROMの仕組みを知ろう
- **Week 3**
    - **Day 15** ROMにプログラムを書き込み、カウンタと接続する
    - **Day 16** プログラムを自動実行するには - 「111-11」を永遠に計算し続ける機械

## 参考書籍、今後の発展

### GPU、AIアクセラレータをさらに知る

- [GPUを支える技術 ――超並列ハードウェアの快進撃](https://amzn.to/3VAygnF)

### CPU自作の発展

- [動かしてわかる CPUの作り方10講](https://amzn.to/3uOp6dF)
- [Build an 8-bit computer from scratch](https://eater.net/8bit)
- CODE - コードから見たコンピュータのからくり
  - [第1版 (2003/4/14)](https://t.co/N9WX2LdY8A)
  - [第2版 (2024/2/22))](https://t.co/HzSITbMn01)
- [RISC-VとChiselで学ぶ　はじめてのCPU自作 --オープンソース命令セットによるカスタムCPU実装への第一歩](https://amzn.to/3uJpxWK)
- [コンピュータの構成と設計 MIPS Edition 第6版 上・下電子合本版](https://amzn.to/3SV0GHg)
- [grself/CIS221\_Lab\_Manual: This is the Logisim-Evolution lab manual I use with my Cochise College CIS 221 Digital Logic class.](https://github.com/grself/CIS221_Lab_Manual)
- [Visual 6502 Remix](https://floooh.github.io/visual6502remix/)
- [CIS 221: Logisim-Evolution Labs 再生リスト](https://youtube.com/playlist?list=PLvjlcTfwDj4spSN4g3S8IHbqY4Qkb5LxP&si=ihZGoc8z_BW_BCFK)
