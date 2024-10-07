from urllib.request import urlopen
import dash
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    # external_stylesheets=external_stylesheets,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}],  # Responsive to MOBILE
    use_pages=True
)

# https://www.sportscheck.com/filialen/
url = "http://olympus.realpython.org/profiles/aphrodite"
page = urlopen(url)

# urlopen() returns an HTTPResponse object:
html_bytes = page.read()
html = html_bytes.decode("utf-8")


title_index = html.find("<title>")
# >>> title_index
start_index = title_index + len("<title>")
# >>> start_index

end_index = html.find("</title>")
# >>> end_index

title = html[start_index:end_index]
# >>> title


# url = "http://olympus.realpython.org/profiles/poseidon"
# >>> page = urlopen(url)
# >>> html = page.read().decode("utf-8")
# >>> start_index = html.find("<title>") + len("<title>")
# >>> end_index = html.find("</title>")
# >>> title = html[start_index:end_index]
# >>> title

if __name__ == "__main__":
    app.run(
        debug=True,
        port=8051
    )