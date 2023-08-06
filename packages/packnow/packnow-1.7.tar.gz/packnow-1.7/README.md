# packnow
Pack everything now. Simple and (maybe) fast.

## 1. Get Packin'

```bash
$ packnow
```

## 2. Get Hostin'
Note: You can also set a password for hosting.

```bash
$ packnow host --file <zip file>
```

## 3. Just Get It!
...from other devices or platforms.

```bash
$ packnow get --url <packnow url>
```

## Packignore Files
Pretty much just like `.gitignore`, `.packignore` files will ignore files that are not going to be packed.

You could use our default templates, for instance, `replit-python`, or you can add your own.

You'll need to create a new `.packignore` file:

```python
# .packignore

# ignores chocolate.js for any directory
*/chocolate.js

# for dirs, suffix a slash
# ignores __pycache__ dir in any directory
*/__pycache__/

# ignores wow.cpp in the current dir
/wow.cpp

# again, for dirs, suffix a slash
# ignores directory my-stuff in the current dir
/my-stuff/

# ignores the specified full path contents
# (don't prefix / suffix a slash)
go/buy/milk
important/homework.py
```