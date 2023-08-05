#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint:disable=invalid-name,unused-argument,too-many-arguments

"""
Use fontawesome icons
"""

import re
import uuid

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives

from sphinx.writers.html import HTMLTranslator
from sphinx.writers.latex import LaTeXTranslator
from sphinx.writers.texinfo import TexinfoTranslator
from sphinx.writers.text import TextTranslator
from sphinx.writers.manpage import ManualPageTranslator
from sphinx.util.osutil import relative_uri

__version_info__ = (2, 0, 0)
__version__ = '.'.join([str(val) for val in __version_info__])


class fa(nodes.General, nodes.Inline, nodes.Element):
    """Generic node for FontAwesome"""


class falink(nodes.General, nodes.Inline, nodes.Element):
    """Generic link node for FontAwesome"""


def append_fa_image(self: HTMLTranslator, node: fa or falink) -> None:
    """Add image to node"""
    path = {
        'brands': self.builder.config.fa_brands_path,
        'regular': self.builder.config.fa_regular_path,
        'solid': self.builder.config.fa_solid_path,
    }[node['iconset']]

    path = relative_uri(
        self.builder.current_docname,
        self.builder.get_asset_paths()[0] + '/' + path
    )

    label_uid = uuid.uuid4()
    title = None
    options = 'role="img"'
    options += ' xmlns="http://www.w3.org/2000/svg"'
    options += ' xmlns:xlink="http://www.w3.org/1999/xlink"'
    if node.get('alt', None):
        options += f' aria-labelledby="fa_{label_uid}"'
        title = f'<title id="{label_uid}">{node["alt"]}</title>'
    else:
        options += ' aria-hidden="true" xlink:title=""'

    if node.get('html_id', None):
        options += f' id={node["html_id"]}'

    options += f' class="fasvg {node.get("html_class", "") or ""}"'

    self.body.append(
        f'<svg {options}>'
    )

    if title:
        self.body.append(title)

    self.body.append(
        f'<use xlink:href="{path}#{node["icon"]}"></use></svg>'
    )


def html_visit_fa(self: HTMLTranslator, node: fa) -> None:
    """Rendering FA node in HTML"""
    append_fa_image(self, node)
    raise nodes.SkipNode


def latex_visit_fa(self: LaTeXTranslator, node: fa) -> None:
    """Rendering FA node in LaTeX"""
    if 'alt' in node.attributes:
        self.body.append(f'[{node["alt"]}]')
    raise nodes.SkipNode


def texinfo_visit_fa(self: TexinfoTranslator, node: fa) -> None:
    """Rendering FA node in TeXinfo"""
    if 'alt' in node.attributes:
        self.body.append(f'[{node["alt"]}]')
    raise nodes.SkipNode


def text_visit_fa(self: TextTranslator, node: fa) -> None:
    """Rendering FA node in text"""
    if 'alt' in node.attributes:
        self.add_text(f'[{node["alt"]}]')
    raise nodes.SkipNode


def gemini_visit_fa(self, node: fa) -> None:
    """Rendering FA node in Gemini"""
    if 'alt' in node.attributes:
        self.add_text(f'[{node["alt"]}]')
    raise nodes.SkipNode


def man_visit_fa(self: ManualPageTranslator, node: fa) -> None:
    """Rendering FA node in Man file"""
    if 'alt' in node.attributes:
        self.body.append(f'[{node["alt"]}]')
    raise nodes.SkipNode


def create_fa_node(iconset, icon, html_id=None, html_class=None, alt=None):
    """Create FA node"""
    node = fa()
    node['iconset'] = iconset
    node['icon'] = icon
    node['html_id'] = html_id
    node['html_class'] = html_class
    node['alt'] = alt or ''
    return node


def html_visit_falink(self: HTMLTranslator, node: fa) -> None:
    """Rendering FA link node in HTML"""
    self.body.append(
        f'<a class="fasvglink {node["icon"]}" href="{node["url"]}">'
    )
    append_fa_image(self, node)

    self.body.append(f' {node["text"]}</a>')
    raise nodes.SkipNode


def latex_visit_falink(self: LaTeXTranslator, node: fa) -> None:
    """Rendering FA link node in LaTeX"""
    self.body.append(
        f'\\href{{{node["url"]}}}'
        f'{{{node["alt"]} {node["text"]}}}'
    )
    raise nodes.SkipNode


def texinfo_visit_falink(self: TexinfoTranslator, node: fa) -> None:
    """Rendering FA link node in TexInfo"""
    self.body.append(
        f'\\href{{{node["url"]}}}{{{node["alt"]} {node["text"]}}}'
    )
    raise nodes.SkipNode


def text_visit_falink(self: TextTranslator, node: fa) -> None:
    """Rendering FA link node in text"""
    self.add_text(
        f'{node["alt"]} {node["text"]} <{node["url"]}>'
    )
    raise nodes.SkipNode


def gemini_visit_falink(self, node: fa) -> None:
    """Rendering FA link node in Gemini"""
    self.end_block()
    self.add_text(
        f'=> {node["alt"]} {node["url"]} {node["text"]}'
    )
    self.end_block()
    raise nodes.SkipNode


