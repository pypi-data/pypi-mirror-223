# jupyter_browser_clipboard
Copy text to OS clipboard when using Jupyter remotely. This uses the web browser's
own clipboard via Javascript.

Originally a gist on github but got tired of copy pasting it into each notebooks.

## Installation

```bash
$ pip install jupyter_browser_clipboard
```

Or, alternatively,

```bash
$ pip install git+https://github.com/bsdz/jupyter_browser_clipboard.git#main
```

## Usage

```python
>>> from jupyter_browser_clipboard import BrowserClipboard
>>> df = pd.DataFrame(data=[1,2,3,5,6, 101])
>>> BrowserClipboard(df.to_csv(sep="\t"))
Copying text to browser's clipboard.. success!
```
