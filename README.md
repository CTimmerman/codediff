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