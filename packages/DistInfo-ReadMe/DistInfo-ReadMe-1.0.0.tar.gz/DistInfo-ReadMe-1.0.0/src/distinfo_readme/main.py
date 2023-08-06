import sys, os, time, argparse, tempfile, webbrowser
import readme_renderer.rst, readme_renderer.txt, readme_renderer.markdown
from importlib.metadata import distribution
from email.message import EmailMessage
from . import __version__
from . import __path__ as _path


_html_part = \
'''
<!DOCTYPE html>
<html dir="ltr" lang="en">
	<head>
		<meta http-equiv="content-type" content="text/html; charset=UTF-8">
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<meta name="defaultLanguage" content="en">
		<title>{0:s} - {1:s}</title>
		<link rel="stylesheet" href="{2:s}/readme-ltr.css">
		<link rel="stylesheet" href="{2:s}/css.css">
		<link rel="icon" href="{2:s}/favicon.ico" type="image/x-icon">
	</head>
	<body data-controller="viewport-toggle" style="padding-top: 0px;">
		<main id="content">
			<div data-controller="project-tabs" data-project-tabs-content="description">
				<div class="tabs-container">
					<div class="vertical-tabs">
						<div class="vertical-tabs__panel">
							<div id="description" data-project-tabs-target="content" class="vertical-tabs__content" role="tabpanel" aria-labelledby="description-tab mobile-description-tab" tabindex="-1" style="display: block;">
								<h2 class="page-title">Project description</h2>
								<div class="project-description">
									{3:s}
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</main>
	</body>
</html>
'''

_RENDERERS = {None           : readme_renderer.rst,
              ''             : readme_renderer.rst,
              'text/x-rst'   : readme_renderer.rst,
              'text/plain'   : readme_renderer.txt,
              'text/markdown': readme_renderer.markdown}

def _main():
    txt = 'A postviewing of the readme of installed Python projects'
    parser = argparse.ArgumentParser(prog = __package__, description = txt)
    parser.add_argument('-V', '--version', action = 'version',
                        version = __version__)
    parser.add_argument('package', help = 'name of installed package')
    parser.add_argument('-b', '--browser-type')
    parser.add_argument('-t', '--timeout', default = 2, type = float,
                        help = 'wait for webbrowser to open temporary HTML '
                               'file (default 2 s)')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    args = parser.parse_args()
    post_view(args.package, args.browser_type, args.timeout, cli = True)

def _render(value, content_type = None, use_fallback = True):
    if value is None:
        value = ''
    if content_type:
        msg = EmailMessage()
        msg['content-type'] = content_type
        content_type = msg.get_content_type()
    renderer = _RENDERERS.get(content_type, readme_renderer.txt)
    rendered = renderer.render(value)
    if use_fallback and rendered is None:
        renderer = _RENDERERS['text/plain']
        rendered = renderer.render(value)
    if renderer == _RENDERERS['text/plain']:
        rendered = f'<pre>{rendered}</pre>'
    return rendered

def post_view(distribution_name = '', browser_type = None, timeout = 2,
              cli = False):
    try:
        timeout = float(timeout)
        browser = webbrowser.get(browser_type)
        dist = distribution(distribution_name)
        name = dist.metadata['Name']
        version = dist.metadata['Version']
        content_type = dist.metadata['Description-Content-Type']
        description = dist.metadata['Description']
        resources = os.path.join(_path[0], 'resources')
        rendered = _render(description, content_type)
        html = _html_part.format(name, version, resources, rendered)
        tmp = tempfile.NamedTemporaryFile(delete = False, suffix = '.html')
        html_file = tmp.name
        print('Creating HTML file {0:s}'.format(html_file))
        tmp.write(html.encode())
        tmp.close()
        browser.open_new_tab(html_file)
        time.sleep(timeout)
        os.unlink(html_file)
    except Exception as e:
        print(e)
        if cli:
            sys.exit(1)
