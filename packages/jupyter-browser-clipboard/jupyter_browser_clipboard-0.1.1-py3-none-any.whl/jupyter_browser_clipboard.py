"""Copy text in remote Jupyter sessions.

Copy text to OS clipboard when using Jupyter remotely. Uses web browsers
clipboard via Javascript.

"""
from IPython.display import HTML
 
class BrowserClipboard(HTML):
    """Pauper's Jupyter clipboard.
    
    >>> df = pd.DataFrame(data=[1,2,3,5,6, 101])
    >>> BrowserClipboard(df.to_csv(sep="\t"))
    Copying text to browser's clipboard.. success!
    """

    def _repr_html_(self):
        return f"""
        Copying text to browser's clipboard.. <span id='foo'></span>
        <script type="text/Javascript">
            globalThis.__bc_data = `{self.data}`;
            var promise = navigator.clipboard.writeText(globalThis.__bc_data).then(function() {{
              document.getElementById("foo").innerHTML = "success!";
            }}, function() {{
              document.getElementById("foo").innerHTML = "failed :(";
            }});
        </script>
        """
