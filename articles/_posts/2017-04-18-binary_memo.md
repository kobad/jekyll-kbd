---
layout: post
title: "Register..."
date: 2017-04-19 23:00:00 +0900
categories: ctf
---

## Register
### 汎用レジスタ
* EAX(アキュムレータレジスタ) - 演算の結果
* ECX(カウンタレジスタ) - ループのカウントなど
* EDX(データレジスタ) - 演算に用いるデータ
* EBX(ベースレジスタ) - アドレスのベース値
* ESI(ソースインデックスレジスタ) - 一部のデータ転送命令で、データの転送元を格納
* EDI(デスティネーションインデックスレジスタ) - 一部のデータ転送命令で、データの転送先を格納

### 特殊レジスタ
* EBP(ベースポインタレジスタ) - 現在のスタックフレームにおける底のアドレスを保持
* ESP(スタックポインタレジスタ) - 現在のスタックトップのアドレスを保持
* EIP(インストラクションポインタレジスタ) - 次に実行する命令のアドレス

### フラグ
* CF(キャリーフラグ) - 演算命令で桁上がりか桁借りが発生時にセット
* ZF(ゼロフラグ) - 操作結果が0の時セット
* SF(符号フラグ) - 操作結果が負の時セット
* DF(方向フラグ) - ストリームの方向を制御
* OF(オーバーフローフラグ) - 符号付き算術演算の結果がレジスタの格納可能範囲を超えた時セット

### セグメントレジスタ
* CS(コードセグメントレジスタ) - コードセグメントのアドレス
* DS(データセグメントレジスタ) - データセグメントのアドレス
* SS(スタックセグメントレジスタ) - スタックセグメントレジスタのアドレス
* ES(エクストラセグメントレジスタ) - エクストラセグメントのアドレス
* FS(Fセグメントレジスタ) - Fセグメント(2つ目の追加セグメント)アドレス
* GS(Gセグメントレジスタ) - Gセグメント(３つ目の追加セグメント)アドレス

## 記法
* b - byte - 8bit
* s - short(16bit整数) - single(32bit浮動小数点)
* w - word - 16bit
* l - long(32bit整数) - double(64bit浮動小数点)
* q - quad(64bit)
* t - 10byte - 80bit浮動小数点
* BYTE - 8bit
* WORD - 16bit
* DWORD - 32bit
* QWORD - 64bit

## 代表命令

* `mov dest, src` - dest = src
* `lea dest, src` - dest = srcAddress
* `xchg dest1, dest2` - xchange dest1 dest2
* `lodsb - lodsw - lodsd` - [DS:ESI]のメモリ内容を、(b, word, dword)バイト分(b)ALレジスタに読み込み、ESIレジスタをDFレジスタに基づいて読み込んだサイズ分加算・減算。
* `stosb` - ALレジスタの値を(b, word, dword)バイト分、[ES:ESI]メモリに書き込み、EDIレジスタをDFレジスタに基づいて読み込んだサイズ分加算・減算
* `push s r c` - argオペランドの値をスタックにpush. ESPレジスタの値をレジスタ幅分(32bit -> 4byte, 64bit -> 8byte)減算し、argオペランドをESPレジスタのさすスタックのトップに格納
* `pop dest` - スタックからargオペランドへpop. ESPレジスタの指すスタックのトップの値をargオペランドへ格納し、ESPレジスタの値をレジスタ幅分(32bit -> 4byte, 64bit -> 8byte)減算
* `add dest, src` - src = src + dest
* `sub dest, src` - src = src - dest
* `mul` - srcオペランドにEAXレジスタの値を乗算し、結果の上位４位バイトをEDXレジスタに格納し下位４バイトをEAXに格納
* `div src` - EDX:EAXの８バイトをsrcバイトの値で除算する。商をEAXレジスタに剰余をEDXレジスタに格納
* `inc dest` - dest++
* `dec dest` - dest--
* `cmp src1, src2` - 減算するが結果は破棄され、結果に伴ってフラグレジスタを変化させる。
* `shr/shl dest, count` - destオペランドcountオペランドで指定したビット数分、それぞれ左、右にビットシフトし、結果をdestに格納。
* `ror/rol dest, count` - destオペランドcountオペランドで指定したビット数分、ローテートさせ、結果をdestに格納。
* `xor dest, src` - dest xor src. xor eax eax で初期化
* `test src1, src2` - 論理積を取る。結果からフラグレジスタを変化
* `jmp arg` - フラグレジスタを参照して、分岐
* `call arg` - jmpの拡張。分岐後にret命令で戻れるように、callの次の命令アドレスを戻り先としてスタックに保存
* `ret` - call元の次の命令へと実行を戻す
* `leave` - データ転送命令。retとセットで使われる。retの前に呼ばれ、スタックポインタをベースポインタと同じ位置に戻し、ベースポインタを復元。`mov esp, edp, pop edp`と同じ動作。

## 分岐

* ZF = 0           : JE(jump if equal), JZ(jump if zero)
* ZF = 0           : JNE(jump if not equal), JNZ(jump if not zero)
* ZF = 0 && SF = OF: JG(jump if greater)
* SF <> OF         : L(jump if less)

## 呼び出し規約

* stdcall  - 後ろの引数からpushされ、返り値はeaxに格納
* cdecl    - 後ろの引数からpushされ、ESPレジスタの値を戻す処理が呼ばれて、返り値をeaxに格納
* fastcall - 左から右への引数リストで見つかる最初の 2 つの DWORD またはこれより小さい引数は、ECX および EDX レジスタに渡されます。他の引数はすべてスタック上で右から左へ渡されます。 ESPレジスタの値を戻す処理が呼ばれて、返り値をeaxに格納

## セキュリティ機構

* RELRO(RELocation ReadOnly) - データのどこにReadOnly属性をつけるか。checksecで調べる
  * No RERLO
  * Partial RELRO(Lazy)
  * Full RELRO(Now) - GOTOverWriteできない
* Stack Smash Protection - スタック上でのBOFを防ぐ。スタックフレームのローカル変数領域とSaved EBPの間にCanaryを挿入し、関数終了時に書き換えられてるかを判定して検出し強制終了。
  * Canaryの値は乱数。先頭がNULLバイトになるようにして、ローカル変数に置かれた文字列がNULLバイトで終わっていなかった時に、Canaryが流出するのを防ぐ。
  * -fno-stack-protector オプションで無効化
* NX bit(No eXecute bit), DEP(Data Execution Prevention) - メモリ上の実行する必要のないデータを実行不可能に設定して、不正に実行されるのを防ぐ。
  * -z execstack オプションで無効化
* ASLR(Address Layout Randomization) - スタックやヒープ、共有ライブラリなどをメモリに配置する際にアドレスの一部をランダム化しアドレス推測を困難にする。
  * OFF: sudo sysctl -w kernel.randomize_va_space=0
  * ON : sudo sysctl -w kernel.randomize_va_space=2
* PIE(Position Independent Executable) - 実行コード内のアドレス参照を全て相対アドレスで行い、実行ファイルがメモリのどこに置かれても実行できるようにコンパイルされたファイル。



## Return to PLT(Procedure Linkage Table)
PLTに書かれた短いコード片を関数として呼び出すと、動的リンクされたライブラリのアドレスを解決してライブラリ内の関数を実行してくれる。

## Return to libc
system関数などのlibc内の関数を呼び出す。

## ROP (Return Oriented Programming)
ret命令で終わる命令列の先頭へのジャンプを繰り返すことで、任意の命令列を実行させる
