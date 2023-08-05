# Markmini

Python bindings for markmini package

Usage:

```py
import markmini

md = markmini.Markmini()

usernames = ["iverks", "testy"]
user_ids = ["1", "2"]
links = [f"/users/{id}" for id in user_ids]
fullnames = ["Iver Småge", "Testy McTestFace"]

md.add_users(usernames, user_ids, links, fullnames)

inp: str = """
# Header

 - List
 - more list

More _markdown_

@testy is my favorite user
"""

response = md.compile(inp)
```
