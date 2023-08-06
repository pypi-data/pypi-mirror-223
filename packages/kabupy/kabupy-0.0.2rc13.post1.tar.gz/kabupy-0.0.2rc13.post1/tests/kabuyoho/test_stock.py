import kabupy
import pytest
import requests_mock


class TestStock:
    @pytest.mark.parametrize(
        "security_code,price",
        [(3260, 692), (5210, 1192)],
    )
    def test_stock_price(self, helpers, security_code, price):
        text = helpers.html2text(f"/workspaces/kabupy/tests/kabuyoho/html/{security_code}.html")
        with requests_mock.Mocker() as m:
            m.get(f"https://kabuyoho.jp/sp/reportTop?bcode={security_code}", text=text)
            assert kabupy.kabuyoho.stock(security_code).price == price
