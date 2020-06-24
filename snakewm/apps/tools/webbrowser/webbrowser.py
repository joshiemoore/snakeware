from markdown2 import Markdown
import html2text
import pygame_gui
import pygame
import requests
from urllib.parse import urljoin


class Webbrowser(pygame_gui.elements.UIWindow):
    """
    Simple Webbrowser for Snakeware
    Licenced under MIT-License.
    Initial release by O. Wannenwetsch, github: deltaflyer

    This is a simple one-file webbrowser that renders HTML-pages
    as text format similar to Lynx or other web browser.

    IT DOES CURRENTLY NOT WORK IN NATIVE SNAKEWARE, DUE TO A MISSING
    NETWORK STACK. BUT IT WORKS SNAKEWM DEVELOPMENT ENVIRONMENTS ON LINUX / OSX.

    It supports retrieving webpages from HTTP(S) resources
    and renders HTML-source code with a minimalistic pipeline:
    html -> escaped html -> markdown -> simplified html for pygame.textbox html-rendering.

    For navigation, please use:
    * a valid URL, entered into to the textfield
    * ENTER for start browsing
    * back and forward button of the mouse to go back and forward
    * mouse-wheel for scrolling

    What does the browser not support:
    * multithreading: while the web browser is downlaoding and rendering content, snakewm will not update
    * anything that uses HTTP-verbs other than GET, e.g. POST (e.g. most forms)
    * image rendering
    * downloads
    * Javascript
    * Websockets and other protocol stuff, (sorry no www.goole.com)
    * Edge cases in rendering (its a simple hackend transforming and rendering pipeline)

    Contribute:
    * Help to get a network stack for Raspi, QEMU and VirtualBox into Snakeawre
    * Change what you like and submit a pull request with new features and fixes.

    """

    def __init__(self, pos, manager):
        # constants for mouse support
        self.MOUSE_BUTTONS = {
            'SCROLL_WHEEL_UP': 4,
            'SCROLL_WHEEL_DOWN': 5,
            'BACK_BUTTON': 8,
            'FORWARD_BUTTON': 9
        }

        # replacement map
        # input: simplified stripped html source code
        # output: html source code compatible with pygame text rendering capabilities
        self.REPLACE_MAP_STRIPPED_HTML = {
            '-ROBRACKET-': '(',
            '-RCBRACKET-': ')',
            '-EOBRACKET-': '[',
            '-ECBRACKTE-': ']',
            '\t': '&nbsp;&nbsp;&nbsp;&nbsp;',
            "\n": '<br>',
            "<p>": '',
            "<\p>": "<br>",
            "<ul>": "",
            "</ul>": "",
            "<li>": "* ",
            "</li>": "<br>",
            "<h1>": "<b>",
            "</h1>": "</b>",
            "<h2>": "<b>",
            "</h2>": "</b>",
            "<h>": "<b>",
            "</h1>": "</b>",
            "<blockquote>": "<i>",
            "</blockquote>": "</i>"
        }

        # replacement map
        # input: html source code
        # output html source code with escapes for mark down syntax
        self.REPLACE_MAP_FULL_HTML = {
            '(': '-ROBRACKET-',
            ')': '-RCBRACKET-',
            '[': '-EOBRACKET-',
            ']': '-ECBRACKTE-'
        }

        super().__init__(
            pygame.Rect(pos, (600, 400)),
            manager,
            window_display_title="Webbrowser",
            object_id="#webbrowser",
            resizable=True,
        )

        # data structure of the browser
        self.current_base_url = str()
        # the browser history is organized as a stack,
        # newly visited URLs are pushed on top.
        # when using the back and forward mouse button,
        # the URL history stack pointer is moved
        self.x_position = 0
        self.url_history_stack = []
        self.url_history_stack_pointer = 0
        # If a new URL is entered the history takes a new start for the last point
        self.is_newly_entered_url = False
        # Simple browser cache implemented as dict using the lower-case URL as key
        # and returns the process HTML for rendering as content (value)
        self.page_cache = {}
        self.markdowner = Markdown()

        self.page_content = pygame_gui.elements.UITextBox(
            "",
            relative_rect=pygame.Rect(0, 35, 568, 300),
            manager=manager,
            container=self,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom",
            },
        )

        self.input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(0, -337, 568, 30),
            manager=manager,
            container=self,
            anchors={
                "left": "left",
                "right": "right",
                "top": "bottom",
                "bottom": "bottom",
            },
        )
        self.input.focus()

    def process_string_with_map(self, string, map):
        """
        Proess as string with a given replacement map
        """
        result_string = string
        for key in map:
            result_string = result_string.replace(key, map[key])
        return result_string

    def process_event(self, event):
        """
        Process incoming events from snakewm
        """
        super().process_event(event)
        # handle Enter-key to start browsing
        if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
            self.is_newly_entered_url = True
            input_url = self.input.get_text()
            self.perform_browsing(input_url.lower())
            # cut the history
            self.url_history_stack = self.url_history_stack[0:self.url_history_stack_pointer]
        # handle clicking on links
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_TEXT_BOX_LINK_CLICKED:
                self.handle_link_click(event.link_target)
        # handle mouse-wheel scrolling and back and fore buttons..
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            position_update_requested = False
            # back-button
            if event.button == self.MOUSE_BUTTONS['BACK_BUTTON'] and self.url_history_stack_pointer != 0:
                self.url_history_stack_pointer -= 1
                self.perform_browsing(self.url_history_stack[self.url_history_stack_pointer])
            # forward-button
            if event.button == self.MOUSE_BUTTONS['FORWARD_BUTTON'] and (
                    len(self.url_history_stack) - 1) > self.url_history_stack_pointer:
                self.url_history_stack_pointer += 1
                self.perform_browsing(self.url_history_stack[self.url_history_stack_pointer])
            # mouse-wheel up
            if event.button == self.MOUSE_BUTTONS['SCROLL_WHEEL_UP'] and self.x_position != 0:
                self.x_position -= 1
                position_update_requested = True
            # mouse wheel down
            if event.button == self.MOUSE_BUTTONS['SCROLL_WHEEL_DOWN']:
                self.x_position += 1
                position_update_requested = True
            # update position
            if (self.page_content.scroll_bar is not None) and position_update_requested:
                self.page_content.scroll_bar.scroll_position = self.x_position
                self.page_content.scroll_bar.scroll_wheel_down = True

    def handle_link_click(self, url):
        """
        Starts browsing using a url retrieved from a click-link event
        """
        if (self.current_base_url not in url) and ('://' not in url):
            # Convert relative URL into full urls ()
            url = "{}{}".format(self.current_base_url, url)
            # Hack for fixing multi-line link containers that are the result of e.g. link extraction from images
            url = url.replace("//", "/").replace(":/", "://").replace("<br>", "")
        self.is_newly_entered_url = True
        self.perform_browsing(url)

    def render_links(self, stripped_html, base_url):
        """
        Helper methods for rendering links that use mark-down-like syntax
        """
        return self.markdowner.convert(stripped_html)

    def perform_browsing(self, url):
        """
        Main browsing method.
        Takes and URL and than downloads the content and starts converting HTML for rendering
        """
        # hack: multi-Line-URLs may contain line breaks from initial HTML-strip-down
        url = url.replace("<br>", "")
        # Set the full url on the text box, e.g. when clicking on links or HTTP-redirects
        self.input.set_text(url)
        # Clear the rendering window
        self.page_content.html_text = str()
        self.page_content.rebuild()
        # If the page is in the cache, we do not download and process it again
        if url.lower() in self.page_cache:
            stripped_html = self.page_cache[url.lower()]
        else:
            try:
                # No cache hit, start the download
                r = requests.get(url, allow_redirects=True)
                r.close()
                if r.status_code == 200:
                    # Sucessful download, start rendering
                    # Improvement: we assume that all pages are UTF-8 encoded. Retrieve encoding instead of guessing UTF-8
                    html_content = r.content.decode('UTF-8')
                    html_content = self.process_string_with_map(html_content, self.REPLACE_MAP_FULL_HTML)
                    stripped_html = html2text.html2text(html_content)
                    stripped_html = self.render_links(stripped_html, self.current_base_url)
                    stripped_html = str(self.process_string_with_map(stripped_html, self.REPLACE_MAP_STRIPPED_HTML))
                else:
                    # HTTP-codes like 404 get an error messages
                    stripped_html = ":-/ There was a problem displaying the page HTTP-STATUS: {}".format(r.status_code)
            except:
                # If something went wrong in the conversion pipeline, we send an error message.
                stripped_html = ":-( Unable to render the page: {}<br>Have you added http:// to the URL?!".format(url)
        # Update the base URL after we successfulle downloaded and processes the page
        self.current_base_url = urljoin(url, '.')
        # Update the history stack
        if self.is_newly_entered_url:
            self.url_history_stack.append(url)
            self.url_history_stack_pointer += 1
            self.is_newly_entered_url = False
        # Send the processed html source code to the pygame.text renderer
        self.page_content.html_text = stripped_html
        self.page_content.rebuild()
        # update cache
        self.page_cache[url.lower()] = stripped_html
        self.x_position = 0
