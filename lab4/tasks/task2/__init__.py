from PyQt6.QtCore import Qt, QUrl, pyqtSlot
from PyQt6.QtWidgets import QDialog

from .ui.task2 import Ui_dl_task2

USER_AGENT = {
    'Chrome 113.0.0 - Windows 10/11':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'Chrome 113.0.0 - OS X 13.4':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'Firefox 113.0 - Windows 10/11':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0',
    'Safari 16.0 - IOS 16.5':
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 EdgiOS/113.1774.50 Mobile/15E148 Safari/605.1.15',
    'Safari 16.4 - OS X 13.4':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15',
    'Chrome Webview 113 - Android 11':
    'Mozilla/5.0 (Linux; Android 11; CPH2351 Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/113.0.5672.131 Mobile Safari/537.36',
}


class Task2(QDialog, Ui_dl_task2):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.init_cb_user_agent()

        self.web_view.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.web_view.load(QUrl('https://google.com'))

        self.connect_signals_slots()

    def connect_signals_slots(self):
        self.btn_view_source.clicked.connect(self.handle_btn_view_source_clicked)

        self.le_url.returnPressed.connect(self.handle_le_url_return_pressed)
        self.cb_user_agent.currentTextChanged.connect(
            self.handle_cb_user_agent_text_changed)

        self.web_view.urlChanged.connect(self.update_le_url)

    def init_cb_user_agent(self):
        for agent in USER_AGENT:
            self.cb_user_agent.addItem(agent)

    def update_le_url(self):
        self.le_url.setText(self.web_view.url().toString())

    def handle_btn_view_source_clicked(self):
        url = self.web_view.url().toString()
        if url.startswith('view-source:'):
            url = url[12:]
        else:
            url = 'view-source:' + url
        self.web_view.load(QUrl(url))

    def handle_le_url_return_pressed(self):
        self.web_view.load(QUrl(self.le_url.text()))

    @pyqtSlot(str)
    def handle_cb_user_agent_text_changed(self, agent):
        self.web_view.page().profile().setHttpUserAgent(USER_AGENT[agent])
