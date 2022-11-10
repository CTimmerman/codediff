# Diff without ANY white space changes

```bash
$ diff a.txt b.txt |python ignore_newlines.py
6,7c7,8
< second
< diff
---
> second diff
> and more!

$ diff -c0 a.txt b.txt |python ignore_newlines.py -c
*** a.txt       2021-12-11 22:16:26.478662800 +0100
--- b.txt       2021-12-11 23:50:41.235329900 +0100
***************
*** 6,7 ****
! second
! diff
--- 7,8 ----
! second diff
! and more!

$ diff -u0 a.txt b.txt |python ignore_newlines.py -u
--- a.txt       2021-12-11 22:16:26.478662800 +0100
+++ b.txt       2021-12-11 23:50:41.235329900 +0100
@@ -6,2 +7,2 @@
-second
-diff
+second diff
+and more!

```
Because even TortoiseGitMerge doesn't skip newlines:
![image](https://user-images.githubusercontent.com/9662163/201135057-ed14f0e3-a370-4f8c-9d2c-101781a27a9f.png)

