# Random Text File Access (by line number)

Quickly access arbitrary line numbers in a text file. A well tested library for Python 3.

**Example Usage**

```python
# https://raw.githubusercontent.com/redacted/XKCD-password-generator/master/xkcdpass/static/default.txt
with IndexedOpen('xkcd_wordlist.txt') as indexed_f:
    pw = ' '.join(indexed_f.random_line().strip() for _ in range(4))

    print(pw)                # 'correct horse battery staple'      
    print(indexed_f[4:8])    # ["'neath\n", "'nother\n", "'til\n", "'tis\n"]
    print(indexed_f[-4:-2])  # ["zygosis\n", "zygote\n"]
    print(indexed_f[5])      # "'nother\n"
```


## Author

Bryce Drennan <random-line-access@brycedrennan.com>