def man_visit_falink(self: ManualPageTranslator, node: fa) -> None:
    """Rendering FA link node in Man file"""
    self.body.append(f'{node["text"]} {node["alt"]} <{node["url"]}>')
    raise nodes.SkipNode


def create_falink_node(iconset, text):
    """Create a new link node depending of text and iconset"""
    node = falink()
    regex = re.compile(
        r'(?P<icon> *[a-zA-Z-_]* *):(?P<text>.*)'
        + r'(?P<alt>\[.*\] *)?<(?P<url>.*)>')
    parsed = regex.search(text)
    node['iconset'] = iconset
    node['icon'] = parsed.group('icon').strip()
    node['url'] = parsed.group('url').strip()
    node['alt'] = (parsed.group('alt') or '').strip().strip('[]')
    node['text'] = parsed.group('text').strip()
    return node


def fab(role, rawtext, text, lineno, inliner, options=None, content=None):
    """Node for FontAwesome brand icon"""
    if not options:
        options = {}
    if not content:
        content = []
    regex = re.compile(r'(?P<icon>[a-zA-Z-_]*)(?P<alt>\[.*\] *)?')
    parsed = regex.search(text)
    alt = (parsed.group('alt') or '').strip().strip('[]')
    icon = parsed.group('icon').strip()
    return [create_fa_node('brands', icon, alt=alt)], []


def far(role, rawtext, text, lineno, inliner, options=None, content=None):
    """Node for FontAwesome regular icon"""
    if not options:
        options = {}
    if not content:
        content = []
    regex = re.compile(r'(?P<icon>[a-zA-Z-_]*)(?P<alt>\[.*\] *)?')
    parsed = regex.search(text)
    alt = (parsed.group('alt') or '').strip().strip('[]')
    icon = parsed.group('icon').strip()
    return [create_fa_node('regular', icon, alt=alt)], []


def fas(role, rawtext, text, lineno, inliner, options=None, content=None):
    """Node for FontAwesome solid icon"""
    if not options:
        options = {}
    if not content:
        content = []
    regex = re.compile(r'(?P<icon>[a-zA-Z-_]*)(?P<alt>\[.*\] *)?')
    parsed = regex.search(text)
    alt = (parsed.group('alt') or '').strip().strip('[]')
    icon = parsed.group('icon').strip()
    return [create_fa_node('solid', icon, alt=alt)], []


def fablink(role, rawtext, text, lineno, inliner, options=None, content=None):
    """Node for link with FontAwesome brands iconset"""
    if not options:
        options = {}
    if not content:
        content = []
    return [create_falink_node('brands', text)], []


def farlink(role, rawtext, text, lineno, inliner, options=None, content=None):
    """Node for link with FontAwesome regular iconset"""
    if not options:
        options = {}
    if not content:
        content = []
    return [create_falink_node('regular', text)], []


def faslink(role, rawtext, text, lineno, inliner, options=None, content=None):
    """Node for link with FontAwesome solid iconset"""
    if not options:
        options = {}
    if not content:
        content = []
    return [create_falink_node('solid', text)], []


class FaDirective(Directive):
    """ Main directive for FontAwesome icons """

    has_content = False
    required_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        "class": directives.unchanged,
        "id": directives.unchanged,
        "alt": directives.unchanged,
    }
    iconset = None

    def run(self):
        node = create_fa_node(
            self.iconset,
            self.arguments[0],
            self.options['id'],
            self.options['class'],
            self.options['alt']
        )
        return [node]


class Fab(FaDirective):
    """ Directive for FontAwesome brands iconset """
    iconset = 'brands'


class Far(FaDirective):
    """ Directive for FontAwesome regular iconset """
    iconset = 'regular'


class Fas(FaDirective):
    """ Directive for FontAwesome solid iconset """
    iconset = 'solid'


def setup(app):
    """
    Setup Sphinx app
    """
    app.add_node(
        fa,
        html=(html_visit_fa, None),
        epub=(html_visit_fa, None),
        latex=(latex_visit_fa, None),
        texinfo=(texinfo_visit_fa, None),
        text=(text_visit_fa, None),
        man=(man_visit_fa, None),
        gemini=(gemini_visit_fa, None),
    )
    app.add_node(
        falink,
        html=(html_visit_falink, None),
        epub=(html_visit_falink, None),
        latex=(latex_visit_falink, None),
        texinfo=(texinfo_visit_falink, None),
        text=(text_visit_falink, None),
        man=(man_visit_falink, None),
        gemini=(gemini_visit_falink, None),
    )
    app.add_config_value('fa_brands_path', 'fa/brands.svg', True)
    app.add_config_value('fa_regular_path', 'fa/regular.svg', True)
    app.add_config_value('fa_solid_path', 'fa/solid.svg', True)
    app.add_role('fab', fab)
    app.add_role('fas', fas)
    app.add_role('far', far)
    app.add_role('fablink', fablink)
    app.add_role('faslink', faslink)
    app.add_role('farlink', farlink)
    app.add_directive('fab', Fab)
    app.add_directive('fas', Fas)
    app.add_directive('far', Far)
    return {'version': __version__}
