import os
from os.path import basename
from traceback import print_exception
from urllib.parse import quote, urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from PyQt6.QtCore import QUrl, pyqtSlot
from PyQt6.QtWidgets import QDialog, QFileDialog, QTableWidgetItem

from .ui.task4 import Ui_dl_task4
from .ui.view_source import Ui_dl_view_souce


class ViewSouce(QDialog, Ui_dl_view_souce):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        try:
            r = requests.get(parent.browser.url().toString())
        except Exception as e:
            print_exception(e)
            return

        self.show_source(r.text)
        self.show_header(self.table_request_headers, r.request.headers)
        self.show_header(self.table_response_headers, r.headers)

    def show_source(self, html):
        self.pte_source.setPlainText(html)

    def show_header(self, table, headers):
        table.setRowCount(0)
        for header, value in headers.items():
            pos = table.rowCount()
            table.insertRow(pos)
            table.setItem(pos, 0, QTableWidgetItem(header))
            table.setItem(pos, 1, QTableWidgetItem(value))


class Task4(QDialog, Ui_dl_task4):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.browser.load(QUrl('https://google.com'))

    @pyqtSlot()
    def on_btn_back_clicked(self):
        self.browser.back()

    @pyqtSlot()
    def on_btn_forward_clicked(self):
        self.browser.forward()

    @pyqtSlot()
    def on_btn_reload_clicked(self):
        self.browser.reload()

    @pyqtSlot()
    def on_le_url_returnPressed(self):
        url = self.le_url.text()
        parsed_url = urlparse(url)

        if not parsed_url.scheme or not parsed_url.netloc:
            url = 'https://www.google.com/search?q=' + quote(url)

        self.browser.load(QUrl(url))

    @pyqtSlot(QUrl)
    def on_browser_urlChanged(self, url):
        self.le_url.setText(url.toString())

    @pyqtSlot()
    def on_btn_view_source_clicked(self):
        view_souce_window = ViewSouce(self)
        view_souce_window.exec()

    @pyqtSlot()
    def on_btn_save_page_clicked(self):
        self.browser.page().toHtml(self.save_page_callback)

    def save_page_callback(self, html):
        file_name = basename(urlparse(self.browser.url().toString()).path)
        if not file_name:
            file_name = self.browser.page().title() + '.html'

        path, _ = QFileDialog.getSaveFileName(self, "Save as", file_name, "HTML (*.html)")
        if not path:
            return

        print("Save as", file_name)

        save_folder = os.path.splitext(path)[0] + '_files'
        inner_tags = {'img': 'src', 'link': 'href', 'script': 'src'}

        soup = BeautifulSoup(html, "html.parser")

        for tag, inner in inner_tags.items():
            os.makedirs(save_folder, exist_ok=True)

            for res in soup.findAll(tag):
                if res.has_attr(inner):
                    try:
                        asset_name = os.path.basename(urlparse(res[inner]).path)
                        if not asset_name:
                            continue

                        file_path = os.path.join(save_folder, asset_name)

                        if not os.path.isfile(file_path):
                            print("Downloading", asset_name)
                            r = requests.get(urljoin(self.browser.url().toString(), res[inner]))

                            with open(file_path, 'wb') as f:
                                f.write(r.content)

                        # rename html ref
                        res[inner] = os.path.join(os.path.basename(save_folder), asset_name)
                    except Exception as e:
                        print_exception(e)

        print("Finished downloading")

        with open(path, 'w') as f:
            f.write(soup.prettify())
