from __future__ import annotations
import logging
import re
from bs4 import BeautifulSoup
import requests
from ..exceptions import InvalidElementError


logger = logging.getLogger(__name__)


class Kabuyoho:
    base_url = "https://kabuyoho.jp/"

    def __init__(self) -> None:
        pass

    def stock(self, security_code: str | int) -> Stock:
        return Stock(self, security_code)


class Stock:
    def __init__(self, website: Kabuyoho, security_code: str | int) -> None:
        self.security_code = str(security_code)
        self.website = website

        # self.report_top_page = ReportTopPage(security_code)

    def __set_attributes(self):
        pass

    @property
    def report_top_url(self) -> str:
        return f"https://kabuyoho.jp/sp/reportTop?bcode={self.security_code}"

    @property
    def price(self) -> float | None:
        """Price of the stock

        Returns:
            float | None: Price if found or None
        """
        response = requests.get(self.report_top_url, timeout=10)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        titles = soup.find_all("dt")
        descriptions = soup.find_all("dd")
        titles = [re.sub(r"\s", "", t.text) for t in titles]
        descriptions = [re.sub(r"\s", "", d.text) for d in descriptions]
        if len(titles) != len(descriptions):
            raise InvalidElementError("The number of dd and dt is not same.")
        for title, description in zip(titles, descriptions):
            if "株価" not in title:
                continue
            _price = re.sub(r"[,円]", "", description)
            return float(_price)
        return None
