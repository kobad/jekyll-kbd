---
layout: post
title: "OSM To mbtiles"
date: 2017-07-09 03:59:26
categories: "other"
toc: true
---

* TOC
{:toc}

## OpenStreetMapからmbtilesを生成する

めちゃくちゃ時間食ったのでメモ

手順としては以下の通り
1. 欲しいマップの.osmファイルをDL
2. osmからpngに分割変換
3. pngからmbtilesに変換

## 1. osmファイル
[http://download.bbbike.org/osm/](http://download.bbbike.org/osm/)からダウンロードできる。

主要な国とかは1からDLできるが、そこに無い又は自分で範囲指定したい時は2に飛んで範囲を指定して

`OSM XML gzip`, e-mail, 適当な名前を決めてextractを押すと数分後にメールが届くのでそこのリンクからDLできる。

![osm](https://kobadlve.github.io/assets/images/osm.png)

DLできたら解凍しとく

## 2. pngに変換

[maperitive](http://maperitive.net/)を使う.

DLして起動したら、File>Open OSM>1でDLしたosmを開く。

Tool>Command Promptを開くと下にコマンド入力するところがでるので, `generate-tiles minzoom=12 maxzoom=14`(ズームレベルはご自由に)

生成が終わったら、`/username/AppData/Local/Temp/Rar$EXxxx/Maperitive/Tiles`に生成されてます。

## 3. mbtiles変換

[mbutil](https://github.com/mapbox/mbutil)を使う.

Install: `$ easy_install mbutil`

2で生成したフォルダに対して

```
$ mb-util Tiles map.mbtiles
```

で作れた.
