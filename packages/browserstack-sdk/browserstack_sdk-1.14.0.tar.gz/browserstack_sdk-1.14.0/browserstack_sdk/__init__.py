# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack1_opy_ = 2048
bstack11_opy_ = 7
def bstack1ll1_opy_ (bstackl_opy_):
    global bstack1l_opy_
    stringNr = ord (bstackl_opy_ [-1])
    bstack1l1l_opy_ = bstackl_opy_ [:-1]
    bstack1lll_opy_ = stringNr % len (bstack1l1l_opy_)
    bstack1l1_opy_ = bstack1l1l_opy_ [:bstack1lll_opy_] + bstack1l1l_opy_ [bstack1lll_opy_:]
    if bstack111_opy_:
        bstack11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1_opy_ - (bstack1ll_opy_ + stringNr) % bstack11_opy_) for bstack1ll_opy_, char in enumerate (bstack1l1_opy_)])
    else:
        bstack11l_opy_ = str () .join ([chr (ord (char) - bstack1_opy_ - (bstack1ll_opy_ + stringNr) % bstack11_opy_) for bstack1ll_opy_, char in enumerate (bstack1l1_opy_)])
    return eval (bstack11l_opy_)
import atexit
import os
import signal
import sys
import time
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
from multiprocessing import Pool
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
bstack111llllll_opy_ = {
	bstack1ll1_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧࠁ"): bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࠪࠂ"),
  bstack1ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪࠃ"): bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡬ࡧࡼࠫࠄ"),
  bstack1ll1_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬࠅ"): bstack1ll1_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧࠆ"),
  bstack1ll1_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫࠇ"): bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡠࡹ࠶ࡧࠬࠈ"),
  bstack1ll1_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫࠉ"): bstack1ll1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࠨࠊ"),
  bstack1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫࠋ"): bstack1ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࠨࠌ"),
  bstack1ll1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࠍ"): bstack1ll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩࠎ"),
  bstack1ll1_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫࠏ"): bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡥࡣࡷࡪࠫࠐ"),
  bstack1ll1_opy_ (u"ࠧࡤࡱࡱࡷࡴࡲࡥࡍࡱࡪࡷࠬࠑ"): bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡷࡴࡲࡥࠨࠒ"),
  bstack1ll1_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧࠓ"): bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧࠔ"),
  bstack1ll1_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨࠕ"): bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨࠖ"),
  bstack1ll1_opy_ (u"࠭ࡶࡪࡦࡨࡳࠬࠗ"): bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡶࡪࡦࡨࡳࠬ࠘"),
  bstack1ll1_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧ࠙"): bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧࠚ"),
  bstack1ll1_opy_ (u"ࠪࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪࠛ"): bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪࠜ"),
  bstack1ll1_opy_ (u"ࠬ࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪࠝ"): bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪࠞ"),
  bstack1ll1_opy_ (u"ࠧࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩࠟ"): bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩࠠ"),
  bstack1ll1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࠡ"): bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬࠢ"),
  bstack1ll1_opy_ (u"ࠫࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪࠣ"): bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪࠤ"),
  bstack1ll1_opy_ (u"࠭ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫࠥ"): bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫࠦ"),
  bstack1ll1_opy_ (u"ࠨ࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨࠧ"): bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨࠨ"),
  bstack1ll1_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡷࠬࠩ"): bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡴࡤࡌࡧࡼࡷࠬࠪ"),
  bstack1ll1_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧࠫ"): bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧࠬ"),
  bstack1ll1_opy_ (u"ࠧࡩࡱࡶࡸࡸ࠭࠭"): bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡩࡱࡶࡸࡸ࠭࠮"),
  bstack1ll1_opy_ (u"ࠩࡥࡪࡨࡧࡣࡩࡧࠪ࠯"): bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡪࡨࡧࡣࡩࡧࠪ࠰"),
  bstack1ll1_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬ࠱"): bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬ࠲"),
  bstack1ll1_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩ࠳"): bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩ࠴"),
  bstack1ll1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬ࠵"): bstack1ll1_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ࠶"),
  bstack1ll1_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧ࠷"): bstack1ll1_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡡࡰࡳࡧ࡯࡬ࡦࠩ࠸"),
  bstack1ll1_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬ࠹"): bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱ࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭࠺"),
  bstack1ll1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧ࠻"): bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧ࠼"),
  bstack1ll1_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪ࠽"): bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪ࠾"),
  bstack1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ࠿"): bstack1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭ࡀ"),
  bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨࡁ"): bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨࡂ"),
  bstack1ll1_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨࡃ"): bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡲࡹࡷࡩࡥࠨࡄ"),
  bstack1ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࡅ"): bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࡆ"),
  bstack1ll1_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧࡇ"): bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧࡈ"),
}
bstack11lll1111_opy_ = [
  bstack1ll1_opy_ (u"ࠧࡰࡵࠪࡉ"),
  bstack1ll1_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫࡊ"),
  bstack1ll1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࡋ"),
  bstack1ll1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࡌ"),
  bstack1ll1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨࡍ"),
  bstack1ll1_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩࡎ"),
  bstack1ll1_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ࡏ"),
]
bstack1l11_opy_ = {
  bstack1ll1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩࡐ"): [bstack1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩࡑ"), bstack1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡥࡎࡂࡏࡈࠫࡒ")],
  bstack1ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ࡓ"): bstack1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧࡔ"),
  bstack1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨࡕ"): bstack1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡓࡇࡍࡆࠩࡖ"),
  bstack1ll1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬࡗ"): bstack1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊ࠭ࡘ"),
  bstack1ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࡙ࠫ"): bstack1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖ࡚ࠬ"),
  bstack1ll1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰ࡛ࠫ"): bstack1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡇࡒࡂࡎࡏࡉࡑ࡙࡟ࡑࡇࡕࡣࡕࡒࡁࡕࡈࡒࡖࡒ࠭࡜"),
  bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ࡝"): bstack1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࠬ࡞"),
  bstack1ll1_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬ࡟"): bstack1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭ࡠ"),
  bstack1ll1_opy_ (u"ࠪࡥࡵࡶࠧࡡ"): [bstack1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡕࡖ࡟ࡊࡆࠪࡢ"), bstack1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡖࡐࠨࡣ")],
  bstack1ll1_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨࡤ"): bstack1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡏࡃࡕࡈࡖ࡛ࡇࡂࡊࡎࡌࡘ࡞ࡥࡄࡆࡄࡘࡋࠬࡥ"),
  bstack1ll1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬࡦ"): bstack1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬࡧ")
}
bstack1ll11l1ll_opy_ = {
  bstack1ll1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࡨ"): [bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࡠࡰࡤࡱࡪ࠭ࡩ"), bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡳࡐࡤࡱࡪ࠭ࡪ")],
  bstack1ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ࡫"): [bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸࡥ࡫ࡦࡻࠪ࡬"), bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ࡭")],
  bstack1ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ࡮"): bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ࡯"),
  bstack1ll1_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩࡰ"): bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩࡱ"),
  bstack1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࡲ"): bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࡳ"),
  bstack1ll1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨࡴ"): [bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡲࡳࡴࠬࡵ"), bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩࡶ")],
  bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨࡷ"): bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪࡸ"),
  bstack1ll1_opy_ (u"࠭ࡲࡦࡴࡸࡲ࡙࡫ࡳࡵࡵࠪࡹ"): bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡲࡦࡴࡸࡲ࡙࡫ࡳࡵࡵࠪࡺ"),
  bstack1ll1_opy_ (u"ࠨࡣࡳࡴࠬࡻ"): bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴࠬࡼ"),
  bstack1ll1_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬࡽ"): bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴ࡭ࡌࡦࡸࡨࡰࠬࡾ"),
  bstack1ll1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩࡿ"): bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩࢀ")
}
bstack1l111l1ll_opy_ = {
  bstack1ll1_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪࢁ"): bstack1ll1_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬࢂ"),
  bstack1ll1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࢃ"): [bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬࢄ"), bstack1ll1_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧࢅ")],
  bstack1ll1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪࢆ"): bstack1ll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫࢇ"),
  bstack1ll1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ࢈"): bstack1ll1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨࢉ"),
  bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧࢊ"): [bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫࢋ"), bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪࢌ")],
  bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ࢍ"): bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨࢎ"),
  bstack1ll1_opy_ (u"ࠧࡳࡧࡤࡰࡒࡵࡢࡪ࡮ࡨࠫ࢏"): bstack1ll1_opy_ (u"ࠨࡴࡨࡥࡱࡥ࡭ࡰࡤ࡬ࡰࡪ࠭࢐"),
  bstack1ll1_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ࢑"): [bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡴࡵ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪ࢒"), bstack1ll1_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ࢓")],
  bstack1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡎࡴࡳࡦࡥࡸࡶࡪࡉࡥࡳࡶࡶࠫ࢔"): [bstack1ll1_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹ࡙ࡳ࡭ࡅࡨࡶࡹࡹࠧ࢕"), bstack1ll1_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡓࡴ࡮ࡆࡩࡷࡺࠧ࢖")]
}
bstack111ll_opy_ = [
  bstack1ll1_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡊࡰࡶࡩࡨࡻࡲࡦࡅࡨࡶࡹࡹࠧࢗ"),
  bstack1ll1_opy_ (u"ࠩࡳࡥ࡬࡫ࡌࡰࡣࡧࡗࡹࡸࡡࡵࡧࡪࡽࠬ࢘"),
  bstack1ll1_opy_ (u"ࠪࡴࡷࡵࡸࡺ࢙ࠩ"),
  bstack1ll1_opy_ (u"ࠫࡸ࡫ࡴࡘ࡫ࡱࡨࡴࡽࡒࡦࡥࡷ࢚ࠫ"),
  bstack1ll1_opy_ (u"ࠬࡺࡩ࡮ࡧࡲࡹࡹࡹ࢛ࠧ"),
  bstack1ll1_opy_ (u"࠭ࡳࡵࡴ࡬ࡧࡹࡌࡩ࡭ࡧࡌࡲࡹ࡫ࡲࡢࡥࡷࡥࡧ࡯࡬ࡪࡶࡼࠫ࢜"),
  bstack1ll1_opy_ (u"ࠧࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡓࡶࡴࡳࡰࡵࡄࡨ࡬ࡦࡼࡩࡰࡴࠪ࢝"),
  bstack1ll1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭࢞"),
  bstack1ll1_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧ࢟"),
  bstack1ll1_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫࢠ"),
  bstack1ll1_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪࢡ"),
  bstack1ll1_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ࢢ"),
]
bstack1l11ll1ll_opy_ = [
  bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪࢣ"),
  bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢤ"),
  bstack1ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࢥ"),
  bstack1ll1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩࢦ"),
  bstack1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࢧ"),
  bstack1ll1_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ࢨ"),
  bstack1ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨࢩ"),
  bstack1ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪࢪ"),
  bstack1ll1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪࢫ"),
  bstack1ll1_opy_ (u"ࠨࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢬ")
]
bstack1l1l11111_opy_ = [
  bstack1ll1_opy_ (u"ࠩࡸࡴࡱࡵࡡࡥࡏࡨࡨ࡮ࡧࠧࢭ"),
  bstack1ll1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࢮ"),
  bstack1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧࢯ"),
  bstack1ll1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪࢰ"),
  bstack1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡔࡷ࡯࡯ࡳ࡫ࡷࡽࠬࢱ"),
  bstack1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪࢲ"),
  bstack1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡔࡢࡩࠪࢳ"),
  bstack1ll1_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧࢴ"),
  bstack1ll1_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬࢵ"),
  bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩࢶ"),
  bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ࢷ"),
  bstack1ll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬࢸ"),
  bstack1ll1_opy_ (u"ࠧࡰࡵࠪࢹ"),
  bstack1ll1_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫࢺ"),
  bstack1ll1_opy_ (u"ࠩ࡫ࡳࡸࡺࡳࠨࢻ"),
  bstack1ll1_opy_ (u"ࠪࡥࡺࡺ࡯ࡘࡣ࡬ࡸࠬࢼ"),
  bstack1ll1_opy_ (u"ࠫࡷ࡫ࡧࡪࡱࡱࠫࢽ"),
  bstack1ll1_opy_ (u"ࠬࡺࡩ࡮ࡧࡽࡳࡳ࡫ࠧࢾ"),
  bstack1ll1_opy_ (u"࠭࡭ࡢࡥ࡫࡭ࡳ࡫ࠧࢿ"),
  bstack1ll1_opy_ (u"ࠧࡳࡧࡶࡳࡱࡻࡴࡪࡱࡱࠫࣀ"),
  bstack1ll1_opy_ (u"ࠨ࡫ࡧࡰࡪ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ࣁ"),
  bstack1ll1_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡑࡵ࡭ࡪࡴࡴࡢࡶ࡬ࡳࡳ࠭ࣂ"),
  bstack1ll1_opy_ (u"ࠪࡺ࡮ࡪࡥࡰࠩࣃ"),
  bstack1ll1_opy_ (u"ࠫࡳࡵࡐࡢࡩࡨࡐࡴࡧࡤࡕ࡫ࡰࡩࡴࡻࡴࠨࣄ"),
  bstack1ll1_opy_ (u"ࠬࡨࡦࡤࡣࡦ࡬ࡪ࠭ࣅ"),
  bstack1ll1_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬࣆ"),
  bstack1ll1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡓࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫࣇ"),
  bstack1ll1_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡔࡧࡱࡨࡐ࡫ࡹࡴࠩࣈ"),
  bstack1ll1_opy_ (u"ࠩࡵࡩࡦࡲࡍࡰࡤ࡬ࡰࡪ࠭ࣉ"),
  bstack1ll1_opy_ (u"ࠪࡲࡴࡖࡩࡱࡧ࡯࡭ࡳ࡫ࠧ࣊"),
  bstack1ll1_opy_ (u"ࠫࡨ࡮ࡥࡤ࡭ࡘࡖࡑ࠭࣋"),
  bstack1ll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ࣌"),
  bstack1ll1_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡉ࡯ࡰ࡭࡬ࡩࡸ࠭࣍"),
  bstack1ll1_opy_ (u"ࠧࡤࡣࡳࡸࡺࡸࡥࡄࡴࡤࡷ࡭࠭࣎"),
  bstack1ll1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩ࣏ࠬ"),
  bstack1ll1_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯࣐ࠩ"),
  bstack1ll1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡖࡦࡴࡶ࡭ࡴࡴ࣑ࠧ"),
  bstack1ll1_opy_ (u"ࠫࡳࡵࡂ࡭ࡣࡱ࡯ࡕࡵ࡬࡭࡫ࡱ࡫࣒ࠬ"),
  bstack1ll1_opy_ (u"ࠬࡳࡡࡴ࡭ࡖࡩࡳࡪࡋࡦࡻࡶ࣓ࠫ"),
  bstack1ll1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡒ࡯ࡨࡵࠪࣔ"),
  bstack1ll1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡉࡥࠩࣕ"),
  bstack1ll1_opy_ (u"ࠨࡦࡨࡨ࡮ࡩࡡࡵࡧࡧࡈࡪࡼࡩࡤࡧࠪࣖ"),
  bstack1ll1_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡒࡤࡶࡦࡳࡳࠨࣗ"),
  bstack1ll1_opy_ (u"ࠪࡴ࡭ࡵ࡮ࡦࡐࡸࡱࡧ࡫ࡲࠨࣘ"),
  bstack1ll1_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࠩࣙ"),
  bstack1ll1_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࡒࡴࡹ࡯࡯࡯ࡵࠪࣚ"),
  bstack1ll1_opy_ (u"࠭ࡣࡰࡰࡶࡳࡱ࡫ࡌࡰࡩࡶࠫࣛ"),
  bstack1ll1_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧࣜ"),
  bstack1ll1_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡍࡱࡪࡷࠬࣝ"),
  bstack1ll1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡄ࡬ࡳࡲ࡫ࡴࡳ࡫ࡦࠫࣞ"),
  bstack1ll1_opy_ (u"ࠪࡺ࡮ࡪࡥࡰࡘ࠵ࠫࣟ"),
  bstack1ll1_opy_ (u"ࠫࡲ࡯ࡤࡔࡧࡶࡷ࡮ࡵ࡮ࡊࡰࡶࡸࡦࡲ࡬ࡂࡲࡳࡷࠬ࣠"),
  bstack1ll1_opy_ (u"ࠬ࡫ࡳࡱࡴࡨࡷࡸࡵࡓࡦࡴࡹࡩࡷ࠭࣡"),
  bstack1ll1_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡍࡱࡪࡷࠬ࣢"),
  bstack1ll1_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡅࡧࡴࣣࠬ"),
  bstack1ll1_opy_ (u"ࠨࡶࡨࡰࡪࡳࡥࡵࡴࡼࡐࡴ࡭ࡳࠨࣤ"),
  bstack1ll1_opy_ (u"ࠩࡶࡽࡳࡩࡔࡪ࡯ࡨ࡛࡮ࡺࡨࡏࡖࡓࠫࣥ"),
  bstack1ll1_opy_ (u"ࠪ࡫ࡪࡵࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨࣦ"),
  bstack1ll1_opy_ (u"ࠫ࡬ࡶࡳࡍࡱࡦࡥࡹ࡯࡯࡯ࠩࣧ"),
  bstack1ll1_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡖࡲࡰࡨ࡬ࡰࡪ࠭ࣨ"),
  bstack1ll1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡔࡥࡵࡹࡲࡶࡰࣩ࠭"),
  bstack1ll1_opy_ (u"ࠧࡧࡱࡵࡧࡪࡉࡨࡢࡰࡪࡩࡏࡧࡲࠨ࣪"),
  bstack1ll1_opy_ (u"ࠨࡺࡰࡷࡏࡧࡲࠨ࣫"),
  bstack1ll1_opy_ (u"ࠩࡻࡱࡽࡐࡡࡳࠩ࣬"),
  bstack1ll1_opy_ (u"ࠪࡱࡦࡹ࡫ࡄࡱࡰࡱࡦࡴࡤࡴ࣭ࠩ"),
  bstack1ll1_opy_ (u"ࠫࡲࡧࡳ࡬ࡄࡤࡷ࡮ࡩࡁࡶࡶ࡫࣮ࠫ"),
  bstack1ll1_opy_ (u"ࠬࡽࡳࡍࡱࡦࡥࡱ࡙ࡵࡱࡲࡲࡶࡹ࣯࠭"),
  bstack1ll1_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࣰࠩ"),
  bstack1ll1_opy_ (u"ࠧࡢࡲࡳ࡚ࡪࡸࡳࡪࡱࡱࣱࠫ"),
  bstack1ll1_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡊࡰࡶࡩࡨࡻࡲࡦࡅࡨࡶࡹࡹࣲࠧ"),
  bstack1ll1_opy_ (u"ࠩࡵࡩࡸ࡯ࡧ࡯ࡃࡳࡴࠬࣳ"),
  bstack1ll1_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡳ࡯࡭ࡢࡶ࡬ࡳࡳࡹࠧࣴ"),
  bstack1ll1_opy_ (u"ࠫࡨࡧ࡮ࡢࡴࡼࠫࣵ"),
  bstack1ll1_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽࣶ࠭"),
  bstack1ll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ࣷ"),
  bstack1ll1_opy_ (u"ࠧࡪࡧࠪࣸ"),
  bstack1ll1_opy_ (u"ࠨࡧࡧ࡫ࡪࣹ࠭"),
  bstack1ll1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࣺࠩ"),
  bstack1ll1_opy_ (u"ࠪࡵࡺ࡫ࡵࡦࠩࣻ"),
  bstack1ll1_opy_ (u"ࠫ࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ࣼ"),
  bstack1ll1_opy_ (u"ࠬࡧࡰࡱࡕࡷࡳࡷ࡫ࡃࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳ࠭ࣽ"),
  bstack1ll1_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡉࡡ࡮ࡧࡵࡥࡎࡳࡡࡨࡧࡌࡲ࡯࡫ࡣࡵ࡫ࡲࡲࠬࣾ"),
  bstack1ll1_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࡊࡾࡣ࡭ࡷࡧࡩࡍࡵࡳࡵࡵࠪࣿ"),
  bstack1ll1_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸࡏ࡮ࡤ࡮ࡸࡨࡪࡎ࡯ࡴࡶࡶࠫऀ"),
  bstack1ll1_opy_ (u"ࠩࡸࡴࡩࡧࡴࡦࡃࡳࡴࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭ँ"),
  bstack1ll1_opy_ (u"ࠪࡶࡪࡹࡥࡳࡸࡨࡈࡪࡼࡩࡤࡧࠪं"),
  bstack1ll1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫः"),
  bstack1ll1_opy_ (u"ࠬࡹࡥ࡯ࡦࡎࡩࡾࡹࠧऄ"),
  bstack1ll1_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡖࡡࡴࡵࡦࡳࡩ࡫ࠧअ"),
  bstack1ll1_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡉࡰࡵࡇࡩࡻ࡯ࡣࡦࡕࡨࡸࡹ࡯࡮ࡨࡵࠪआ"),
  bstack1ll1_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡂࡷࡧ࡭ࡴࡏ࡮࡫ࡧࡦࡸ࡮ࡵ࡮ࠨइ"),
  bstack1ll1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡃࡳࡴࡱ࡫ࡐࡢࡻࠪई"),
  bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫउ"),
  bstack1ll1_opy_ (u"ࠫࡼࡪࡩࡰࡕࡨࡶࡻ࡯ࡣࡦࠩऊ"),
  bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧऋ"),
  bstack1ll1_opy_ (u"࠭ࡰࡳࡧࡹࡩࡳࡺࡃࡳࡱࡶࡷࡘ࡯ࡴࡦࡖࡵࡥࡨࡱࡩ࡯ࡩࠪऌ"),
  bstack1ll1_opy_ (u"ࠧࡩ࡫ࡪ࡬ࡈࡵ࡮ࡵࡴࡤࡷࡹ࠭ऍ"),
  bstack1ll1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡑࡴࡨࡪࡪࡸࡥ࡯ࡥࡨࡷࠬऎ"),
  bstack1ll1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡕ࡬ࡱࠬए"),
  bstack1ll1_opy_ (u"ࠪࡷ࡮ࡳࡏࡱࡶ࡬ࡳࡳࡹࠧऐ"),
  bstack1ll1_opy_ (u"ࠫࡷ࡫࡭ࡰࡸࡨࡍࡔ࡙ࡁࡱࡲࡖࡩࡹࡺࡩ࡯ࡩࡶࡐࡴࡩࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠩऑ"),
  bstack1ll1_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧऒ"),
  bstack1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨओ"),
  bstack1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩऔ"),
  bstack1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧक"),
  bstack1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫख"),
  bstack1ll1_opy_ (u"ࠪࡴࡦ࡭ࡥࡍࡱࡤࡨࡘࡺࡲࡢࡶࡨ࡫ࡾ࠭ग"),
  bstack1ll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪघ"),
  bstack1ll1_opy_ (u"ࠬࡺࡩ࡮ࡧࡲࡹࡹࡹࠧङ"),
  bstack1ll1_opy_ (u"࠭ࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࡒࡵࡳࡲࡶࡴࡃࡧ࡫ࡥࡻ࡯࡯ࡳࠩच")
]
bstack1ll1l1l11_opy_ = {
  bstack1ll1_opy_ (u"ࠧࡷࠩछ"): bstack1ll1_opy_ (u"ࠨࡸࠪज"),
  bstack1ll1_opy_ (u"ࠩࡩࠫझ"): bstack1ll1_opy_ (u"ࠪࡪࠬञ"),
  bstack1ll1_opy_ (u"ࠫ࡫ࡵࡲࡤࡧࠪट"): bstack1ll1_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࠫठ"),
  bstack1ll1_opy_ (u"࠭࡯࡯࡮ࡼࡥࡺࡺ࡯࡮ࡣࡷࡩࠬड"): bstack1ll1_opy_ (u"ࠧࡰࡰ࡯ࡽࡆࡻࡴࡰ࡯ࡤࡸࡪ࠭ढ"),
  bstack1ll1_opy_ (u"ࠨࡨࡲࡶࡨ࡫࡬ࡰࡥࡤࡰࠬण"): bstack1ll1_opy_ (u"ࠩࡩࡳࡷࡩࡥ࡭ࡱࡦࡥࡱ࠭त"),
  bstack1ll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡪࡲࡷࡹ࠭थ"): bstack1ll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡋࡳࡸࡺࠧद"),
  bstack1ll1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡴࡴࡸࡴࠨध"): bstack1ll1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩन"),
  bstack1ll1_opy_ (u"ࠧࡱࡴࡲࡼࡾࡻࡳࡦࡴࠪऩ"): bstack1ll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡕࡴࡧࡵࠫप"),
  bstack1ll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬफ"): bstack1ll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭ब"),
  bstack1ll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡩࡱࡶࡸࠬभ"): bstack1ll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡊࡲࡷࡹ࠭म"),
  bstack1ll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡳࡳࡷࡺࠧय"): bstack1ll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡔࡴࡸࡴࠨर"),
  bstack1ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡺࡹࡥࡳࠩऱ"): bstack1ll1_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡕࡴࡧࡵࠫल"),
  bstack1ll1_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡶࡵࡨࡶࠬळ"): bstack1ll1_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡗࡶࡩࡷ࠭ऴ"),
  bstack1ll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡲࡤࡷࡸ࠭व"): bstack1ll1_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡔࡦࡹࡳࠨश"),
  bstack1ll1_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡵࡧࡳࡴࠩष"): bstack1ll1_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾࡖࡡࡴࡵࠪस"),
  bstack1ll1_opy_ (u"ࠩࡥ࡭ࡳࡧࡲࡺࡲࡤࡸ࡭࠭ह"): bstack1ll1_opy_ (u"ࠪࡦ࡮ࡴࡡࡳࡻࡳࡥࡹ࡮ࠧऺ"),
  bstack1ll1_opy_ (u"ࠫࡵࡧࡣࡧ࡫࡯ࡩࠬऻ"): bstack1ll1_opy_ (u"ࠬ࠳ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨ़"),
  bstack1ll1_opy_ (u"࠭ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨऽ"): bstack1ll1_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪा"),
  bstack1ll1_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫि"): bstack1ll1_opy_ (u"ࠩ࠰ࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬी"),
  bstack1ll1_opy_ (u"ࠪࡰࡴ࡭ࡦࡪ࡮ࡨࠫु"): bstack1ll1_opy_ (u"ࠫࡱࡵࡧࡧ࡫࡯ࡩࠬू"),
  bstack1ll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧृ"): bstack1ll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨॄ"),
}
bstack1ll1l_opy_ = bstack1ll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡪࡸࡦ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡹࡧ࠳࡭ࡻࡢࠨॅ")
bstack11ll1lll1_opy_ = bstack1ll1_opy_ (u"ࠨࡪࡷࡸࡵࡀ࠯࠰ࡪࡸࡦ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠫॆ")
bstack1l111l11l_opy_ = bstack1ll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲࡬ࡺࡨ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡲࡪࡾࡴࡠࡪࡸࡦࡸ࠭े")
bstack1ll1lll1l_opy_ = {
  bstack1ll1_opy_ (u"ࠪࡧࡷ࡯ࡴࡪࡥࡤࡰࠬै"): 50,
  bstack1ll1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪॉ"): 40,
  bstack1ll1_opy_ (u"ࠬࡽࡡࡳࡰ࡬ࡲ࡬࠭ॊ"): 30,
  bstack1ll1_opy_ (u"࠭ࡩ࡯ࡨࡲࠫो"): 20,
  bstack1ll1_opy_ (u"ࠧࡥࡧࡥࡹ࡬࠭ौ"): 10
}
bstack11llll1_opy_ = bstack1ll1lll1l_opy_[bstack1ll1_opy_ (u"ࠨ࡫ࡱࡪࡴ्࠭")]
bstack1l11111_opy_ = bstack1ll1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨॎ")
bstack11l11ll1_opy_ = bstack1ll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨॏ")
bstack1l1lll11_opy_ = bstack1ll1_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࠪॐ")
bstack111l_opy_ = bstack1ll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࠫ॑")
bstack1ll11l1l1_opy_ = [bstack1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡑࡅࡒࡋ॒ࠧ"), bstack1ll1_opy_ (u"࡚ࠧࡑࡘࡖࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧ॓")]
bstack11lll111l_opy_ = [bstack1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫ॔"), bstack1ll1_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫॕ")]
bstack1lll1ll1l_opy_ = [
  bstack1ll1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡎࡢ࡯ࡨࠫॖ"),
  bstack1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ॗ"),
  bstack1ll1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩक़"),
  bstack1ll1_opy_ (u"࠭࡮ࡦࡹࡆࡳࡲࡳࡡ࡯ࡦࡗ࡭ࡲ࡫࡯ࡶࡶࠪख़"),
  bstack1ll1_opy_ (u"ࠧࡢࡲࡳࠫग़"),
  bstack1ll1_opy_ (u"ࠨࡷࡧ࡭ࡩ࠭ज़"),
  bstack1ll1_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫड़"),
  bstack1ll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡧࠪढ़"),
  bstack1ll1_opy_ (u"ࠫࡴࡸࡩࡦࡰࡷࡥࡹ࡯࡯࡯ࠩफ़"),
  bstack1ll1_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡩࡧࡼࡩࡦࡹࠪय़"),
  bstack1ll1_opy_ (u"࠭࡮ࡰࡔࡨࡷࡪࡺࠧॠ"), bstack1ll1_opy_ (u"ࠧࡧࡷ࡯ࡰࡗ࡫ࡳࡦࡶࠪॡ"),
  bstack1ll1_opy_ (u"ࠨࡥ࡯ࡩࡦࡸࡓࡺࡵࡷࡩࡲࡌࡩ࡭ࡧࡶࠫॢ"),
  bstack1ll1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡕ࡫ࡰ࡭ࡳ࡭ࡳࠨॣ"),
  bstack1ll1_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡓࡩࡷ࡬࡯ࡳ࡯ࡤࡲࡨ࡫ࡌࡰࡩࡪ࡭ࡳ࡭ࠧ।"),
  bstack1ll1_opy_ (u"ࠫࡴࡺࡨࡦࡴࡄࡴࡵࡹࠧ॥"),
  bstack1ll1_opy_ (u"ࠬࡶࡲࡪࡰࡷࡔࡦ࡭ࡥࡔࡱࡸࡶࡨ࡫ࡏ࡯ࡈ࡬ࡲࡩࡌࡡࡪ࡮ࡸࡶࡪ࠭०"),
  bstack1ll1_opy_ (u"࠭ࡡࡱࡲࡄࡧࡹ࡯ࡶࡪࡶࡼࠫ१"), bstack1ll1_opy_ (u"ࠧࡢࡲࡳࡔࡦࡩ࡫ࡢࡩࡨࠫ२"), bstack1ll1_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡃࡦࡸ࡮ࡼࡩࡵࡻࠪ३"), bstack1ll1_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡓࡥࡨࡱࡡࡨࡧࠪ४"), bstack1ll1_opy_ (u"ࠪࡥࡵࡶࡗࡢ࡫ࡷࡈࡺࡸࡡࡵ࡫ࡲࡲࠬ५"),
  bstack1ll1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡖࡪࡧࡤࡺࡖ࡬ࡱࡪࡵࡵࡵࠩ६"),
  bstack1ll1_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡘࡪࡹࡴࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠩ७"),
  bstack1ll1_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡃࡰࡸࡨࡶࡦ࡭ࡥࠨ८"), bstack1ll1_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡄࡱࡹࡩࡷࡧࡧࡦࡇࡱࡨࡎࡴࡴࡦࡰࡷࠫ९"),
  bstack1ll1_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡆࡨࡺ࡮ࡩࡥࡓࡧࡤࡨࡾ࡚ࡩ࡮ࡧࡲࡹࡹ࠭॰"),
  bstack1ll1_opy_ (u"ࠩࡤࡨࡧࡖ࡯ࡳࡶࠪॱ"),
  bstack1ll1_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡈࡪࡼࡩࡤࡧࡖࡳࡨࡱࡥࡵࠩॲ"),
  bstack1ll1_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡎࡴࡳࡵࡣ࡯ࡰ࡙࡯࡭ࡦࡱࡸࡸࠬॳ"),
  bstack1ll1_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡏ࡮ࡴࡶࡤࡰࡱࡖࡡࡵࡪࠪॴ"),
  bstack1ll1_opy_ (u"࠭ࡡࡷࡦࠪॵ"), bstack1ll1_opy_ (u"ࠧࡢࡸࡧࡐࡦࡻ࡮ࡤࡪࡗ࡭ࡲ࡫࡯ࡶࡶࠪॶ"), bstack1ll1_opy_ (u"ࠨࡣࡹࡨࡗ࡫ࡡࡥࡻࡗ࡭ࡲ࡫࡯ࡶࡶࠪॷ"), bstack1ll1_opy_ (u"ࠩࡤࡺࡩࡇࡲࡨࡵࠪॸ"),
  bstack1ll1_opy_ (u"ࠪࡹࡸ࡫ࡋࡦࡻࡶࡸࡴࡸࡥࠨॹ"), bstack1ll1_opy_ (u"ࠫࡰ࡫ࡹࡴࡶࡲࡶࡪࡖࡡࡵࡪࠪॺ"), bstack1ll1_opy_ (u"ࠬࡱࡥࡺࡵࡷࡳࡷ࡫ࡐࡢࡵࡶࡻࡴࡸࡤࠨॻ"),
  bstack1ll1_opy_ (u"࠭࡫ࡦࡻࡄࡰ࡮ࡧࡳࠨॼ"), bstack1ll1_opy_ (u"ࠧ࡬ࡧࡼࡔࡦࡹࡳࡸࡱࡵࡨࠬॽ"),
  bstack1ll1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡅࡹࡧࡦࡹࡹࡧࡢ࡭ࡧࠪॾ"), bstack1ll1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡂࡴࡪࡷࠬॿ"), bstack1ll1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡇࡻࡩࡨࡻࡴࡢࡤ࡯ࡩࡉ࡯ࡲࠨঀ"), bstack1ll1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡆ࡬ࡷࡵ࡭ࡦࡏࡤࡴࡵ࡯࡮ࡨࡈ࡬ࡰࡪ࠭ঁ"), bstack1ll1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵ࡙ࡸ࡫ࡓࡺࡵࡷࡩࡲࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࠩং"),
  bstack1ll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡕࡵࡲࡵࠩঃ"), bstack1ll1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡖ࡯ࡳࡶࡶࠫ঄"),
  bstack1ll1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡄࡪࡵࡤࡦࡱ࡫ࡂࡶ࡫࡯ࡨࡈ࡮ࡥࡤ࡭ࠪঅ"),
  bstack1ll1_opy_ (u"ࠩࡤࡹࡹࡵࡗࡦࡤࡹ࡭ࡪࡽࡔࡪ࡯ࡨࡳࡺࡺࠧআ"),
  bstack1ll1_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡄࡧࡹ࡯࡯࡯ࠩই"), bstack1ll1_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡇࡦࡺࡥࡨࡱࡵࡽࠬঈ"), bstack1ll1_opy_ (u"ࠬ࡯࡮ࡵࡧࡱࡸࡋࡲࡡࡨࡵࠪউ"), bstack1ll1_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡧ࡬ࡊࡰࡷࡩࡳࡺࡁࡳࡩࡸࡱࡪࡴࡴࡴࠩঊ"),
  bstack1ll1_opy_ (u"ࠧࡥࡱࡱࡸࡘࡺ࡯ࡱࡃࡳࡴࡔࡴࡒࡦࡵࡨࡸࠬঋ"),
  bstack1ll1_opy_ (u"ࠨࡷࡱ࡭ࡨࡵࡤࡦࡍࡨࡽࡧࡵࡡࡳࡦࠪঌ"), bstack1ll1_opy_ (u"ࠩࡵࡩࡸ࡫ࡴࡌࡧࡼࡦࡴࡧࡲࡥࠩ঍"),
  bstack1ll1_opy_ (u"ࠪࡲࡴ࡙ࡩࡨࡰࠪ঎"),
  bstack1ll1_opy_ (u"ࠫ࡮࡭࡮ࡰࡴࡨ࡙ࡳ࡯࡭ࡱࡱࡵࡸࡦࡴࡴࡗ࡫ࡨࡻࡸ࠭এ"),
  bstack1ll1_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇ࡮ࡥࡴࡲ࡭ࡩ࡝ࡡࡵࡥ࡫ࡩࡷࡹࠧঐ"),
  bstack1ll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭঑"),
  bstack1ll1_opy_ (u"ࠧࡳࡧࡦࡶࡪࡧࡴࡦࡅ࡫ࡶࡴࡳࡥࡅࡴ࡬ࡺࡪࡸࡓࡦࡵࡶ࡭ࡴࡴࡳࠨ঒"),
  bstack1ll1_opy_ (u"ࠨࡰࡤࡸ࡮ࡼࡥࡘࡧࡥࡗࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧও"),
  bstack1ll1_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡖࡡࡵࡪࠪঔ"),
  bstack1ll1_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡗࡵ࡫ࡥࡥࠩক"),
  bstack1ll1_opy_ (u"ࠫ࡬ࡶࡳࡆࡰࡤࡦࡱ࡫ࡤࠨখ"),
  bstack1ll1_opy_ (u"ࠬ࡯ࡳࡉࡧࡤࡨࡱ࡫ࡳࡴࠩগ"),
  bstack1ll1_opy_ (u"࠭ࡡࡥࡤࡈࡼࡪࡩࡔࡪ࡯ࡨࡳࡺࡺࠧঘ"),
  bstack1ll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࡫ࡓࡤࡴ࡬ࡴࡹ࠭ঙ"),
  bstack1ll1_opy_ (u"ࠨࡵ࡮࡭ࡵࡊࡥࡷ࡫ࡦࡩࡎࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡡࡵ࡫ࡲࡲࠬচ"),
  bstack1ll1_opy_ (u"ࠩࡤࡹࡹࡵࡇࡳࡣࡱࡸࡕ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮ࡴࠩছ"),
  bstack1ll1_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡒࡦࡺࡵࡳࡣ࡯ࡓࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨজ"),
  bstack1ll1_opy_ (u"ࠫࡸࡿࡳࡵࡧࡰࡔࡴࡸࡴࠨঝ"),
  bstack1ll1_opy_ (u"ࠬࡸࡥ࡮ࡱࡷࡩࡆࡪࡢࡉࡱࡶࡸࠬঞ"),
  bstack1ll1_opy_ (u"࠭ࡳ࡬࡫ࡳ࡙ࡳࡲ࡯ࡤ࡭ࠪট"), bstack1ll1_opy_ (u"ࠧࡶࡰ࡯ࡳࡨࡱࡔࡺࡲࡨࠫঠ"), bstack1ll1_opy_ (u"ࠨࡷࡱࡰࡴࡩ࡫ࡌࡧࡼࠫড"),
  bstack1ll1_opy_ (u"ࠩࡤࡹࡹࡵࡌࡢࡷࡱࡧ࡭࠭ঢ"),
  bstack1ll1_opy_ (u"ࠪࡷࡰ࡯ࡰࡍࡱࡪࡧࡦࡺࡃࡢࡲࡷࡹࡷ࡫ࠧণ"),
  bstack1ll1_opy_ (u"ࠫࡺࡴࡩ࡯ࡵࡷࡥࡱࡲࡏࡵࡪࡨࡶࡕࡧࡣ࡬ࡣࡪࡩࡸ࠭ত"),
  bstack1ll1_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪ࡝ࡩ࡯ࡦࡲࡻࡆࡴࡩ࡮ࡣࡷ࡭ࡴࡴࠧথ"),
  bstack1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨ࡙ࡵ࡯࡭ࡵ࡙ࡩࡷࡹࡩࡰࡰࠪদ"),
  bstack1ll1_opy_ (u"ࠧࡦࡰࡩࡳࡷࡩࡥࡂࡲࡳࡍࡳࡹࡴࡢ࡮࡯ࠫধ"),
  bstack1ll1_opy_ (u"ࠨࡧࡱࡷࡺࡸࡥࡘࡧࡥࡺ࡮࡫ࡷࡴࡊࡤࡺࡪࡖࡡࡨࡧࡶࠫন"), bstack1ll1_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࡇࡩࡻࡺ࡯ࡰ࡮ࡶࡔࡴࡸࡴࠨ঩"), bstack1ll1_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧ࡚ࡩࡧࡼࡩࡦࡹࡇࡩࡹࡧࡩ࡭ࡵࡆࡳࡱࡲࡥࡤࡶ࡬ࡳࡳ࠭প"),
  bstack1ll1_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡅࡵࡶࡳࡄࡣࡦ࡬ࡪࡒࡩ࡮࡫ࡷࠫফ"),
  bstack1ll1_opy_ (u"ࠬࡩࡡ࡭ࡧࡱࡨࡦࡸࡆࡰࡴࡰࡥࡹ࠭ব"),
  bstack1ll1_opy_ (u"࠭ࡢࡶࡰࡧࡰࡪࡏࡤࠨভ"),
  bstack1ll1_opy_ (u"ࠧ࡭ࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧম"),
  bstack1ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࡖࡩࡷࡼࡩࡤࡧࡶࡉࡳࡧࡢ࡭ࡧࡧࠫয"), bstack1ll1_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࡗࡪࡸࡶࡪࡥࡨࡷࡆࡻࡴࡩࡱࡵ࡭ࡿ࡫ࡤࠨর"),
  bstack1ll1_opy_ (u"ࠪࡥࡺࡺ࡯ࡂࡥࡦࡩࡵࡺࡁ࡭ࡧࡵࡸࡸ࠭঱"), bstack1ll1_opy_ (u"ࠫࡦࡻࡴࡰࡆ࡬ࡷࡲ࡯ࡳࡴࡃ࡯ࡩࡷࡺࡳࠨল"),
  bstack1ll1_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩࡎࡴࡳࡵࡴࡸࡱࡪࡴࡴࡴࡎ࡬ࡦࠬ঳"),
  bstack1ll1_opy_ (u"࠭࡮ࡢࡶ࡬ࡺࡪ࡝ࡥࡣࡖࡤࡴࠬ঴"),
  bstack1ll1_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡉ࡯࡫ࡷ࡭ࡦࡲࡕࡳ࡮ࠪ঵"), bstack1ll1_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡂ࡮࡯ࡳࡼࡖ࡯ࡱࡷࡳࡷࠬশ"), bstack1ll1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡋࡪࡲࡴࡸࡥࡇࡴࡤࡹࡩ࡝ࡡࡳࡰ࡬ࡲ࡬࠭ষ"), bstack1ll1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࡒࡴࡪࡴࡌࡪࡰ࡮ࡷࡎࡴࡂࡢࡥ࡮࡫ࡷࡵࡵ࡯ࡦࠪস"),
  bstack1ll1_opy_ (u"ࠫࡰ࡫ࡥࡱࡍࡨࡽࡈ࡮ࡡࡪࡰࡶࠫহ"),
  bstack1ll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯࡭ࡿࡧࡢ࡭ࡧࡖࡸࡷ࡯࡮ࡨࡵࡇ࡭ࡷ࠭঺"),
  bstack1ll1_opy_ (u"࠭ࡰࡳࡱࡦࡩࡸࡹࡁࡳࡩࡸࡱࡪࡴࡴࡴࠩ঻"),
  bstack1ll1_opy_ (u"ࠧࡪࡰࡷࡩࡷࡑࡥࡺࡆࡨࡰࡦࡿ়ࠧ"),
  bstack1ll1_opy_ (u"ࠨࡵ࡫ࡳࡼࡏࡏࡔࡎࡲ࡫ࠬঽ"),
  bstack1ll1_opy_ (u"ࠩࡶࡩࡳࡪࡋࡦࡻࡖࡸࡷࡧࡴࡦࡩࡼࠫা"),
  bstack1ll1_opy_ (u"ࠪࡻࡪࡨ࡫ࡪࡶࡕࡩࡸࡶ࡯࡯ࡵࡨࡘ࡮ࡳࡥࡰࡷࡷࠫি"), bstack1ll1_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡘࡣ࡬ࡸ࡙࡯࡭ࡦࡱࡸࡸࠬী"),
  bstack1ll1_opy_ (u"ࠬࡸࡥ࡮ࡱࡷࡩࡉ࡫ࡢࡶࡩࡓࡶࡴࡾࡹࠨু"),
  bstack1ll1_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡇࡳࡺࡰࡦࡉࡽ࡫ࡣࡶࡶࡨࡊࡷࡵ࡭ࡉࡶࡷࡴࡸ࠭ূ"),
  bstack1ll1_opy_ (u"ࠧࡴ࡭࡬ࡴࡑࡵࡧࡄࡣࡳࡸࡺࡸࡥࠨৃ"),
  bstack1ll1_opy_ (u"ࠨࡹࡨࡦࡰ࡯ࡴࡅࡧࡥࡹ࡬ࡖࡲࡰࡺࡼࡔࡴࡸࡴࠨৄ"),
  bstack1ll1_opy_ (u"ࠩࡩࡹࡱࡲࡃࡰࡰࡷࡩࡽࡺࡌࡪࡵࡷࠫ৅"),
  bstack1ll1_opy_ (u"ࠪࡻࡦ࡯ࡴࡇࡱࡵࡅࡵࡶࡓࡤࡴ࡬ࡴࡹ࠭৆"),
  bstack1ll1_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࡈࡵ࡮࡯ࡧࡦࡸࡗ࡫ࡴࡳ࡫ࡨࡷࠬে"),
  bstack1ll1_opy_ (u"ࠬࡧࡰࡱࡐࡤࡱࡪ࠭ৈ"),
  bstack1ll1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡓࡍࡅࡨࡶࡹ࠭৉"),
  bstack1ll1_opy_ (u"ࠧࡵࡣࡳ࡛࡮ࡺࡨࡔࡪࡲࡶࡹࡖࡲࡦࡵࡶࡈࡺࡸࡡࡵ࡫ࡲࡲࠬ৊"),
  bstack1ll1_opy_ (u"ࠨࡵࡦࡥࡱ࡫ࡆࡢࡥࡷࡳࡷ࠭ো"),
  bstack1ll1_opy_ (u"ࠩࡺࡨࡦࡒ࡯ࡤࡣ࡯ࡔࡴࡸࡴࠨৌ"),
  bstack1ll1_opy_ (u"ࠪࡷ࡭ࡵࡷ࡙ࡥࡲࡨࡪࡒ࡯ࡨ্ࠩ"),
  bstack1ll1_opy_ (u"ࠫ࡮ࡵࡳࡊࡰࡶࡸࡦࡲ࡬ࡑࡣࡸࡷࡪ࠭ৎ"),
  bstack1ll1_opy_ (u"ࠬࡾࡣࡰࡦࡨࡇࡴࡴࡦࡪࡩࡉ࡭ࡱ࡫ࠧ৏"),
  bstack1ll1_opy_ (u"࠭࡫ࡦࡻࡦ࡬ࡦ࡯࡮ࡑࡣࡶࡷࡼࡵࡲࡥࠩ৐"),
  bstack1ll1_opy_ (u"ࠧࡶࡵࡨࡔࡷ࡫ࡢࡶ࡫࡯ࡸ࡜ࡊࡁࠨ৑"),
  bstack1ll1_opy_ (u"ࠨࡲࡵࡩࡻ࡫࡮ࡵ࡙ࡇࡅࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠩ৒"),
  bstack1ll1_opy_ (u"ࠩࡺࡩࡧࡊࡲࡪࡸࡨࡶࡆ࡭ࡥ࡯ࡶࡘࡶࡱ࠭৓"),
  bstack1ll1_opy_ (u"ࠪ࡯ࡪࡿࡣࡩࡣ࡬ࡲࡕࡧࡴࡩࠩ৔"),
  bstack1ll1_opy_ (u"ࠫࡺࡹࡥࡏࡧࡺ࡛ࡉࡇࠧ৕"),
  bstack1ll1_opy_ (u"ࠬࡽࡤࡢࡎࡤࡹࡳࡩࡨࡕ࡫ࡰࡩࡴࡻࡴࠨ৖"), bstack1ll1_opy_ (u"࠭ࡷࡥࡣࡆࡳࡳࡴࡥࡤࡶ࡬ࡳࡳ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ৗ"),
  bstack1ll1_opy_ (u"ࠧࡹࡥࡲࡨࡪࡕࡲࡨࡋࡧࠫ৘"), bstack1ll1_opy_ (u"ࠨࡺࡦࡳࡩ࡫ࡓࡪࡩࡱ࡭ࡳ࡭ࡉࡥࠩ৙"),
  bstack1ll1_opy_ (u"ࠩࡸࡴࡩࡧࡴࡦࡦ࡚ࡈࡆࡈࡵ࡯ࡦ࡯ࡩࡎࡪࠧ৚"),
  bstack1ll1_opy_ (u"ࠪࡶࡪࡹࡥࡵࡑࡱࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡲࡵࡑࡱࡰࡾ࠭৛"),
  bstack1ll1_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨ࡙࡯࡭ࡦࡱࡸࡸࡸ࠭ড়"),
  bstack1ll1_opy_ (u"ࠬࡽࡤࡢࡕࡷࡥࡷࡺࡵࡱࡔࡨࡸࡷ࡯ࡥࡴࠩঢ়"), bstack1ll1_opy_ (u"࠭ࡷࡥࡣࡖࡸࡦࡸࡴࡶࡲࡕࡩࡹࡸࡹࡊࡰࡷࡩࡷࡼࡡ࡭ࠩ৞"),
  bstack1ll1_opy_ (u"ࠧࡤࡱࡱࡲࡪࡩࡴࡉࡣࡵࡨࡼࡧࡲࡦࡍࡨࡽࡧࡵࡡࡳࡦࠪয়"),
  bstack1ll1_opy_ (u"ࠨ࡯ࡤࡼ࡙ࡿࡰࡪࡰࡪࡊࡷ࡫ࡱࡶࡧࡱࡧࡾ࠭ৠ"),
  bstack1ll1_opy_ (u"ࠩࡶ࡭ࡲࡶ࡬ࡦࡋࡶ࡚࡮ࡹࡩࡣ࡮ࡨࡇ࡭࡫ࡣ࡬ࠩৡ"),
  bstack1ll1_opy_ (u"ࠪࡹࡸ࡫ࡃࡢࡴࡷ࡬ࡦ࡭ࡥࡔࡵ࡯ࠫৢ"),
  bstack1ll1_opy_ (u"ࠫࡸ࡮࡯ࡶ࡮ࡧ࡙ࡸ࡫ࡓࡪࡰࡪࡰࡪࡺ࡯࡯ࡖࡨࡷࡹࡓࡡ࡯ࡣࡪࡩࡷ࠭ৣ"),
  bstack1ll1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡍ࡜ࡊࡐࠨ৤"),
  bstack1ll1_opy_ (u"࠭ࡡ࡭࡮ࡲࡻ࡙ࡵࡵࡤࡪࡌࡨࡊࡴࡲࡰ࡮࡯ࠫ৥"),
  bstack1ll1_opy_ (u"ࠧࡪࡩࡱࡳࡷ࡫ࡈࡪࡦࡧࡩࡳࡇࡰࡪࡒࡲࡰ࡮ࡩࡹࡆࡴࡵࡳࡷ࠭০"),
  bstack1ll1_opy_ (u"ࠨ࡯ࡲࡧࡰࡒ࡯ࡤࡣࡷ࡭ࡴࡴࡁࡱࡲࠪ১"),
  bstack1ll1_opy_ (u"ࠩ࡯ࡳ࡬ࡩࡡࡵࡈࡲࡶࡲࡧࡴࠨ২"), bstack1ll1_opy_ (u"ࠪࡰࡴ࡭ࡣࡢࡶࡉ࡭ࡱࡺࡥࡳࡕࡳࡩࡨࡹࠧ৩"),
  bstack1ll1_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡇࡩࡱࡧࡹࡂࡦࡥࠫ৪")
]
bstack1111l1_opy_ = bstack1ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠰ࡧࡱࡵࡵࡥ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡺࡶ࡬ࡰࡣࡧࠫ৫")
bstack1l1111ll1_opy_ = [bstack1ll1_opy_ (u"࠭࠮ࡢࡲ࡮ࠫ৬"), bstack1ll1_opy_ (u"ࠧ࠯ࡣࡤࡦࠬ৭"), bstack1ll1_opy_ (u"ࠨ࠰࡬ࡴࡦ࠭৮")]
bstack1l1l11l11_opy_ = [bstack1ll1_opy_ (u"ࠩ࡬ࡨࠬ৯"), bstack1ll1_opy_ (u"ࠪࡴࡦࡺࡨࠨৰ"), bstack1ll1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧৱ"), bstack1ll1_opy_ (u"ࠬࡹࡨࡢࡴࡨࡥࡧࡲࡥࡠ࡫ࡧࠫ৲")]
bstack1l1l1111l_opy_ = {
  bstack1ll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭৳"): bstack1ll1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ৴"),
  bstack1ll1_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩ৵"): bstack1ll1_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧ৶"),
  bstack1ll1_opy_ (u"ࠪࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ৷"): bstack1ll1_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬ৸"),
  bstack1ll1_opy_ (u"ࠬ࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ৹"): bstack1ll1_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬ৺"),
  bstack1ll1_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡏࡱࡶ࡬ࡳࡳࡹࠧ৻"): bstack1ll1_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩৼ")
}
bstack11l1l111l_opy_ = [
  bstack1ll1_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ৽"),
  bstack1ll1_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨ৾"),
  bstack1ll1_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬ৿"),
  bstack1ll1_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫ਀"),
  bstack1ll1_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧਁ"),
]
bstack1111ll11_opy_ = bstack1l11ll1ll_opy_ + bstack1l1l11111_opy_ + bstack1lll1ll1l_opy_
bstack111lll1_opy_ = [
  bstack1ll1_opy_ (u"ࠧ࡟࡮ࡲࡧࡦࡲࡨࡰࡵࡷࠨࠬਂ"),
  bstack1ll1_opy_ (u"ࠨࡠࡥࡷ࠲ࡲ࡯ࡤࡣ࡯࠲ࡨࡵ࡭ࠥࠩਃ"),
  bstack1ll1_opy_ (u"ࠩࡡ࠵࠷࠽࠮ࠨ਄"),
  bstack1ll1_opy_ (u"ࠪࡢ࠶࠶࠮ࠨਅ"),
  bstack1ll1_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠴࡟࠻࠳࠹࡞࠰ࠪਆ"),
  bstack1ll1_opy_ (u"ࠬࡤ࠱࠸࠴࠱࠶ࡠ࠶࠭࠺࡟࠱ࠫਇ"),
  bstack1ll1_opy_ (u"࠭࡞࠲࠹࠵࠲࠸ࡡ࠰࠮࠳ࡠ࠲ࠬਈ"),
  bstack1ll1_opy_ (u"ࠧ࡟࠳࠼࠶࠳࠷࠶࠹࠰ࠪਉ")
]
bstack1llll11_opy_ = bstack1ll1_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡾࢁࠬਊ")
bstack11l1ll111_opy_ = bstack1ll1_opy_ (u"ࠩࡶࡨࡰ࠵ࡶ࠲࠱ࡨࡺࡪࡴࡴࠨ਋")
bstack1ll1l11l1_opy_ = [ bstack1ll1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ਌") ]
bstack1llll1l11_opy_ = [ bstack1ll1_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪ਍") ]
bstack11111l1_opy_ = [ bstack1ll1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ਎") ]
bstack1llll1l1_opy_ = bstack1ll1_opy_ (u"࠭ࡓࡅࡍࡖࡩࡹࡻࡰࠨਏ")
bstack1lll11l1_opy_ = bstack1ll1_opy_ (u"ࠧࡔࡆࡎࡘࡪࡹࡴࡂࡶࡷࡩࡲࡶࡴࡦࡦࠪਐ")
bstack11ll1ll1l_opy_ = bstack1ll1_opy_ (u"ࠨࡕࡇࡏ࡙࡫ࡳࡵࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠬ਑")
bstack1l11ll1l_opy_ = bstack1ll1_opy_ (u"ࠩ࠷࠲࠵࠴࠰ࠨ਒")
bstack11ll1l1_opy_ = [
  bstack1ll1_opy_ (u"ࠪࡉࡗࡘ࡟ࡇࡃࡌࡐࡊࡊࠧਓ"),
  bstack1ll1_opy_ (u"ࠫࡊࡘࡒࡠࡖࡌࡑࡊࡊ࡟ࡐࡗࡗࠫਔ"),
  bstack1ll1_opy_ (u"ࠬࡋࡒࡓࡡࡅࡐࡔࡉࡋࡆࡆࡢࡆ࡞ࡥࡃࡍࡋࡈࡒ࡙࠭ਕ"),
  bstack1ll1_opy_ (u"࠭ࡅࡓࡔࡢࡒࡊ࡚ࡗࡐࡔࡎࡣࡈࡎࡁࡏࡉࡈࡈࠬਖ"),
  bstack1ll1_opy_ (u"ࠧࡆࡔࡕࡣࡘࡕࡃࡌࡇࡗࡣࡓࡕࡔࡠࡅࡒࡒࡓࡋࡃࡕࡇࡇࠫਗ"),
  bstack1ll1_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡆࡐࡔ࡙ࡅࡅࠩਘ"),
  bstack1ll1_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡖࡊ࡙ࡅࡕࠩਙ"),
  bstack1ll1_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡗࡋࡆࡖࡕࡈࡈࠬਚ"),
  bstack1ll1_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡇࡂࡐࡔࡗࡉࡉ࠭ਛ"),
  bstack1ll1_opy_ (u"ࠬࡋࡒࡓࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭ਜ"),
  bstack1ll1_opy_ (u"࠭ࡅࡓࡔࡢࡒࡆࡓࡅࡠࡐࡒࡘࡤࡘࡅࡔࡑࡏ࡚ࡊࡊࠧਝ"),
  bstack1ll1_opy_ (u"ࠧࡆࡔࡕࡣࡆࡊࡄࡓࡇࡖࡗࡤࡏࡎࡗࡃࡏࡍࡉ࠭ਞ"),
  bstack1ll1_opy_ (u"ࠨࡇࡕࡖࡤࡇࡄࡅࡔࡈࡗࡘࡥࡕࡏࡔࡈࡅࡈࡎࡁࡃࡎࡈࠫਟ"),
  bstack1ll1_opy_ (u"ࠩࡈࡖࡗࡥࡔࡖࡐࡑࡉࡑࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪਠ"),
  bstack1ll1_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣ࡙ࡏࡍࡆࡆࡢࡓ࡚࡚ࠧਡ"),
  bstack1ll1_opy_ (u"ࠫࡊࡘࡒࡠࡕࡒࡇࡐ࡙࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡋࡇࡉࡍࡇࡇࠫਢ"),
  bstack1ll1_opy_ (u"ࠬࡋࡒࡓࡡࡖࡓࡈࡑࡓࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡎࡏࡔࡖࡢ࡙ࡓࡘࡅࡂࡅࡋࡅࡇࡒࡅࠨਣ"),
  bstack1ll1_opy_ (u"࠭ࡅࡓࡔࡢࡔࡗࡕࡘ࡚ࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭ਤ"),
  bstack1ll1_opy_ (u"ࠧࡆࡔࡕࡣࡓࡇࡍࡆࡡࡑࡓ࡙ࡥࡒࡆࡕࡒࡐ࡛ࡋࡄࠨਥ"),
  bstack1ll1_opy_ (u"ࠨࡇࡕࡖࡤࡔࡁࡎࡇࡢࡖࡊ࡙ࡏࡍࡗࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧਦ"),
  bstack1ll1_opy_ (u"ࠩࡈࡖࡗࡥࡍࡂࡐࡇࡅ࡙ࡕࡒ࡚ࡡࡓࡖࡔ࡞࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠࡈࡄࡍࡑࡋࡄࠨਧ"),
]
bstack11ll_opy_ = bstack1ll1_opy_ (u"ࠪ࠲࠴ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡦࡸࡴࡪࡨࡤࡧࡹࡹ࠯ࠨਨ")
def bstack1l1l11ll_opy_():
  global CONFIG
  headers = {
        bstack1ll1_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪ਩"): bstack1ll1_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨਪ"),
      }
  proxies = bstack1lll11l11_opy_(CONFIG, bstack1l111l11l_opy_)
  try:
    response = requests.get(bstack1l111l11l_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack111l11l1_opy_ = response.json()[bstack1ll1_opy_ (u"࠭ࡨࡶࡤࡶࠫਫ")]
      logger.debug(bstack11l111l_opy_.format(response.json()))
      return bstack111l11l1_opy_
    else:
      logger.debug(bstack11l111l11_opy_.format(bstack1ll1_opy_ (u"ࠢࡓࡧࡶࡴࡴࡴࡳࡦࠢࡍࡗࡔࡔࠠࡱࡣࡵࡷࡪࠦࡥࡳࡴࡲࡶࠥࠨਬ")))
  except Exception as e:
    logger.debug(bstack11l111l11_opy_.format(e))
def bstack11lll1l1_opy_(hub_url):
  global CONFIG
  url = bstack1ll1_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥਭ")+  hub_url + bstack1ll1_opy_ (u"ࠤ࠲ࡧ࡭࡫ࡣ࡬ࠤਮ")
  headers = {
        bstack1ll1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩਯ"): bstack1ll1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧਰ"),
      }
  proxies = bstack1lll11l11_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack11l1l11_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1l11l1l11_opy_.format(hub_url, e))
def bstack11l1ll11l_opy_():
  try:
    global bstack11l11lll1_opy_
    bstack111l11l1_opy_ = bstack1l1l11ll_opy_()
    bstack1l11l1ll1_opy_ = []
    results = []
    for bstack1llll111l_opy_ in bstack111l11l1_opy_:
      bstack1l11l1ll1_opy_.append(bstack11l1lll1_opy_(target=bstack11lll1l1_opy_,args=(bstack1llll111l_opy_,)))
    for t in bstack1l11l1ll1_opy_:
      t.start()
    for t in bstack1l11l1ll1_opy_:
      results.append(t.join())
    bstack111l1ll1_opy_ = {}
    for item in results:
      hub_url = item[bstack1ll1_opy_ (u"ࠬ࡮ࡵࡣࡡࡸࡶࡱ࠭਱")]
      latency = item[bstack1ll1_opy_ (u"࠭࡬ࡢࡶࡨࡲࡨࡿࠧਲ")]
      bstack111l1ll1_opy_[hub_url] = latency
    bstack1111111l_opy_ = min(bstack111l1ll1_opy_, key= lambda x: bstack111l1ll1_opy_[x])
    bstack11l11lll1_opy_ = bstack1111111l_opy_
    logger.debug(bstack1l1111111_opy_.format(bstack1111111l_opy_))
  except Exception as e:
    logger.debug(bstack1l11l1_opy_.format(e))
bstack111111ll_opy_ = bstack1ll1_opy_ (u"ࠧࡔࡧࡷࡸ࡮ࡴࡧࠡࡷࡳࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠬࠡࡷࡶ࡭ࡳ࡭ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࠽ࠤࢀࢃࠧਲ਼")
bstack11lll1lll_opy_ = bstack1ll1_opy_ (u"ࠨࡅࡲࡱࡵࡲࡥࡵࡧࡧࠤࡸ࡫ࡴࡶࡲࠤࠫ਴")
bstack1l11ll11l_opy_ = bstack1ll1_opy_ (u"ࠩࡓࡥࡷࡹࡥࡥࠢࡦࡳࡳ࡬ࡩࡨࠢࡩ࡭ࡱ࡫࠺ࠡࡽࢀࠫਵ")
bstack1ll111lll_opy_ = bstack1ll1_opy_ (u"ࠪࡗࡦࡴࡩࡵ࡫ࡽࡩࡩࠦࡣࡰࡰࡩ࡭࡬ࠦࡦࡪ࡮ࡨ࠾ࠥࢁࡽࠨਸ਼")
bstack111ll11_opy_ = bstack1ll1_opy_ (u"࡚ࠫࡹࡩ࡯ࡩࠣ࡬ࡺࡨࠠࡶࡴ࡯࠾ࠥࢁࡽࠨ਷")
bstack1lll11l1l_opy_ = bstack1ll1_opy_ (u"࡙ࠬࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡵࡸࡪࡪࠠࡸ࡫ࡷ࡬ࠥ࡯ࡤ࠻ࠢࡾࢁࠬਸ")
bstack11llllll1_opy_ = bstack1ll1_opy_ (u"࠭ࡒࡦࡥࡨ࡭ࡻ࡫ࡤࠡ࡫ࡱࡸࡪࡸࡲࡶࡲࡷ࠰ࠥ࡫ࡸࡪࡶ࡬ࡲ࡬࠭ਹ")
bstack1l111111_opy_ = bstack1ll1_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡵࡨࡰࡪࡴࡩࡶ࡯ࠣࡸࡴࠦࡲࡶࡰࠣࡸࡪࡹࡴࡴ࠰ࠣࡤࡵ࡯ࡰࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡶࡩࡱ࡫࡮ࡪࡷࡰࡤࠬ਺")
bstack11l1l111_opy_ = bstack1ll1_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵࠢࡤࡲࡩࠦࡰࡺࡶࡨࡷࡹ࠳ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠡࡲࡤࡧࡰࡧࡧࡦࡵ࠱ࠤࡥࡶࡩࡱࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶࠣࡴࡾࡺࡥࡴࡶ࠰ࡷࡪࡲࡥ࡯࡫ࡸࡱࡥ࠭਻")
bstack1ll1ll1_opy_ = bstack1ll1_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡶࡴࡨ࡯ࡵ࠮ࠣࡴࡦࡨ࡯ࡵࠢࡤࡲࡩࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࡭࡫ࡥࡶࡦࡸࡹࠡࡲࡤࡧࡰࡧࡧࡦࡵࠣࡸࡴࠦࡲࡶࡰࠣࡶࡴࡨ࡯ࡵࠢࡷࡩࡸࡺࡳࠡ࡫ࡱࠤࡵࡧࡲࡢ࡮࡯ࡩࡱ࠴ࠠࡡࡲ࡬ࡴࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡲࡰࡤࡲࡸ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡳࡱࡥࡳࡹ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠮ࡲࡤࡦࡴࡺࠠࡳࡱࡥࡳࡹ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠮ࡵࡨࡰࡪࡴࡩࡶ࡯࡯࡭ࡧࡸࡡࡳࡻࡣ਼ࠫ")
bstack1l11l11ll_opy_ = bstack1ll1_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡧ࡫ࡨࡢࡸࡨࠤࡹࡵࠠࡳࡷࡱࠤࡹ࡫ࡳࡵࡵ࠱ࠤࡥࡶࡩࡱࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡦࡪ࡮ࡡࡷࡧࡣࠫ਽")
bstack1l1lll11l_opy_ = bstack1ll1_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡧࡰࡱ࡫ࡸࡱ࠲ࡩ࡬ࡪࡧࡱࡸࠥࡺ࡯ࠡࡴࡸࡲࠥࡺࡥࡴࡶࡶ࠲ࠥࡦࡰࡪࡲࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡆࡶࡰࡪࡷࡰ࠱ࡕࡿࡴࡩࡱࡱ࠱ࡈࡲࡩࡦࡰࡷࡤࠬਾ")
bstack11ll11_opy_ = bstack1ll1_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡸࡴࠦࡲࡶࡰࠣࡸࡪࡹࡴࡴ࠰ࠣࡤࡵ࡯ࡰࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡦࠧਿ")
bstack1llll11ll_opy_ = bstack1ll1_opy_ (u"࠭ࡃࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡩ࡭ࡳࡪࠠࡦ࡫ࡷ࡬ࡪࡸࠠࡔࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡲࡶࠥࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳ࠯ࠢࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡹࡧ࡬࡭ࠢࡷ࡬ࡪࠦࡲࡦ࡮ࡨࡺࡦࡴࡴࠡࡲࡤࡧࡰࡧࡧࡦࡵࠣࡹࡸ࡯࡮ࡨࠢࡳ࡭ࡵࠦࡴࡰࠢࡵࡹࡳࠦࡴࡦࡵࡷࡷ࠳࠭ੀ")
bstack1l1ll111_opy_ = bstack1ll1_opy_ (u"ࠧࡉࡣࡱࡨࡱ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡧࡱࡵࡳࡦࠩੁ")
bstack1l1l1ll1l_opy_ = bstack1ll1_opy_ (u"ࠨࡃ࡯ࡰࠥࡪ࡯࡯ࡧࠤࠫੂ")
bstack1l1lllll_opy_ = bstack1ll1_opy_ (u"ࠩࡆࡳࡳ࡬ࡩࡨࠢࡩ࡭ࡱ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴࠡࡣࡷࠤࡦࡴࡹࠡࡲࡤࡶࡪࡴࡴࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡴ࡬ࠠࠣࡽࢀࠦ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡥ࡯ࡹࡩ࡫ࠠࡢࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰ࠴ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡧ࡭࡭ࠢࡩ࡭ࡱ࡫ࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤ࡫ࡵࡲࠡࡶࡨࡷࡹࡹ࠮ࠨ੃")
bstack1ll11l_opy_ = bstack1ll1_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡦࡶࡪࡪࡥ࡯ࡶ࡬ࡥࡱࡹࠠ࡯ࡱࡷࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩ࠴ࠠࡑ࡮ࡨࡥࡸ࡫ࠠࡢࡦࡧࠤࡹ࡮ࡥ࡮ࠢ࡬ࡲࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠡࡥࡲࡲ࡫࡯ࡧࠡࡨ࡬ࡰࡪࠦࡡࡴࠢࠥࡹࡸ࡫ࡲࡏࡣࡰࡩࠧࠦࡡ࡯ࡦࠣࠦࡦࡩࡣࡦࡵࡶࡏࡪࡿࠢࠡࡱࡵࠤࡸ࡫ࡴࠡࡶ࡫ࡩࡲࠦࡡࡴࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࡵ࠽ࠤࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊࠨࠠࡢࡰࡧࠤࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠣࠩ੄")
bstack1l111lll_opy_ = bstack1ll1_opy_ (u"ࠫࡒࡧ࡬ࡧࡱࡵࡱࡪࡪࠠࡤࡱࡱࡪ࡮࡭ࠠࡧ࡫࡯ࡩ࠿ࠨࡻࡾࠤࠪ੅")
bstack1llllll_opy_ = bstack1ll1_opy_ (u"ࠬࡋ࡮ࡤࡱࡸࡲࡹ࡫ࡲࡦࡦࠣࡩࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡸࡴࠥ࠳ࠠࡼࡿࠪ੆")
bstack11ll11l1_opy_ = bstack1ll1_opy_ (u"࠭ࡓࡵࡣࡵࡸ࡮ࡴࡧࠡࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡍࡱࡦࡥࡱ࠭ੇ")
bstack1ll111l1l_opy_ = bstack1ll1_opy_ (u"ࠧࡔࡶࡲࡴࡵ࡯࡮ࡨࠢࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡎࡲࡧࡦࡲࠧੈ")
bstack111l1_opy_ = bstack1ll1_opy_ (u"ࠨࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡍࡱࡦࡥࡱࠦࡩࡴࠢࡱࡳࡼࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠡࠨ੉")
bstack11l111111_opy_ = bstack1ll1_opy_ (u"ࠩࡆࡳࡺࡲࡤࠡࡰࡲࡸࠥࡹࡴࡢࡴࡷࠤࡇࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡐࡴࡩࡡ࡭࠼ࠣࡿࢂ࠭੊")
bstack1l11ll1_opy_ = bstack1ll1_opy_ (u"ࠪࡗࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡲ࡯ࡤࡣ࡯ࠤࡧ࡯࡮ࡢࡴࡼࠤࡼ࡯ࡴࡩࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࢀࢃࠧੋ")
bstack1l1ll1ll_opy_ = bstack1ll1_opy_ (u"࡚ࠫࡶࡤࡢࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡥࡧࡷࡥ࡮ࡲࡳ࠻ࠢࡾࢁࠬੌ")
bstack1l11111l_opy_ = bstack1ll1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡷࡳࡨࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡵࡷࡥࡹࡻࡳࠡࡽࢀ੍ࠫ")
bstack11l11l11_opy_ = bstack1ll1_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡰࡳࡱࡹ࡭ࡩ࡫ࠠࡢࡰࠣࡥࡵࡶࡲࡰࡲࡵ࡭ࡦࡺࡥࠡࡈ࡚ࠤ࠭ࡸ࡯ࡣࡱࡷ࠳ࡵࡧࡢࡰࡶࠬࠤ࡮ࡴࠠࡤࡱࡱࡪ࡮࡭ࠠࡧ࡫࡯ࡩ࠱ࠦࡳ࡬࡫ࡳࠤࡹ࡮ࡥࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡰ࡫ࡹࠡ࡫ࡱࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡮࡬ࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡵ࡬ࡱࡵࡲࡥࠡࡲࡼࡸ࡭ࡵ࡮ࠡࡵࡦࡶ࡮ࡶࡴࠡࡹ࡬ࡸ࡭ࡵࡵࡵࠢࡤࡲࡾࠦࡆࡘ࠰ࠪ੎")
bstack11l11111l_opy_ = bstack1ll1_opy_ (u"ࠧࡔࡧࡷࡸ࡮ࡴࡧࠡࡪࡷࡸࡵࡖࡲࡰࡺࡼ࠳࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠡ࡫ࡶࠤࡳࡵࡴࠡࡵࡸࡴࡵࡵࡲࡵࡧࡧࠤࡴࡴࠠࡤࡷࡵࡶࡪࡴࡴ࡭ࡻࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡰࡨࠣࡷࡪࡲࡥ࡯࡫ࡸࡱࠥ࠮ࡻࡾࠫ࠯ࠤࡵࡲࡥࡢࡵࡨࠤࡺࡶࡧࡳࡣࡧࡩࠥࡺ࡯ࠡࡕࡨࡰࡪࡴࡩࡶ࡯ࡁࡁ࠹࠴࠰࠯࠲ࠣࡳࡷࠦࡲࡦࡨࡨࡶࠥࡺ࡯ࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡺࡻࡼ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡧࡳࡨࡹ࠯ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡶࡩࡱ࡫࡮ࡪࡷࡰ࠳ࡷࡻ࡮࠮ࡶࡨࡷࡹࡹ࠭ࡣࡧ࡫࡭ࡳࡪ࠭ࡱࡴࡲࡼࡾࠩࡰࡺࡶ࡫ࡳࡳࠦࡦࡰࡴࠣࡥࠥࡽ࡯ࡳ࡭ࡤࡶࡴࡻ࡮ࡥ࠰ࠪ੏")
bstack1l1ll11l1_opy_ = bstack1ll1_opy_ (u"ࠨࡉࡨࡲࡪࡸࡡࡵ࡫ࡱ࡫ࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡾࡳ࡬ࠡࡨ࡬ࡰࡪ࠴࠮ࠨ੐")
bstack11lllll11_opy_ = bstack1ll1_opy_ (u"ࠩࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡩࡨࡲࡪࡸࡡࡵࡧࡧࠤࡹ࡮ࡥࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡨ࡬ࡰࡪࠧࠧੑ")
bstack1ll11l11l_opy_ = bstack1ll1_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡶ࡫ࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤ࡫࡯࡬ࡦ࠰ࠣࡿࢂ࠭੒")
bstack1lll111_opy_ = bstack1ll1_opy_ (u"ࠫࡊࡾࡰࡦࡥࡷࡩࡩࠦࡡࡵࠢ࡯ࡩࡦࡹࡴࠡ࠳ࠣ࡭ࡳࡶࡵࡵ࠮ࠣࡶࡪࡩࡥࡪࡸࡨࡨࠥ࠶ࠧ੓")
bstack1ll11_opy_ = bstack1ll1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡩࡻࡲࡪࡰࡪࠤࡆࡶࡰࠡࡷࡳࡰࡴࡧࡤ࠯ࠢࡾࢁࠬ੔")
bstack1l11111l1_opy_ = bstack1ll1_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡸࡴࡱࡵࡡࡥࠢࡄࡴࡵ࠴ࠠࡊࡰࡹࡥࡱ࡯ࡤࠡࡨ࡬ࡰࡪࠦࡰࡢࡶ࡫ࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩࠦࡻࡾ࠰ࠪ੕")
bstack11ll1_opy_ = bstack1ll1_opy_ (u"ࠧࡌࡧࡼࡷࠥࡩࡡ࡯ࡰࡲࡸࠥࡩ࡯࠮ࡧࡻ࡭ࡸࡺࠠࡢࡵࠣࡥࡵࡶࠠࡷࡣ࡯ࡹࡪࡹࠬࠡࡷࡶࡩࠥࡧ࡮ࡺࠢࡲࡲࡪࠦࡰࡳࡱࡳࡩࡷࡺࡹࠡࡨࡵࡳࡲࠦࡻࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡶࡡࡵࡪ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡩࡵࡴࡶࡲࡱࡤ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡷ࡭ࡧࡲࡦࡣࡥࡰࡪࡥࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀࢀ࠰ࠥࡵ࡮࡭ࡻࠣࠦࡵࡧࡴࡩࠤࠣࡥࡳࡪࠠࠣࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠦࠥࡩࡡ࡯ࠢࡦࡳ࠲࡫ࡸࡪࡵࡷࠤࡹࡵࡧࡦࡶ࡫ࡩࡷ࠴ࠧ੖")
bstack1l1ll1_opy_ = bstack1ll1_opy_ (u"ࠨ࡝ࡌࡲࡻࡧ࡬ࡪࡦࠣࡥࡵࡶࠠࡱࡴࡲࡴࡪࡸࡴࡺ࡟ࠣࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠣࡥࡷ࡫ࠠࡼ࡫ࡧࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡰࡢࡶ࡫ࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡣࡶࡵࡷࡳࡲࡥࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁࢁ࠳ࠦࡆࡰࡴࠣࡱࡴࡸࡥࠡࡦࡨࡸࡦ࡯࡬ࡴࠢࡳࡰࡪࡧࡳࡦࠢࡹ࡭ࡸ࡯ࡴࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡺࡻࡼ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡧࡳࡨࡹ࠯ࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡡࡱࡲ࡬ࡹࡲ࠵ࡳࡦࡶ࠰ࡹࡵ࠳ࡴࡦࡵࡷࡷ࠴ࡹࡰࡦࡥ࡬ࡪࡾ࠳ࡡࡱࡲࠪ੗")
bstack11l11ll11_opy_ = bstack1ll1_opy_ (u"ࠩ࡞ࡍࡳࡼࡡ࡭࡫ࡧࠤࡦࡶࡰࠡࡲࡵࡳࡵ࡫ࡲࡵࡻࡠࠤࡘࡻࡰࡱࡱࡵࡸࡪࡪࠠࡷࡣ࡯ࡹࡪࡹࠠࡰࡨࠣࡥࡵࡶࠠࡢࡴࡨࠤࡴ࡬ࠠࡼ࡫ࡧࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡰࡢࡶ࡫ࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡣࡶࡵࡷࡳࡲࡥࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁࢁ࠳ࠦࡆࡰࡴࠣࡱࡴࡸࡥࠡࡦࡨࡸࡦ࡯࡬ࡴࠢࡳࡰࡪࡧࡳࡦࠢࡹ࡭ࡸ࡯ࡴࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡺࡻࡼ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡧࡳࡨࡹ࠯ࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡡࡱࡲ࡬ࡹࡲ࠵ࡳࡦࡶ࠰ࡹࡵ࠳ࡴࡦࡵࡷࡷ࠴ࡹࡰࡦࡥ࡬ࡪࡾ࠳ࡡࡱࡲࠪ੘")
bstack111lll1l_opy_ = bstack1ll1_opy_ (u"࡙ࠪࡸ࡯࡮ࡨࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡦࡶࡰࠡ࡫ࡧࠤࢀࢃࠠࡧࡱࡵࠤ࡭ࡧࡳࡩࠢ࠽ࠤࢀࢃ࠮ࠨਖ਼")
bstack111ll1ll1_opy_ = bstack1ll1_opy_ (u"ࠫࡆࡶࡰࠡࡗࡳࡰࡴࡧࡤࡦࡦࠣࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺ࠰ࠣࡍࡉࠦ࠺ࠡࡽࢀࠫਗ਼")
bstack1ll1ll11_opy_ = bstack1ll1_opy_ (u"࡛ࠬࡳࡪࡰࡪࠤࡆࡶࡰࠡ࠼ࠣࡿࢂ࠴ࠧਜ਼")
bstack1l11l111l_opy_ = bstack1ll1_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲࠦࡩࡴࠢࡱࡳࡹࠦࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡩࡳࡷࠦࡶࡢࡰ࡬ࡰࡱࡧࠠࡱࡻࡷ࡬ࡴࡴࠠࡵࡧࡶࡸࡸ࠲ࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡹ࡬ࡸ࡭ࠦࡰࡢࡴࡤࡰࡱ࡫࡬ࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠥࡃࠠ࠲ࠩੜ")
bstack1l1lll1_opy_ = bstack1ll1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࡀࠠࡼࡿࠪ੝")
bstack11l111_opy_ = bstack1ll1_opy_ (u"ࠨࡅࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡨࡲ࡯ࡴࡧࠣࡦࡷࡵࡷࡴࡧࡵ࠾ࠥࢁࡽࠨਫ਼")
bstack111111l_opy_ = bstack1ll1_opy_ (u"ࠩࡆࡳࡺࡲࡤࠡࡰࡲࡸࠥ࡭ࡥࡵࠢࡵࡩࡦࡹ࡯࡯ࠢࡩࡳࡷࠦࡢࡦࡪࡤࡺࡪࠦࡦࡦࡣࡷࡹࡷ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥ࠯ࠢࡾࢁࠬ੟")
bstack11ll11ll_opy_ = bstack1ll1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠤ࡫ࡸ࡯࡮ࠢࡤࡴ࡮ࠦࡣࡢ࡮࡯࠲ࠥࡋࡲࡳࡱࡵ࠾ࠥࢁࡽࠨ੠")
bstack1lll11lll_opy_ = bstack1ll1_opy_ (u"࡚ࠫࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡪࡲࡻࠥࡨࡵࡪ࡮ࡧࠤ࡚ࡘࡌ࠭ࠢࡤࡷࠥࡨࡵࡪ࡮ࡧࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠡ࡫ࡶࠤࡳࡵࡴࠡࡷࡶࡩࡩ࠴ࠧ੡")
bstack1ll1l1lll_opy_ = bstack1ll1_opy_ (u"࡙ࠬࡥࡳࡸࡨࡶࠥࡹࡩࡥࡧࠣࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠮ࡻࡾࠫࠣ࡭ࡸࠦ࡮ࡰࡶࠣࡷࡦࡳࡥࠡࡣࡶࠤࡨࡲࡩࡦࡰࡷࠤࡸ࡯ࡤࡦࠢࡥࡹ࡮ࡲࡤࡏࡣࡰࡩ࠭ࢁࡽࠪࠩ੢")
bstack1l11l11l_opy_ = bstack1ll1_opy_ (u"࠭ࡖࡪࡧࡺࠤࡧࡻࡩ࡭ࡦࠣࡳࡳࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡪࡡࡴࡪࡥࡳࡦࡸࡤ࠻ࠢࡾࢁࠬ੣")
bstack11llll1l1_opy_ = bstack1ll1_opy_ (u"ࠧࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡥࡨࡩࡥࡴࡵࠣࡥࠥࡶࡲࡪࡸࡤࡸࡪࠦࡤࡰ࡯ࡤ࡭ࡳࡀࠠࡼࡿࠣ࠲࡙ࠥࡥࡵࠢࡷ࡬ࡪࠦࡦࡰ࡮࡯ࡳࡼ࡯࡮ࡨࠢࡦࡳࡳ࡬ࡩࡨࠢ࡬ࡲࠥࡿ࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱࠦࡦࡪ࡮ࡨ࠾ࠥࡢ࡮࠮࠯࠰࠱࠲࠳࠭࠮࠯࠰࠱ࠥࡢ࡮ࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰ࠿ࠦࡴࡳࡷࡨࠤࡡࡴ࠭࠮࠯࠰࠱࠲࠳࠭࠮࠯࠰ࠫ੤")
bstack1l1l1111_opy_ = bstack1ll1_opy_ (u"ࠨࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡦࡺࡨࡧࡺࡺࡩ࡯ࡩࠣ࡫ࡪࡺ࡟࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࡤ࡫ࡲࡳࡱࡵࠤ࠿ࠦࡻࡾࠩ੥")
bstack1111111_opy_ = bstack1ll1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫࡮ࡥࡡࡤࡱࡵࡲࡩࡵࡷࡧࡩࡤ࡫ࡶࡦࡰࡷࠤ࡫ࡵࡲࠡࡕࡇࡏࡘ࡫ࡴࡶࡲࠣࡿࢂࠨ੦")
bstack11111lll_opy_ = bstack1ll1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥ࡯ࡦࡢࡥࡲࡶ࡬ࡪࡶࡸࡨࡪࡥࡥࡷࡧࡱࡸࠥ࡬࡯ࡳࠢࡖࡈࡐ࡚ࡥࡴࡶࡄࡸࡹ࡫࡭ࡱࡶࡨࡨࠥࢁࡽࠣ੧")
bstack1l111llll_opy_ = bstack1ll1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡰࡧࡣࡦࡳࡰ࡭࡫ࡷࡹࡩ࡫࡟ࡦࡸࡨࡲࡹࠦࡦࡰࡴࠣࡗࡉࡑࡔࡦࡵࡷࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲࠠࡼࡿࠥ੨")
bstack1l1l111_opy_ = bstack1ll1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧ࡫ࡵࡩࡤࡸࡥࡲࡷࡨࡷࡹࠦࡻࡾࠤ੩")
bstack111ll1l11_opy_ = bstack1ll1_opy_ (u"ࠨࡐࡐࡕࡗࠤࡊࡼࡥ࡯ࡶࠣࡿࢂࠦࡲࡦࡵࡳࡳࡳࡹࡥࠡ࠼ࠣࡿࢂࠨ੪")
bstack1ll1l1ll1_opy_ = bstack1ll1_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡧࡴࡴࡦࡪࡩࡸࡶࡪࠦࡰࡳࡱࡻࡽࠥࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠫ੫")
bstack11l111l_opy_ = bstack1ll1_opy_ (u"ࠨࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡪࡷࡵ࡭ࠡ࠱ࡱࡩࡽࡺ࡟ࡩࡷࡥࡷࠥࢁࡽࠨ੬")
bstack11l111l11_opy_ = bstack1ll1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠠࡧࡴࡲࡱࠥ࠵࡮ࡦࡺࡷࡣ࡭ࡻࡢࡴ࠼ࠣࡿࢂ࠭੭")
bstack1l1111111_opy_ = bstack1ll1_opy_ (u"ࠪࡒࡪࡧࡲࡦࡵࡷࠤ࡭ࡻࡢࠡࡣ࡯ࡰࡴࡩࡡࡵࡧࡧࠤ࡮ࡹ࠺ࠡࡽࢀࠫ੮")
bstack1l11l1_opy_ = bstack1ll1_opy_ (u"ࠫࡊࡘࡒࡐࡔࠣࡍࡓࠦࡁࡍࡎࡒࡇࡆ࡚ࡅࠡࡊࡘࡆࠥࢁࡽࠨ੯")
bstack11l1l11_opy_ = bstack1ll1_opy_ (u"ࠬࡒࡡࡵࡧࡱࡧࡾࠦ࡯ࡧࠢ࡫ࡹࡧࡀࠠࡼࡿࠣ࡭ࡸࡀࠠࡼࡿࠪੰ")
bstack1l11l1l11_opy_ = bstack1ll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢ࡯ࡥࡹ࡫࡮ࡤࡻࠣࡪࡴࡸࠠࡼࡿࠣ࡬ࡺࡨ࠺ࠡࡽࢀࠫੱ")
bstack111lll11l_opy_ = bstack1ll1_opy_ (u"ࠧࡉࡷࡥࠤࡺࡸ࡬ࠡࡥ࡫ࡥࡳ࡭ࡥࡥࠢࡷࡳࠥࡺࡨࡦࠢࡲࡴࡹ࡯࡭ࡢ࡮ࠣ࡬ࡺࡨ࠺ࠡࡽࢀࠫੲ")
bstack1ll1111_opy_ = bstack1ll1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡴࡶࡴࡪ࡯ࡤࡰࠥ࡮ࡵࡣࠢࡸࡶࡱࡀࠠࡼࡿࠪੳ")
bstack1l1l11l1_opy_ = bstack1ll1_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡭ࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡰ࡮ࡹࡴࡴ࠼ࠣࡿࢂ࠭ੴ")
bstack111l11ll_opy_ = bstack1ll1_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡣࡷ࡬ࡰࡩࠦࡡࡳࡶ࡬ࡪࡦࡩࡴࡴ࠼ࠣࡿࢂ࠭ੵ")
bstack11lllll1l_opy_ = bstack1ll1_opy_ (u"࡚ࠫࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡰࡢࡥࠣࡪ࡮ࡲࡥࠡࡽࢀ࠲ࠥࡋࡲࡳࡱࡵࠤ࠲ࠦࡻࡾࠩ੶")
bstack11lll11ll_opy_ = bstack1ll1_opy_ (u"ࠬࠦࠠ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࠥࠦࡩࡧࠪࡳࡥ࡬࡫ࠠ࠾࠿ࡀࠤࡻࡵࡩࡥࠢ࠳࠭ࠥࢁ࡜࡯ࠢࠣࠤࡹࡸࡹࡼ࡞ࡱࠤࡨࡵ࡮ࡴࡶࠣࡪࡸࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪ࡟ࠫ࡫ࡹ࡜ࠨࠫ࠾ࡠࡳࠦࠠࠡࠢࠣࡪࡸ࠴ࡡࡱࡲࡨࡲࡩࡌࡩ࡭ࡧࡖࡽࡳࡩࠨࡣࡵࡷࡥࡨࡱ࡟ࡱࡣࡷ࡬࠱ࠦࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡱࡡ࡬ࡲࡩ࡫ࡸࠪࠢ࠮ࠤࠧࡀࠢࠡ࠭ࠣࡎࡘࡕࡎ࠯ࡵࡷࡶ࡮ࡴࡧࡪࡨࡼࠬࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࠪࡤࡻࡦ࡯ࡴࠡࡰࡨࡻࡕࡧࡧࡦ࠴࠱ࡩࡻࡧ࡬ࡶࡣࡷࡩ࠭ࠨࠨࠪࠢࡀࡂࠥࢁࡽࠣ࠮ࠣࡠࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧ࡭ࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡆࡨࡸࡦ࡯࡬ࡴࠤࢀࡠࠬ࠯ࠩࠪ࡝ࠥ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩࠨ࡝ࠪࠢ࠮ࠤࠧ࠲࡜࡝ࡰࠥ࠭ࡡࡴࠠࠡࠢࠣࢁࡨࡧࡴࡤࡪࠫࡩࡽ࠯ࡻ࡝ࡰࠣࠤࠥࠦࡽ࡝ࡰࠣࠤࢂࡢ࡮ࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࠬ੷")
bstack1l1ll1l1l_opy_ = bstack1ll1_opy_ (u"࠭࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࡩ࡯࡯ࡵࡷࠤࡧࡹࡴࡢࡥ࡮ࡣࡵࡧࡴࡩࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸ࡣ࡜࡯ࡥࡲࡲࡸࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠲࡟࡟ࡲࡨࡵ࡮ࡴࡶࠣࡴࡤ࡯࡮ࡥࡧࡻࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠲࡞࡞ࡱࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡷࡱ࡯ࡣࡦࠪ࠳࠰ࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳ࠪ࡞ࡱࡧࡴࡴࡳࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣࠫ࠾ࡠࡳ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡲࡡࡶࡰࡦ࡬ࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨ࡭ࡣࡸࡲࡨ࡮ࡏࡱࡶ࡬ࡳࡳࡹࠩࠡ࠿ࡁࠤࢀࡢ࡮࡭ࡧࡷࠤࡨࡧࡰࡴ࠽࡟ࡲࡹࡸࡹࠡࡽ࡟ࡲࡨࡧࡰࡴࠢࡀࠤࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸ࠯࡜࡯ࠢࠣࢁࠥࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࠡࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡩ࡯࡯ࡰࡨࡧࡹ࠮ࡻ࡝ࡰࠣࠤࠥࠦࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶ࠽ࠤࡥࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠤࡼࡧࡱࡧࡴࡪࡥࡖࡔࡌࡇࡴࡳࡰࡰࡰࡨࡲࡹ࠮ࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡤࡣࡳࡷ࠮࠯ࡽࡡ࠮࡟ࡲࠥࠦࠠࠡ࠰࠱࠲ࡱࡧࡵ࡯ࡥ࡫ࡓࡵࡺࡩࡰࡰࡶࡠࡳࠦࠠࡾࠫ࡟ࡲࢂࡢ࡮࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࠬ੸")
from ._version import __version__
bstack1ll111l1_opy_ = None
CONFIG = {}
bstack11ll1l111_opy_ = {}
bstack1ll1l1l1l_opy_ = {}
bstack1lll1111l_opy_ = None
bstack11l1111ll_opy_ = None
bstack11l1ll1ll_opy_ = None
bstack1l1111lll_opy_ = -1
bstack11l11111_opy_ = bstack11llll1_opy_
bstack11l1l1l11_opy_ = 1
bstack1l1ll11_opy_ = False
bstack11ll1ll_opy_ = False
bstack1ll1l1ll_opy_ = bstack1ll1_opy_ (u"ࠧࠨ੹")
bstack11ll111l1_opy_ = bstack1ll1_opy_ (u"ࠨࠩ੺")
bstack1ll1ll1l_opy_ = False
bstack1111ll1_opy_ = True
bstack11111l_opy_ = bstack1ll1_opy_ (u"ࠩࠪ੻")
bstack11l1111l_opy_ = []
bstack11l11lll1_opy_ = bstack1ll1_opy_ (u"ࠪࠫ੼")
bstack1lll1lll_opy_ = False
bstack11lll1l_opy_ = None
bstack111ll1l_opy_ = -1
bstack11111_opy_ = os.path.join(os.path.expanduser(bstack1ll1_opy_ (u"ࠫࢃ࠭੽")), bstack1ll1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ੾"), bstack1ll1_opy_ (u"࠭࠮ࡳࡱࡥࡳࡹ࠳ࡲࡦࡲࡲࡶࡹ࠳ࡨࡦ࡮ࡳࡩࡷ࠴ࡪࡴࡱࡱࠫ੿"))
bstack111lll_opy_ = []
bstack11llllll_opy_ = False
bstack1111l1l1_opy_ = None
bstack1l11lll_opy_ = None
bstack1llllllll_opy_ = None
bstack1l1l1l1_opy_ = None
bstack11ll11l_opy_ = None
bstack1lllll_opy_ = None
bstack11lll1_opy_ = None
bstack111l111_opy_ = None
bstack1l1l1l1l_opy_ = None
bstack1l11lllll_opy_ = None
bstack1111l11l_opy_ = None
bstack11l1lll1l_opy_ = None
bstack1ll1llll1_opy_ = None
bstack11llll1ll_opy_ = None
bstack111l1l_opy_ = None
bstack1ll11ll1l_opy_ = None
bstack11l1l1ll1_opy_ = bstack1ll1_opy_ (u"ࠢࠣ઀")
class bstack11l1lll1_opy_(threading.Thread):
  def run(self):
    self.exc = None
    try:
      self.ret = self._target(*self._args, **self._kwargs)
    except Exception as e:
      self.exc = e
  def join(self, timeout=None):
    super(bstack11l1lll1_opy_, self).join(timeout)
    if self.exc:
      raise self.exc
    return self.ret
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack11l11111_opy_,
                    format=bstack1ll1_opy_ (u"ࠨ࡞ࡱࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭ઁ"),
                    datefmt=bstack1ll1_opy_ (u"ࠩࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫં"))
def bstack1l1l111l_opy_():
  global CONFIG
  global bstack11l11111_opy_
  if bstack1ll1_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬઃ") in CONFIG:
    bstack11l11111_opy_ = bstack1ll1lll1l_opy_[CONFIG[bstack1ll1_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭઄")]]
    logging.getLogger().setLevel(bstack11l11111_opy_)
def bstack1l1l1ll1_opy_():
  global CONFIG
  global bstack11llllll_opy_
  bstack1l11ll111_opy_ = bstack1l1l111ll_opy_(CONFIG)
  if(bstack1ll1_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧઅ") in bstack1l11ll111_opy_ and str(bstack1l11ll111_opy_[bstack1ll1_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨઆ")]).lower() == bstack1ll1_opy_ (u"ࠧࡵࡴࡸࡩࠬઇ")):
    bstack11llllll_opy_ = True
def bstack1lll1ll1_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1lll1111_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l1ll1111_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1ll1_opy_ (u"ࠣ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡥࡲࡲ࡫࡯ࡧࡧ࡫࡯ࡩࠧઈ") == args[i].lower() or bstack1ll1_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡴࡦࡪࡩࠥઉ") == args[i].lower():
      path = args[i+1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack11111l_opy_
      bstack11111l_opy_ += bstack1ll1_opy_ (u"ࠪ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡇࡴࡴࡦࡪࡩࡉ࡭ࡱ࡫ࠠࠨઊ") + path
      return path
  return None
def bstack111ll1_opy_():
  bstack11l1ll1l1_opy_ = bstack1l1ll1111_opy_()
  if bstack11l1ll1l1_opy_ and os.path.exists(os.path.abspath(bstack11l1ll1l1_opy_)):
    fileName = bstack11l1ll1l1_opy_
  if bstack1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨઋ") in os.environ and os.path.exists(os.path.abspath(os.environ[bstack1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆࠩઌ")])) and not bstack1ll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡒࡦࡳࡥࠨઍ") in locals():
    fileName = os.environ[bstack1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ઎")]
  if bstack1ll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡔࡡ࡮ࡧࠪએ") in locals():
    bstack111ll1111_opy_ = os.path.abspath(fileName)
  else:
    bstack111ll1111_opy_ = bstack1ll1_opy_ (u"ࠩࠪઐ")
  bstack1l1ll111l_opy_ = os.getcwd()
  bstack11l1l1_opy_ = bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ઑ")
  bstack1l1ll1lll_opy_ = bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡦࡳ࡬ࠨ઒")
  while (not os.path.exists(bstack111ll1111_opy_)) and bstack1l1ll111l_opy_ != bstack1ll1_opy_ (u"ࠧࠨઓ"):
    bstack111ll1111_opy_ = os.path.join(bstack1l1ll111l_opy_, bstack11l1l1_opy_)
    if not os.path.exists(bstack111ll1111_opy_):
      bstack111ll1111_opy_ = os.path.join(bstack1l1ll111l_opy_, bstack1l1ll1lll_opy_)
    if bstack1l1ll111l_opy_ != os.path.dirname(bstack1l1ll111l_opy_):
      bstack1l1ll111l_opy_ = os.path.dirname(bstack1l1ll111l_opy_)
    else:
      bstack1l1ll111l_opy_ = bstack1ll1_opy_ (u"ࠨࠢઔ")
  if not os.path.exists(bstack111ll1111_opy_):
    bstack11ll1l11l_opy_(
      bstack1l1lllll_opy_.format(os.getcwd()))
  with open(bstack111ll1111_opy_, bstack1ll1_opy_ (u"ࠧࡳࠩક")) as stream:
    try:
      config = yaml.safe_load(stream)
      return config
    except yaml.YAMLError as exc:
      bstack11ll1l11l_opy_(bstack1l111lll_opy_.format(str(exc)))
def bstack11l1l1lll_opy_(config):
  bstack1l1l11l_opy_ = bstack11ll11111_opy_(config)
  for option in list(bstack1l1l11l_opy_):
    if option.lower() in bstack1ll1l1l11_opy_ and option != bstack1ll1l1l11_opy_[option.lower()]:
      bstack1l1l11l_opy_[bstack1ll1l1l11_opy_[option.lower()]] = bstack1l1l11l_opy_[option]
      del bstack1l1l11l_opy_[option]
  return config
def bstack11ll111_opy_():
  global bstack1ll1l1l1l_opy_
  for key, bstack1l1ll_opy_ in bstack1l11_opy_.items():
    if isinstance(bstack1l1ll_opy_, list):
      for var in bstack1l1ll_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1ll1l1l1l_opy_[key] = os.environ[var]
          break
    elif bstack1l1ll_opy_ in os.environ and os.environ[bstack1l1ll_opy_] and str(os.environ[bstack1l1ll_opy_]).strip():
      bstack1ll1l1l1l_opy_[key] = os.environ[bstack1l1ll_opy_]
  if bstack1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪખ") in os.environ:
    bstack1ll1l1l1l_opy_[bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ગ")] = {}
    bstack1ll1l1l1l_opy_[bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧઘ")][bstack1ll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ઙ")] = os.environ[bstack1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧચ")]
def bstack11ll1llll_opy_():
  global bstack11ll1l111_opy_
  global bstack11111l_opy_
  for idx, val in enumerate(sys.argv):
    if idx<len(sys.argv) and bstack1ll1_opy_ (u"࠭࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩછ").lower() == val.lower():
      bstack11ll1l111_opy_[bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫજ")] = {}
      bstack11ll1l111_opy_[bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬઝ")][bstack1ll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫઞ")] = sys.argv[idx+1]
      del sys.argv[idx:idx+2]
      break
  for key, bstack11lll11_opy_ in bstack1ll11l1ll_opy_.items():
    if isinstance(bstack11lll11_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack11lll11_opy_:
          if idx<len(sys.argv) and bstack1ll1_opy_ (u"ࠪ࠱࠲࠭ટ") + var.lower() == val.lower() and not key in bstack11ll1l111_opy_:
            bstack11ll1l111_opy_[key] = sys.argv[idx+1]
            bstack11111l_opy_ += bstack1ll1_opy_ (u"ࠫࠥ࠳࠭ࠨઠ") + var + bstack1ll1_opy_ (u"ࠬࠦࠧડ") + sys.argv[idx+1]
            del sys.argv[idx:idx+2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx<len(sys.argv) and bstack1ll1_opy_ (u"࠭࠭࠮ࠩઢ") + bstack11lll11_opy_.lower() == val.lower() and not key in bstack11ll1l111_opy_:
          bstack11ll1l111_opy_[key] = sys.argv[idx+1]
          bstack11111l_opy_ += bstack1ll1_opy_ (u"ࠧࠡ࠯࠰ࠫણ") + bstack11lll11_opy_ + bstack1ll1_opy_ (u"ࠨࠢࠪત") + sys.argv[idx+1]
          del sys.argv[idx:idx+2]
def bstack1l1l1l11_opy_(config):
  bstack1l111lll1_opy_ = config.keys()
  for bstack11l11l_opy_, bstack1lll1l11_opy_ in bstack111llllll_opy_.items():
    if bstack1lll1l11_opy_ in bstack1l111lll1_opy_:
      config[bstack11l11l_opy_] = config[bstack1lll1l11_opy_]
      del config[bstack1lll1l11_opy_]
  for bstack11l11l_opy_, bstack1lll1l11_opy_ in bstack1l111l1ll_opy_.items():
    if isinstance(bstack1lll1l11_opy_, list):
      for bstack1l1llll1l_opy_ in bstack1lll1l11_opy_:
        if bstack1l1llll1l_opy_ in bstack1l111lll1_opy_:
          config[bstack11l11l_opy_] = config[bstack1l1llll1l_opy_]
          del config[bstack1l1llll1l_opy_]
          break
    elif bstack1lll1l11_opy_ in bstack1l111lll1_opy_:
        config[bstack11l11l_opy_] = config[bstack1lll1l11_opy_]
        del config[bstack1lll1l11_opy_]
  for bstack1l1llll1l_opy_ in list(config):
    for bstack1l111l111_opy_ in bstack1111ll11_opy_:
      if bstack1l1llll1l_opy_.lower() == bstack1l111l111_opy_.lower() and bstack1l1llll1l_opy_ != bstack1l111l111_opy_:
        config[bstack1l111l111_opy_] = config[bstack1l1llll1l_opy_]
        del config[bstack1l1llll1l_opy_]
  bstack1111l111_opy_ = []
  if bstack1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬથ") in config:
    bstack1111l111_opy_ = config[bstack1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭દ")]
  for platform in bstack1111l111_opy_:
    for bstack1l1llll1l_opy_ in list(platform):
      for bstack1l111l111_opy_ in bstack1111ll11_opy_:
        if bstack1l1llll1l_opy_.lower() == bstack1l111l111_opy_.lower() and bstack1l1llll1l_opy_ != bstack1l111l111_opy_:
          platform[bstack1l111l111_opy_] = platform[bstack1l1llll1l_opy_]
          del platform[bstack1l1llll1l_opy_]
  for bstack11l11l_opy_, bstack1lll1l11_opy_ in bstack1l111l1ll_opy_.items():
    for platform in bstack1111l111_opy_:
      if isinstance(bstack1lll1l11_opy_, list):
        for bstack1l1llll1l_opy_ in bstack1lll1l11_opy_:
          if bstack1l1llll1l_opy_ in platform:
            platform[bstack11l11l_opy_] = platform[bstack1l1llll1l_opy_]
            del platform[bstack1l1llll1l_opy_]
            break
      elif bstack1lll1l11_opy_ in platform:
        platform[bstack11l11l_opy_] = platform[bstack1lll1l11_opy_]
        del platform[bstack1lll1l11_opy_]
  for bstack1lllll111_opy_ in bstack1l1l1111l_opy_:
    if bstack1lllll111_opy_ in config:
      if not bstack1l1l1111l_opy_[bstack1lllll111_opy_] in config:
        config[bstack1l1l1111l_opy_[bstack1lllll111_opy_]] = {}
      config[bstack1l1l1111l_opy_[bstack1lllll111_opy_]].update(config[bstack1lllll111_opy_])
      del config[bstack1lllll111_opy_]
  for platform in bstack1111l111_opy_:
    for bstack1lllll111_opy_ in bstack1l1l1111l_opy_:
      if bstack1lllll111_opy_ in list(platform):
        if not bstack1l1l1111l_opy_[bstack1lllll111_opy_] in platform:
          platform[bstack1l1l1111l_opy_[bstack1lllll111_opy_]] = {}
        platform[bstack1l1l1111l_opy_[bstack1lllll111_opy_]].update(platform[bstack1lllll111_opy_])
        del platform[bstack1lllll111_opy_]
  config = bstack11l1l1lll_opy_(config)
  return config
def bstack1lllll1ll_opy_(config):
  global bstack11ll111l1_opy_
  if bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨધ") in config and str(config[bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩન")]).lower() != bstack1ll1_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ઩"):
    if not bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫપ") in config:
      config[bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬફ")] = {}
    if not bstack1ll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫબ") in config[bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧભ")]:
      bstack11l111ll1_opy_ = datetime.datetime.now()
      bstack11l11l1l1_opy_ = bstack11l111ll1_opy_.strftime(bstack1ll1_opy_ (u"ࠫࠪࡪ࡟ࠦࡤࡢࠩࡍࠫࡍࠨમ"))
      hostname = socket.gethostname()
      bstack111ll111l_opy_ = bstack1ll1_opy_ (u"ࠬ࠭ય").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1ll1_opy_ (u"࠭ࡻࡾࡡࡾࢁࡤࢁࡽࠨર").format(bstack11l11l1l1_opy_, hostname, bstack111ll111l_opy_)
      config[bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ઱")][bstack1ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪલ")] = identifier
    bstack11ll111l1_opy_ = config[bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ળ")][bstack1ll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ઴")]
  return config
def bstack1llll1111_opy_():
  if (
    isinstance(os.getenv(bstack1ll1_opy_ (u"ࠫࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠩવ")), str) and len(os.getenv(bstack1ll1_opy_ (u"ࠬࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠪશ"))) > 0
  ) or (
    isinstance(os.getenv(bstack1ll1_opy_ (u"࠭ࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠬષ")), str) and len(os.getenv(bstack1ll1_opy_ (u"ࠧࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊ࠭સ"))) > 0
  ):
    return os.getenv(bstack1ll1_opy_ (u"ࠨࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠧહ"), 0)
  if str(os.getenv(bstack1ll1_opy_ (u"ࠩࡆࡍࠬ઺"))).lower() == bstack1ll1_opy_ (u"ࠪࡸࡷࡻࡥࠨ઻") and str(os.getenv(bstack1ll1_opy_ (u"ࠫࡈࡏࡒࡄࡎࡈࡇࡎ઼࠭"))).lower() == bstack1ll1_opy_ (u"ࠬࡺࡲࡶࡧࠪઽ"):
    return os.getenv(bstack1ll1_opy_ (u"࠭ࡃࡊࡔࡆࡐࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࠩા"), 0)
  if str(os.getenv(bstack1ll1_opy_ (u"ࠧࡄࡋࠪિ"))).lower() == bstack1ll1_opy_ (u"ࠨࡶࡵࡹࡪ࠭ી") and str(os.getenv(bstack1ll1_opy_ (u"ࠩࡗࡖࡆ࡜ࡉࡔࠩુ"))).lower() == bstack1ll1_opy_ (u"ࠪࡸࡷࡻࡥࠨૂ"):
    return os.getenv(bstack1ll1_opy_ (u"࡙ࠫࡘࡁࡗࡋࡖࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠪૃ"), 0)
  if str(os.getenv(bstack1ll1_opy_ (u"ࠬࡉࡉࠨૄ"))).lower() == bstack1ll1_opy_ (u"࠭ࡴࡳࡷࡨࠫૅ") and str(os.getenv(bstack1ll1_opy_ (u"ࠧࡄࡋࡢࡒࡆࡓࡅࠨ૆"))).lower() == bstack1ll1_opy_ (u"ࠨࡥࡲࡨࡪࡹࡨࡪࡲࠪે"):
    return 0 # bstack1lll1ll_opy_ bstack1ll1l111l_opy_ not set build number env
  if os.getenv(bstack1ll1_opy_ (u"ࠩࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡒࡂࡐࡆࡌࠬૈ")) and os.getenv(bstack1ll1_opy_ (u"ࠪࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡃࡐࡏࡐࡍ࡙࠭ૉ")):
    return os.getenv(bstack1ll1_opy_ (u"ࠫࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗ࠭૊"), 0)
  if str(os.getenv(bstack1ll1_opy_ (u"ࠬࡉࡉࠨો"))).lower() == bstack1ll1_opy_ (u"࠭ࡴࡳࡷࡨࠫૌ") and str(os.getenv(bstack1ll1_opy_ (u"ࠧࡅࡔࡒࡒࡊ્࠭"))).lower() == bstack1ll1_opy_ (u"ࠨࡶࡵࡹࡪ࠭૎"):
    return os.getenv(bstack1ll1_opy_ (u"ࠩࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠧ૏"), 0)
  if str(os.getenv(bstack1ll1_opy_ (u"ࠪࡇࡎ࠭ૐ"))).lower() == bstack1ll1_opy_ (u"ࠫࡹࡸࡵࡦࠩ૑") and str(os.getenv(bstack1ll1_opy_ (u"࡙ࠬࡅࡎࡃࡓࡌࡔࡘࡅࠨ૒"))).lower() == bstack1ll1_opy_ (u"࠭ࡴࡳࡷࡨࠫ૓"):
    return os.getenv(bstack1ll1_opy_ (u"ࠧࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡊࡆࠪ૔"), 0)
  if str(os.getenv(bstack1ll1_opy_ (u"ࠨࡅࡌࠫ૕"))).lower() == bstack1ll1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ૖") and str(os.getenv(bstack1ll1_opy_ (u"ࠪࡋࡎ࡚ࡌࡂࡄࡢࡇࡎ࠭૗"))).lower() == bstack1ll1_opy_ (u"ࠫࡹࡸࡵࡦࠩ૘"):
    return os.getenv(bstack1ll1_opy_ (u"ࠬࡉࡉࡠࡌࡒࡆࡤࡏࡄࠨ૙"), 0)
  if str(os.getenv(bstack1ll1_opy_ (u"࠭ࡃࡊࠩ૚"))).lower() == bstack1ll1_opy_ (u"ࠧࡵࡴࡸࡩࠬ૛") and str(os.getenv(bstack1ll1_opy_ (u"ࠨࡄࡘࡍࡑࡊࡋࡊࡖࡈࠫ૜"))).lower() == bstack1ll1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ૝"):
    return os.getenv(bstack1ll1_opy_ (u"ࠪࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠬ૞"), 0)
  if str(os.getenv(bstack1ll1_opy_ (u"࡙ࠫࡌ࡟ࡃࡗࡌࡐࡉ࠭૟"))).lower() == bstack1ll1_opy_ (u"ࠬࡺࡲࡶࡧࠪૠ"):
    return os.getenv(bstack1ll1_opy_ (u"࠭ࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉ࠭ૡ"), 0)
  return -1
def bstack1l11l1l_opy_(bstack11lll1l11_opy_):
  global CONFIG
  if not bstack1ll1_opy_ (u"ࠧࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩૢ") in CONFIG[bstack1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪૣ")]:
    return
  CONFIG[bstack1ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ૤")] = CONFIG[bstack1ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ૥")].replace(
    bstack1ll1_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭૦"),
    str(bstack11lll1l11_opy_)
  )
def bstack111llll1l_opy_():
  global CONFIG
  if not bstack1ll1_opy_ (u"ࠬࠪࡻࡅࡃࡗࡉࡤ࡚ࡉࡎࡇࢀࠫ૧") in CONFIG[bstack1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૨")]:
    return
  bstack11l111ll1_opy_ = datetime.datetime.now()
  bstack11l11l1l1_opy_ = bstack11l111ll1_opy_.strftime(bstack1ll1_opy_ (u"ࠧࠦࡦ࠰ࠩࡧ࠳ࠥࡉ࠼ࠨࡑࠬ૩"))
  CONFIG[bstack1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ૪")] = CONFIG[bstack1ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ૫")].replace(
    bstack1ll1_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾࠩ૬"),
    bstack11l11l1l1_opy_
  )
def bstack1111l1ll_opy_():
  global CONFIG
  if bstack1ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭૭") in CONFIG and not bool(CONFIG[bstack1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ૮")]):
    del CONFIG[bstack1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૯")]
    return
  if not bstack1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ૰") in CONFIG:
    CONFIG[bstack1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ૱")] = bstack1ll1_opy_ (u"ࠩࠦࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬ૲")
  if bstack1ll1_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾࠩ૳") in CONFIG[bstack1ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭૴")]:
    bstack111llll1l_opy_()
    os.environ[bstack1ll1_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩ૵")] = CONFIG[bstack1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૶")]
  if not bstack1ll1_opy_ (u"ࠧࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩ૷") in CONFIG[bstack1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ૸")]:
    return
  bstack11lll1l11_opy_ = bstack1ll1_opy_ (u"ࠩࠪૹ")
  bstack11ll11lll_opy_ = bstack1llll1111_opy_()
  if bstack11ll11lll_opy_ != -1:
    bstack11lll1l11_opy_ = bstack1ll1_opy_ (u"ࠪࡇࡎࠦࠧૺ") + str(bstack11ll11lll_opy_)
  if bstack11lll1l11_opy_ == bstack1ll1_opy_ (u"ࠫࠬૻ"):
    bstack1l111ll1l_opy_ = bstack1l1l111l1_opy_(CONFIG[bstack1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨૼ")])
    if bstack1l111ll1l_opy_ != -1:
      bstack11lll1l11_opy_ = str(bstack1l111ll1l_opy_)
  if bstack11lll1l11_opy_:
    bstack1l11l1l_opy_(bstack11lll1l11_opy_)
    os.environ[bstack1ll1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ૽")] = CONFIG[bstack1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ૾")]
def bstack1l1llll_opy_(bstack1ll1ll1ll_opy_, bstack1lll111l_opy_, path):
  bstack111ll11l_opy_ = {
    bstack1ll1_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ૿"): bstack1lll111l_opy_
  }
  if os.path.exists(path):
    bstack11111ll1_opy_ = json.load(open(path, bstack1ll1_opy_ (u"ࠩࡵࡦࠬ଀")))
  else:
    bstack11111ll1_opy_ = {}
  bstack11111ll1_opy_[bstack1ll1ll1ll_opy_] = bstack111ll11l_opy_
  with open(path, bstack1ll1_opy_ (u"ࠥࡻ࠰ࠨଁ")) as outfile:
    json.dump(bstack11111ll1_opy_, outfile)
def bstack1l1l111l1_opy_(bstack1ll1ll1ll_opy_):
  bstack1ll1ll1ll_opy_ = str(bstack1ll1ll1ll_opy_)
  bstack111ll1l1_opy_ = os.path.join(os.path.expanduser(bstack1ll1_opy_ (u"ࠫࢃ࠭ଂ")), bstack1ll1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬଃ"))
  try:
    if not os.path.exists(bstack111ll1l1_opy_):
      os.makedirs(bstack111ll1l1_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1ll1_opy_ (u"࠭ࡾࠨ଄")), bstack1ll1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧଅ"), bstack1ll1_opy_ (u"ࠨ࠰ࡥࡹ࡮ࡲࡤ࠮ࡰࡤࡱࡪ࠳ࡣࡢࡥ࡫ࡩ࠳ࡰࡳࡰࡰࠪଆ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1ll1_opy_ (u"ࠩࡺࠫଇ")):
        pass
      with open(file_path, bstack1ll1_opy_ (u"ࠥࡻ࠰ࠨଈ")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1ll1_opy_ (u"ࠫࡷ࠭ଉ")) as bstack11l1l1l1l_opy_:
      bstack1llll1ll1_opy_ = json.load(bstack11l1l1l1l_opy_)
    if bstack1ll1ll1ll_opy_ in bstack1llll1ll1_opy_:
      bstack1ll111_opy_ = bstack1llll1ll1_opy_[bstack1ll1ll1ll_opy_][bstack1ll1_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩଊ")]
      bstack111lllll_opy_ = int(bstack1ll111_opy_) + 1
      bstack1l1llll_opy_(bstack1ll1ll1ll_opy_, bstack111lllll_opy_, file_path)
      return bstack111lllll_opy_
    else:
      bstack1l1llll_opy_(bstack1ll1ll1ll_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1l1lll1_opy_.format(str(e)))
    return -1
def bstack1l1l1lll_opy_(config):
  if not config[bstack1ll1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨଋ")] or not config[bstack1ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪଌ")]:
    return True
  else:
    return False
def bstack11ll1ll1_opy_(config):
  if bstack1ll1_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧ଍") in config:
    del(config[bstack1ll1_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨ଎")])
    return False
  if bstack1lll1111_opy_() < version.parse(bstack1ll1_opy_ (u"ࠪ࠷࠳࠺࠮࠱ࠩଏ")):
    return False
  if bstack1lll1111_opy_() >= version.parse(bstack1ll1_opy_ (u"ࠫ࠹࠴࠱࠯࠷ࠪଐ")):
    return True
  if bstack1ll1_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ଑") in config and config[bstack1ll1_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭଒")] == False:
    return False
  else:
    return True
def bstack1l1ll1l11_opy_(config, index = 0):
  global bstack1ll1ll1l_opy_
  bstack11llll_opy_ = {}
  caps = bstack1l11ll1ll_opy_ + bstack111ll_opy_
  if bstack1ll1ll1l_opy_:
    caps += bstack1lll1ll1l_opy_
  for key in config:
    if key in caps + [bstack1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଓ")]:
      continue
    bstack11llll_opy_[key] = config[key]
  if bstack1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫଔ") in config:
    for bstack11l1l1111_opy_ in config[bstack1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬକ")][index]:
      if bstack11l1l1111_opy_ in caps + [bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨଖ"), bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬଗ")]:
        continue
      bstack11llll_opy_[bstack11l1l1111_opy_] = config[bstack1ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଘ")][index][bstack11l1l1111_opy_]
  bstack11llll_opy_[bstack1ll1_opy_ (u"࠭ࡨࡰࡵࡷࡒࡦࡳࡥࠨଙ")] = socket.gethostname()
  if bstack1ll1_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨଚ") in bstack11llll_opy_:
    del(bstack11llll_opy_[bstack1ll1_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩଛ")])
  return bstack11llll_opy_
def bstack11l1l1ll_opy_(config):
  global bstack1ll1ll1l_opy_
  bstack1lll11ll1_opy_ = {}
  caps = bstack111ll_opy_
  if bstack1ll1ll1l_opy_:
    caps+= bstack1lll1ll1l_opy_
  for key in caps:
    if key in config:
      bstack1lll11ll1_opy_[key] = config[key]
  return bstack1lll11ll1_opy_
def bstack1ll11ll1_opy_(bstack11llll_opy_, bstack1lll11ll1_opy_):
  bstack1lll1llll_opy_ = {}
  for key in bstack11llll_opy_.keys():
    if key in bstack111llllll_opy_:
      bstack1lll1llll_opy_[bstack111llllll_opy_[key]] = bstack11llll_opy_[key]
    else:
      bstack1lll1llll_opy_[key] = bstack11llll_opy_[key]
  for key in bstack1lll11ll1_opy_:
    if key in bstack111llllll_opy_:
      bstack1lll1llll_opy_[bstack111llllll_opy_[key]] = bstack1lll11ll1_opy_[key]
    else:
      bstack1lll1llll_opy_[key] = bstack1lll11ll1_opy_[key]
  return bstack1lll1llll_opy_
def bstack1lll1_opy_(config, index = 0):
  global bstack1ll1ll1l_opy_
  caps = {}
  bstack1lll11ll1_opy_ = bstack11l1l1ll_opy_(config)
  bstack11ll111l_opy_ = bstack111ll_opy_
  bstack11ll111l_opy_ += bstack11l1l111l_opy_
  if bstack1ll1ll1l_opy_:
    bstack11ll111l_opy_ += bstack1lll1ll1l_opy_
  if bstack1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬଜ") in config:
    if bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨଝ") in config[bstack1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଞ")][index]:
      caps[bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪଟ")] = config[bstack1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଠ")][index][bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬଡ")]
    if bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩଢ") in config[bstack1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬଣ")][index]:
      caps[bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫତ")] = str(config[bstack1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଥ")][index][bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ଦ")])
    bstack1l1ll1ll1_opy_ = {}
    for bstack111ll1ll_opy_ in bstack11ll111l_opy_:
      if bstack111ll1ll_opy_ in config[bstack1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଧ")][index]:
        if bstack111ll1ll_opy_ == bstack1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩନ"):
          bstack1l1ll1ll1_opy_[bstack111ll1ll_opy_] = str(config[bstack1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ଩")][index][bstack111ll1ll_opy_] * 1.0)
        else:
          bstack1l1ll1ll1_opy_[bstack111ll1ll_opy_] = config[bstack1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬପ")][index][bstack111ll1ll_opy_]
        del(config[bstack1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଫ")][index][bstack111ll1ll_opy_])
    bstack1lll11ll1_opy_ = update(bstack1lll11ll1_opy_, bstack1l1ll1ll1_opy_)
  bstack11llll_opy_ = bstack1l1ll1l11_opy_(config, index)
  for bstack1l1llll1l_opy_ in bstack111ll_opy_ + [bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩବ"), bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ଭ")]:
    if bstack1l1llll1l_opy_ in bstack11llll_opy_:
      bstack1lll11ll1_opy_[bstack1l1llll1l_opy_] = bstack11llll_opy_[bstack1l1llll1l_opy_]
      del(bstack11llll_opy_[bstack1l1llll1l_opy_])
  if bstack11ll1ll1_opy_(config):
    bstack11llll_opy_[bstack1ll1_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ମ")] = True
    caps.update(bstack1lll11ll1_opy_)
    caps[bstack1ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨଯ")] = bstack11llll_opy_
  else:
    bstack11llll_opy_[bstack1ll1_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨର")] = False
    caps.update(bstack1ll11ll1_opy_(bstack11llll_opy_, bstack1lll11ll1_opy_))
    if bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ଱") in caps:
      caps[bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫଲ")] = caps[bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩଳ")]
      del(caps[bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ଴")])
    if bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧଵ") in caps:
      caps[bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩଶ")] = caps[bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩଷ")]
      del(caps[bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪସ")])
  return caps
def bstack11lllll1_opy_():
  global bstack11l11lll1_opy_
  if bstack1lll1111_opy_() <= version.parse(bstack1ll1_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪହ")):
    if bstack11l11lll1_opy_ != bstack1ll1_opy_ (u"ࠫࠬ଺"):
      return bstack1ll1_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨ଻") + bstack11l11lll1_opy_ + bstack1ll1_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤ଼ࠥ")
    return bstack11ll1lll1_opy_
  if  bstack11l11lll1_opy_ != bstack1ll1_opy_ (u"ࠧࠨଽ"):
    return bstack1ll1_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥା") + bstack11l11lll1_opy_ + bstack1ll1_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥି")
  return bstack1ll1l_opy_
def bstack11l1l11ll_opy_(options):
  return hasattr(options, bstack1ll1_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫୀ"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack111lllll1_opy_(options, bstack1llll1lll_opy_):
  for bstack11l11lll_opy_ in bstack1llll1lll_opy_:
    if bstack11l11lll_opy_ in [bstack1ll1_opy_ (u"ࠫࡦࡸࡧࡴࠩୁ"), bstack1ll1_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩୂ")]:
      next
    if bstack11l11lll_opy_ in options._experimental_options:
      options._experimental_options[bstack11l11lll_opy_]= update(options._experimental_options[bstack11l11lll_opy_], bstack1llll1lll_opy_[bstack11l11lll_opy_])
    else:
      options.add_experimental_option(bstack11l11lll_opy_, bstack1llll1lll_opy_[bstack11l11lll_opy_])
  if bstack1ll1_opy_ (u"࠭ࡡࡳࡩࡶࠫୃ") in bstack1llll1lll_opy_:
    for arg in bstack1llll1lll_opy_[bstack1ll1_opy_ (u"ࠧࡢࡴࡪࡷࠬୄ")]:
      options.add_argument(arg)
    del(bstack1llll1lll_opy_[bstack1ll1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭୅")])
  if bstack1ll1_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭୆") in bstack1llll1lll_opy_:
    for ext in bstack1llll1lll_opy_[bstack1ll1_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧେ")]:
      options.add_extension(ext)
    del(bstack1llll1lll_opy_[bstack1ll1_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨୈ")])
def bstack1lll11_opy_(options, bstack1l11111ll_opy_):
  if bstack1ll1_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ୉") in bstack1l11111ll_opy_:
    for bstack1l111ll1_opy_ in bstack1l11111ll_opy_[bstack1ll1_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬ୊")]:
      if bstack1l111ll1_opy_ in options._preferences:
        options._preferences[bstack1l111ll1_opy_] = update(options._preferences[bstack1l111ll1_opy_], bstack1l11111ll_opy_[bstack1ll1_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ୋ")][bstack1l111ll1_opy_])
      else:
        options.set_preference(bstack1l111ll1_opy_, bstack1l11111ll_opy_[bstack1ll1_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧୌ")][bstack1l111ll1_opy_])
  if bstack1ll1_opy_ (u"ࠩࡤࡶ࡬ࡹ୍ࠧ") in bstack1l11111ll_opy_:
    for arg in bstack1l11111ll_opy_[bstack1ll1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ୎")]:
      options.add_argument(arg)
def bstack111lll1ll_opy_(options, bstack1l1lllll1_opy_):
  if bstack1ll1_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࠬ୏") in bstack1l1lllll1_opy_:
    options.use_webview(bool(bstack1l1lllll1_opy_[bstack1ll1_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼ࠭୐")]))
  bstack111lllll1_opy_(options, bstack1l1lllll1_opy_)
def bstack11llll11l_opy_(options, bstack11l1ll_opy_):
  for bstack1l1111ll_opy_ in bstack11l1ll_opy_:
    if bstack1l1111ll_opy_ in [bstack1ll1_opy_ (u"࠭ࡴࡦࡥ࡫ࡲࡴࡲ࡯ࡨࡻࡓࡶࡪࡼࡩࡦࡹࠪ୑"), bstack1ll1_opy_ (u"ࠧࡢࡴࡪࡷࠬ୒")]:
      next
    options.set_capability(bstack1l1111ll_opy_, bstack11l1ll_opy_[bstack1l1111ll_opy_])
  if bstack1ll1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭୓") in bstack11l1ll_opy_:
    for arg in bstack11l1ll_opy_[bstack1ll1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ୔")]:
      options.add_argument(arg)
  if bstack1ll1_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧ୕") in bstack11l1ll_opy_:
    options.use_technology_preview(bool(bstack11l1ll_opy_[bstack1ll1_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨୖ")]))
def bstack11l1llll1_opy_(options, bstack11ll1l1ll_opy_):
  for bstack1l1llllll_opy_ in bstack11ll1l1ll_opy_:
    if bstack1l1llllll_opy_ in [bstack1ll1_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩୗ"), bstack1ll1_opy_ (u"࠭ࡡࡳࡩࡶࠫ୘")]:
      next
    options._options[bstack1l1llllll_opy_] = bstack11ll1l1ll_opy_[bstack1l1llllll_opy_]
  if bstack1ll1_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ୙") in bstack11ll1l1ll_opy_:
    for bstack1l11llll1_opy_ in bstack11ll1l1ll_opy_[bstack1ll1_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ୚")]:
      options.bstack1lll1l1ll_opy_(
          bstack1l11llll1_opy_, bstack11ll1l1ll_opy_[bstack1ll1_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭୛")][bstack1l11llll1_opy_])
  if bstack1ll1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨଡ଼") in bstack11ll1l1ll_opy_:
    for arg in bstack11ll1l1ll_opy_[bstack1ll1_opy_ (u"ࠫࡦࡸࡧࡴࠩଢ଼")]:
      options.add_argument(arg)
def bstack11ll1111l_opy_(options, caps):
  if not hasattr(options, bstack1ll1_opy_ (u"ࠬࡑࡅ࡚ࠩ୞")):
    return
  if options.KEY == bstack1ll1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫୟ") and options.KEY in caps:
    bstack111lllll1_opy_(options, caps[bstack1ll1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬୠ")])
  elif options.KEY == bstack1ll1_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ୡ") and options.KEY in caps:
    bstack1lll11_opy_(options, caps[bstack1ll1_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧୢ")])
  elif options.KEY == bstack1ll1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫୣ") and options.KEY in caps:
    bstack11llll11l_opy_(options, caps[bstack1ll1_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬ୤")])
  elif options.KEY == bstack1ll1_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭୥") and options.KEY in caps:
    bstack111lll1ll_opy_(options, caps[bstack1ll1_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ୦")])
  elif options.KEY == bstack1ll1_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭୧") and options.KEY in caps:
    bstack11l1llll1_opy_(options, caps[bstack1ll1_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ୨")])
def bstack1l11l1111_opy_(caps):
  global bstack1ll1ll1l_opy_
  if bstack1ll1ll1l_opy_:
    if bstack1lll1ll1_opy_() < version.parse(bstack1ll1_opy_ (u"ࠩ࠵࠲࠸࠴࠰ࠨ୩")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1ll1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪ୪")
    if bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ୫") in caps:
      browser = caps[bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ୬")]
    elif bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ୭") in caps:
      browser = caps[bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ୮")]
    browser = str(browser).lower()
    if browser == bstack1ll1_opy_ (u"ࠨ࡫ࡳ࡬ࡴࡴࡥࠨ୯") or browser == bstack1ll1_opy_ (u"ࠩ࡬ࡴࡦࡪࠧ୰"):
      browser = bstack1ll1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪୱ")
    if browser == bstack1ll1_opy_ (u"ࠫࡸࡧ࡭ࡴࡷࡱ࡫ࠬ୲"):
      browser = bstack1ll1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬ୳")
    if browser not in [bstack1ll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭୴"), bstack1ll1_opy_ (u"ࠧࡦࡦࡪࡩࠬ୵"), bstack1ll1_opy_ (u"ࠨ࡫ࡨࠫ୶"), bstack1ll1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩ୷"), bstack1ll1_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫ୸")]:
      return None
    try:
      package = bstack1ll1_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡾࢁ࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭୹").format(browser)
      name = bstack1ll1_opy_ (u"ࠬࡕࡰࡵ࡫ࡲࡲࡸ࠭୺")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack11l1l11ll_opy_(options):
        return None
      for bstack1l1llll1l_opy_ in caps.keys():
        options.set_capability(bstack1l1llll1l_opy_, caps[bstack1l1llll1l_opy_])
      bstack11ll1111l_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1lll11111_opy_(options, bstack11lll111_opy_):
  if not bstack11l1l11ll_opy_(options):
    return
  for bstack1l1llll1l_opy_ in bstack11lll111_opy_.keys():
    if bstack1l1llll1l_opy_ in bstack11l1l111l_opy_:
      next
    if bstack1l1llll1l_opy_ in options._caps and type(options._caps[bstack1l1llll1l_opy_]) in [dict, list]:
      options._caps[bstack1l1llll1l_opy_] = update(options._caps[bstack1l1llll1l_opy_], bstack11lll111_opy_[bstack1l1llll1l_opy_])
    else:
      options.set_capability(bstack1l1llll1l_opy_, bstack11lll111_opy_[bstack1l1llll1l_opy_])
  bstack11ll1111l_opy_(options, bstack11lll111_opy_)
  if bstack1ll1_opy_ (u"࠭࡭ࡰࡼ࠽ࡨࡪࡨࡵࡨࡩࡨࡶࡆࡪࡤࡳࡧࡶࡷࠬ୻") in options._caps:
    if options._caps[bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ୼")] and options._caps[bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭୽")].lower() != bstack1ll1_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪ୾"):
      del options._caps[bstack1ll1_opy_ (u"ࠪࡱࡴࢀ࠺ࡥࡧࡥࡹ࡬࡭ࡥࡳࡃࡧࡨࡷ࡫ࡳࡴࠩ୿")]
def bstack111111l1_opy_(proxy_config):
  if bstack1ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ஀") in proxy_config:
    proxy_config[bstack1ll1_opy_ (u"ࠬࡹࡳ࡭ࡒࡵࡳࡽࡿࠧ஁")] = proxy_config[bstack1ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪஂ")]
    del(proxy_config[bstack1ll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫஃ")])
  if bstack1ll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫ஄") in proxy_config and proxy_config[bstack1ll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬஅ")].lower() != bstack1ll1_opy_ (u"ࠪࡨ࡮ࡸࡥࡤࡶࠪஆ"):
    proxy_config[bstack1ll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧஇ")] = bstack1ll1_opy_ (u"ࠬࡳࡡ࡯ࡷࡤࡰࠬஈ")
  if bstack1ll1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡆࡻࡴࡰࡥࡲࡲ࡫࡯ࡧࡖࡴ࡯ࠫஉ") in proxy_config:
    proxy_config[bstack1ll1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪஊ")] = bstack1ll1_opy_ (u"ࠨࡲࡤࡧࠬ஋")
  return proxy_config
def bstack11l11_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1ll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨ஌") in config:
    return proxy
  config[bstack1ll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩ஍")] = bstack111111l1_opy_(config[bstack1ll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪஎ")])
  if proxy == None:
    proxy = Proxy(config[bstack1ll1_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫஏ")])
  return proxy
def bstack1l1l1llll_opy_(self):
  global CONFIG
  global bstack1l1l1l1l_opy_
  try:
    proxy = bstack11l1l_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1ll1_opy_ (u"࠭࠮ࡱࡣࡦࠫஐ")):
        proxies = bstack1l1ll1l1_opy_(proxy, bstack11lllll1_opy_())
        if len(proxies) > 0:
          protocol, bstack1ll11111l_opy_ = proxies.popitem()
          if bstack1ll1_opy_ (u"ࠢ࠻࠱࠲ࠦ஑") in bstack1ll11111l_opy_:
            return bstack1ll11111l_opy_
          else:
            return bstack1ll1_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤஒ") + bstack1ll11111l_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1ll1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡶࡲࡰࡺࡼࠤࡺࡸ࡬ࠡ࠼ࠣࡿࢂࠨஓ").format(str(e)))
  return bstack1l1l1l1l_opy_(self)
def bstack11ll111ll_opy_():
  global CONFIG
  return bstack1ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ஔ") in CONFIG or bstack1ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨக") in CONFIG
def bstack11l1l_opy_(config):
  if not bstack11ll111ll_opy_():
    return
  if config.get(bstack1ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ஖")):
    return config.get(bstack1ll1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ஗"))
  if config.get(bstack1ll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ஘")):
    return config.get(bstack1ll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬங"))
def bstack1l1l1ll11_opy_(url):
  try:
      result = urlparse(url)
      return all([result.scheme, result.netloc])
  except:
      return False
def bstack111l1ll_opy_(bstack11l11l111_opy_, bstack1ll1ll111_opy_):
  from pypac import get_pac
  from pypac import PACSession
  from pypac.parser import PACFile
  import socket
  if os.path.isfile(bstack11l11l111_opy_):
    with open(bstack11l11l111_opy_) as f:
      pac = PACFile(f.read())
  elif bstack1l1l1ll11_opy_(bstack11l11l111_opy_):
    pac = get_pac(url=bstack11l11l111_opy_)
  else:
    raise Exception(bstack1ll1_opy_ (u"ࠩࡓࡥࡨࠦࡦࡪ࡮ࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠿ࠦࡻࡾࠩச").format(bstack11l11l111_opy_))
  session = PACSession(pac)
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((bstack1ll1_opy_ (u"ࠥ࠼࠳࠾࠮࠹࠰࠻ࠦ஛"), 80))
    bstack1l11l1ll_opy_ = s.getsockname()[0]
    s.close()
  except:
    bstack1l11l1ll_opy_ = bstack1ll1_opy_ (u"ࠫ࠵࠴࠰࠯࠲࠱࠴ࠬஜ")
  proxy_url = session.get_pac().find_proxy_for_url(bstack1ll1ll111_opy_, bstack1l11l1ll_opy_)
  return proxy_url
def bstack1l1ll1l1_opy_(bstack11l11l111_opy_, bstack1ll1ll111_opy_):
  proxies = {}
  global bstack1llll1_opy_
  if bstack1ll1_opy_ (u"ࠬࡖࡁࡄࡡࡓࡖࡔ࡞࡙ࠨ஝") in globals():
    return bstack1llll1_opy_
  try:
    proxy = bstack111l1ll_opy_(bstack11l11l111_opy_,bstack1ll1ll111_opy_)
    if bstack1ll1_opy_ (u"ࠨࡄࡊࡔࡈࡇ࡙ࠨஞ") in proxy:
      proxies = {}
    elif bstack1ll1_opy_ (u"ࠢࡉࡖࡗࡔࠧட") in proxy or bstack1ll1_opy_ (u"ࠣࡊࡗࡘࡕ࡙ࠢ஠") in proxy or bstack1ll1_opy_ (u"ࠤࡖࡓࡈࡑࡓࠣ஡") in proxy:
      bstack1ll11llll_opy_ = proxy.split(bstack1ll1_opy_ (u"ࠥࠤࠧ஢"))
      if bstack1ll1_opy_ (u"ࠦ࠿࠵࠯ࠣண") in bstack1ll1_opy_ (u"ࠧࠨத").join(bstack1ll11llll_opy_[1:]):
        proxies = {
          bstack1ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬ஥"): bstack1ll1_opy_ (u"ࠢࠣ஦").join(bstack1ll11llll_opy_[1:])
        }
      else:
        proxies = {
          bstack1ll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ஧") : str(bstack1ll11llll_opy_[0]).lower()+ bstack1ll1_opy_ (u"ࠤ࠽࠳࠴ࠨந") + bstack1ll1_opy_ (u"ࠥࠦன").join(bstack1ll11llll_opy_[1:])
        }
    elif bstack1ll1_opy_ (u"ࠦࡕࡘࡏ࡙࡛ࠥப") in proxy:
      bstack1ll11llll_opy_ = proxy.split(bstack1ll1_opy_ (u"ࠧࠦࠢ஫"))
      if bstack1ll1_opy_ (u"ࠨ࠺࠰࠱ࠥ஬") in bstack1ll1_opy_ (u"ࠢࠣ஭").join(bstack1ll11llll_opy_[1:]):
        proxies = {
          bstack1ll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧம"): bstack1ll1_opy_ (u"ࠤࠥய").join(bstack1ll11llll_opy_[1:])
        }
      else:
        proxies = {
          bstack1ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩர"): bstack1ll1_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧற") + bstack1ll1_opy_ (u"ࠧࠨல").join(bstack1ll11llll_opy_[1:])
        }
    else:
      proxies = {
        bstack1ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬள"): proxy
      }
  except Exception as e:
    logger.error(bstack11lllll1l_opy_.format(bstack11l11l111_opy_, str(e)))
  bstack1llll1_opy_ = proxies
  return proxies
def bstack1lll11l11_opy_(config, bstack1ll1ll111_opy_):
  proxy = bstack11l1l_opy_(config)
  proxies = {}
  if config.get(bstack1ll1_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪழ")) or config.get(bstack1ll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬவ")):
    if proxy.endswith(bstack1ll1_opy_ (u"ࠩ࠱ࡴࡦࡩࠧஶ")):
      proxies = bstack1l1ll1l1_opy_(proxy,bstack1ll1ll111_opy_)
    else:
      proxies = {
        bstack1ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩஷ"): proxy
      }
  return proxies
def bstack11l11l1_opy_():
  return bstack11ll111ll_opy_() and bstack1lll1111_opy_() >= version.parse(bstack1l11ll1l_opy_)
def bstack11ll11111_opy_(config):
  bstack1l1l11l_opy_ = {}
  if bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨஸ") in config:
    bstack1l1l11l_opy_ =  config[bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩஹ")]
  if bstack1ll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ஺") in config:
    bstack1l1l11l_opy_ = config[bstack1ll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭஻")]
  proxy = bstack11l1l_opy_(config)
  if proxy:
    if proxy.endswith(bstack1ll1_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭஼")) and os.path.isfile(proxy):
      bstack1l1l11l_opy_[bstack1ll1_opy_ (u"ࠩ࠰ࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬ஽")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1ll1_opy_ (u"ࠪ࠲ࡵࡧࡣࠨா")):
        proxies = bstack1lll11l11_opy_(config, bstack11lllll1_opy_())
        if len(proxies) > 0:
          protocol, bstack1ll11111l_opy_ = proxies.popitem()
          if bstack1ll1_opy_ (u"ࠦ࠿࠵࠯ࠣி") in bstack1ll11111l_opy_:
            parsed_url = urlparse(bstack1ll11111l_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1ll1_opy_ (u"ࠧࡀ࠯࠰ࠤீ") + bstack1ll11111l_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1l1l11l_opy_[bstack1ll1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡍࡵࡳࡵࠩு")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1l1l11l_opy_[bstack1ll1_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖ࡯ࡳࡶࠪூ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1l1l11l_opy_[bstack1ll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡕࡴࡧࡵࠫ௃")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1l1l11l_opy_[bstack1ll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬ௄")] = str(parsed_url.password)
  return bstack1l1l11l_opy_
def bstack1l1l111ll_opy_(config):
  if bstack1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨ௅") in config:
    return config[bstack1ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩெ")]
  return {}
def bstack1l1l1l1ll_opy_(caps):
  global bstack11ll111l1_opy_
  if bstack1ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ே") in caps:
    caps[bstack1ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧை")][bstack1ll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭௉")] = True
    if bstack11ll111l1_opy_:
      caps[bstack1ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩொ")][bstack1ll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫோ")] = bstack11ll111l1_opy_
  else:
    caps[bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨௌ")] = True
    if bstack11ll111l1_opy_:
      caps[bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ்ࠬ")] = bstack11ll111l1_opy_
def bstack1111llll_opy_():
  global CONFIG
  if bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ௎") in CONFIG and CONFIG[bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ௏")]:
    bstack1l1l11l_opy_ = bstack11ll11111_opy_(CONFIG)
    bstack1lllll1l_opy_(CONFIG[bstack1ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪௐ")], bstack1l1l11l_opy_)
def bstack1lllll1l_opy_(key, bstack1l1l11l_opy_):
  global bstack1ll111l1_opy_
  logger.info(bstack11ll11l1_opy_)
  try:
    bstack1ll111l1_opy_ = Local()
    bstack11ll1111_opy_ = {bstack1ll1_opy_ (u"ࠨ࡭ࡨࡽࠬ௑"): key}
    bstack11ll1111_opy_.update(bstack1l1l11l_opy_)
    logger.debug(bstack1l11ll1_opy_.format(str(bstack11ll1111_opy_)))
    bstack1ll111l1_opy_.start(**bstack11ll1111_opy_)
    if bstack1ll111l1_opy_.isRunning():
      logger.info(bstack111l1_opy_)
  except Exception as e:
    bstack11ll1l11l_opy_(bstack11l111111_opy_.format(str(e)))
def bstack11lll11l_opy_():
  global bstack1ll111l1_opy_
  if bstack1ll111l1_opy_.isRunning():
    logger.info(bstack1ll111l1l_opy_)
    bstack1ll111l1_opy_.stop()
  bstack1ll111l1_opy_ = None
def bstack1l1l1_opy_(bstack1lllll1l1_opy_=[]):
  global CONFIG
  bstack11l111lll_opy_ = []
  bstack1l111l11_opy_ = [bstack1ll1_opy_ (u"ࠩࡲࡷࠬ௒"), bstack1ll1_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭௓"), bstack1ll1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨ௔"), bstack1ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ௕"), bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ௖"), bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨௗ")]
  try:
    for err in bstack1lllll1l1_opy_:
      bstack1ll1ll_opy_ = {}
      for k in bstack1l111l11_opy_:
        val = CONFIG[bstack1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ௘")][int(err[bstack1ll1_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ௙")])].get(k)
        if val:
          bstack1ll1ll_opy_[k] = val
      bstack1ll1ll_opy_[bstack1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡴࠩ௚")] = {
        err[bstack1ll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ௛")]: err[bstack1ll1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ௜")]
      }
      bstack11l111lll_opy_.append(bstack1ll1ll_opy_)
  except Exception as e:
    logger.debug(bstack1ll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡨࡲࡶࡲࡧࡴࡵ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡀࠠࠨ௝") +str(e))
  finally:
    return bstack11l111lll_opy_
def bstack11l1ll11_opy_():
  global bstack11l1l1ll1_opy_
  global bstack11l1111l_opy_
  global bstack111lll_opy_
  if bstack11l1l1ll1_opy_:
    logger.warning(bstack11llll1l1_opy_.format(str(bstack11l1l1ll1_opy_)))
  logger.info(bstack1l1ll111_opy_)
  global bstack1ll111l1_opy_
  if bstack1ll111l1_opy_:
    bstack11lll11l_opy_()
  try:
    for driver in bstack11l1111l_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1l1l1ll1l_opy_)
  bstack11lll1ll1_opy_()
  if len(bstack111lll_opy_) > 0:
    message = bstack1l1l1_opy_(bstack111lll_opy_)
    bstack11lll1ll1_opy_(message)
  else:
    bstack11lll1ll1_opy_()
def bstack1111_opy_(self, *args):
  logger.error(bstack11llllll1_opy_)
  bstack11l1ll11_opy_()
  sys.exit(1)
def bstack11ll1l11l_opy_(err):
  logger.critical(bstack1llllll_opy_.format(str(err)))
  bstack11lll1ll1_opy_(bstack1llllll_opy_.format(str(err)))
  atexit.unregister(bstack11l1ll11_opy_)
  sys.exit(1)
def bstack11ll1l11_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack11lll1ll1_opy_(message)
  atexit.unregister(bstack11l1ll11_opy_)
  sys.exit(1)
def bstack1ll1l111_opy_():
  global CONFIG
  global bstack11ll1l111_opy_
  global bstack1ll1l1l1l_opy_
  global bstack1111ll1_opy_
  CONFIG = bstack111ll1_opy_()
  bstack11ll111_opy_()
  bstack11ll1llll_opy_()
  CONFIG = bstack1l1l1l11_opy_(CONFIG)
  update(CONFIG, bstack1ll1l1l1l_opy_)
  update(CONFIG, bstack11ll1l111_opy_)
  CONFIG = bstack1lllll1ll_opy_(CONFIG)
  if bstack1ll1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ௞") in CONFIG and str(CONFIG[bstack1ll1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ௟")]).lower() == bstack1ll1_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ௠"):
    bstack1111ll1_opy_ = False
  if (bstack1ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭௡") in CONFIG and bstack1ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ௢") in bstack11ll1l111_opy_) or (bstack1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ௣") in CONFIG and bstack1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ௤") not in bstack1ll1l1l1l_opy_):
    if os.getenv(bstack1ll1_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫ௥")):
      CONFIG[bstack1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ௦")] = os.getenv(bstack1ll1_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭௧"))
    else:
      bstack1111l1ll_opy_()
  elif (bstack1ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭௨") not in CONFIG and bstack1ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭௩") in CONFIG) or (bstack1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ௪") in bstack1ll1l1l1l_opy_ and bstack1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ௫") not in bstack11ll1l111_opy_):
    del(CONFIG[bstack1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ௬")])
  if bstack1l1l1lll_opy_(CONFIG):
    bstack11ll1l11l_opy_(bstack1ll11l_opy_)
  bstack1l1l1lll1_opy_()
  bstack1l111l1_opy_()
  if bstack1ll1ll1l_opy_:
    CONFIG[bstack1ll1_opy_ (u"ࠨࡣࡳࡴࠬ௭")] = bstack1ll1l1l1_opy_(CONFIG)
    logger.info(bstack1ll1ll11_opy_.format(CONFIG[bstack1ll1_opy_ (u"ࠩࡤࡴࡵ࠭௮")]))
def bstack1l111l1_opy_():
  global CONFIG
  global bstack1ll1ll1l_opy_
  if bstack1ll1_opy_ (u"ࠪࡥࡵࡶࠧ௯") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack11ll1l11_opy_(e, bstack1l1lll11l_opy_)
    bstack1ll1ll1l_opy_ = True
def bstack1ll1l1l1_opy_(config):
  bstack11l111ll_opy_ = bstack1ll1_opy_ (u"ࠫࠬ௰")
  app = config[bstack1ll1_opy_ (u"ࠬࡧࡰࡱࠩ௱")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1l1111ll1_opy_:
      if os.path.exists(app):
        bstack11l111ll_opy_ = bstack111ll111_opy_(config, app)
      elif bstack1ll111ll_opy_(app):
        bstack11l111ll_opy_ = app
      else:
        bstack11ll1l11l_opy_(bstack1l11111l1_opy_.format(app))
    else:
      if bstack1ll111ll_opy_(app):
        bstack11l111ll_opy_ = app
      elif os.path.exists(app):
        bstack11l111ll_opy_ = bstack111ll111_opy_(app)
      else:
        bstack11ll1l11l_opy_(bstack11l11ll11_opy_)
  else:
    if len(app) > 2:
      bstack11ll1l11l_opy_(bstack11ll1_opy_)
    elif len(app) == 2:
      if bstack1ll1_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ௲") in app and bstack1ll1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪ௳") in app:
        if os.path.exists(app[bstack1ll1_opy_ (u"ࠨࡲࡤࡸ࡭࠭௴")]):
          bstack11l111ll_opy_ = bstack111ll111_opy_(config, app[bstack1ll1_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ௵")], app[bstack1ll1_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭௶")])
        else:
          bstack11ll1l11l_opy_(bstack1l11111l1_opy_.format(app))
      else:
        bstack11ll1l11l_opy_(bstack11ll1_opy_)
    else:
      for key in app:
        if key in bstack1l1l11l11_opy_:
          if key == bstack1ll1_opy_ (u"ࠫࡵࡧࡴࡩࠩ௷"):
            if os.path.exists(app[key]):
              bstack11l111ll_opy_ = bstack111ll111_opy_(config, app[key])
            else:
              bstack11ll1l11l_opy_(bstack1l11111l1_opy_.format(app))
          else:
            bstack11l111ll_opy_ = app[key]
        else:
          bstack11ll1l11l_opy_(bstack1l1ll1_opy_)
  return bstack11l111ll_opy_
def bstack1ll111ll_opy_(bstack11l111ll_opy_):
  import re
  bstack1llll11l1_opy_ = re.compile(bstack1ll1_opy_ (u"ࡷࠨ࡞࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭ࠨࠧ௸"))
  bstack1l111_opy_ = re.compile(bstack1ll1_opy_ (u"ࡸࠢ࡟࡝ࡤ࠱ࡿࡇ࡛࠭࠲࠰࠽ࡡࡥ࠮࡝࠯ࡠ࠮࠴ࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫࠦࠥ௹"))
  if bstack1ll1_opy_ (u"ࠧࡣࡵ࠽࠳࠴࠭௺") in bstack11l111ll_opy_ or re.fullmatch(bstack1llll11l1_opy_, bstack11l111ll_opy_) or re.fullmatch(bstack1l111_opy_, bstack11l111ll_opy_):
    return True
  else:
    return False
def bstack111ll111_opy_(config, path, bstack1ll1lll_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1ll1_opy_ (u"ࠨࡴࡥࠫ௻")).read()).hexdigest()
  bstack1l11llll_opy_ = bstack1l11l11l1_opy_(md5_hash)
  bstack11l111ll_opy_ = None
  if bstack1l11llll_opy_:
    logger.info(bstack111lll1l_opy_.format(bstack1l11llll_opy_, md5_hash))
    return bstack1l11llll_opy_
  bstack11l1l11l_opy_ = MultipartEncoder(
    fields={
        bstack1ll1_opy_ (u"ࠩࡩ࡭ࡱ࡫ࠧ௼"): (os.path.basename(path), open(os.path.abspath(path), bstack1ll1_opy_ (u"ࠪࡶࡧ࠭௽")), bstack1ll1_opy_ (u"ࠫࡹ࡫ࡸࡵ࠱ࡳࡰࡦ࡯࡮ࠨ௾")),
        bstack1ll1_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨ௿"): bstack1ll1lll_opy_
    }
  )
  response = requests.post(bstack1111l1_opy_, data=bstack11l1l11l_opy_,
                         headers={bstack1ll1_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬఀ"): bstack11l1l11l_opy_.content_type}, auth=(config[bstack1ll1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩఁ")], config[bstack1ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫం")]))
  try:
    res = json.loads(response.text)
    bstack11l111ll_opy_ = res[bstack1ll1_opy_ (u"ࠩࡤࡴࡵࡥࡵࡳ࡮ࠪః")]
    logger.info(bstack111ll1ll1_opy_.format(bstack11l111ll_opy_))
    bstack1l1lll1ll_opy_(md5_hash, bstack11l111ll_opy_)
  except ValueError as err:
    bstack11ll1l11l_opy_(bstack1ll11_opy_.format(str(err)))
  return bstack11l111ll_opy_
def bstack1l1l1lll1_opy_():
  global CONFIG
  global bstack11l1l1l11_opy_
  bstack1ll11l1_opy_ = 0
  bstack1lll1l111_opy_ = 1
  if bstack1ll1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪఄ") in CONFIG:
    bstack1lll1l111_opy_ = CONFIG[bstack1ll1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫఅ")]
  if bstack1ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨఆ") in CONFIG:
    bstack1ll11l1_opy_ = len(CONFIG[bstack1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩఇ")])
  bstack11l1l1l11_opy_ = int(bstack1lll1l111_opy_) * int(bstack1ll11l1_opy_)
def bstack1l11l11l1_opy_(md5_hash):
  bstack1l11ll11_opy_ = os.path.join(os.path.expanduser(bstack1ll1_opy_ (u"ࠧࡿࠩఈ")), bstack1ll1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨఉ"), bstack1ll1_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪఊ"))
  if os.path.exists(bstack1l11ll11_opy_):
    bstack11ll11l11_opy_ = json.load(open(bstack1l11ll11_opy_,bstack1ll1_opy_ (u"ࠪࡶࡧ࠭ఋ")))
    if md5_hash in bstack11ll11l11_opy_:
      bstack1l1llll11_opy_ = bstack11ll11l11_opy_[md5_hash]
      bstack1111ll1l_opy_ = datetime.datetime.now()
      bstack1l111111l_opy_ = datetime.datetime.strptime(bstack1l1llll11_opy_[bstack1ll1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧఌ")], bstack1ll1_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩ఍"))
      if (bstack1111ll1l_opy_ - bstack1l111111l_opy_).days > 60:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1l1llll11_opy_[bstack1ll1_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫఎ")]):
        return None
      return bstack1l1llll11_opy_[bstack1ll1_opy_ (u"ࠧࡪࡦࠪఏ")]
  else:
    return None
def bstack1l1lll1ll_opy_(md5_hash, bstack11l111ll_opy_):
  bstack111ll1l1_opy_ = os.path.join(os.path.expanduser(bstack1ll1_opy_ (u"ࠨࢀࠪఐ")), bstack1ll1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ఑"))
  if not os.path.exists(bstack111ll1l1_opy_):
    os.makedirs(bstack111ll1l1_opy_)
  bstack1l11ll11_opy_ = os.path.join(os.path.expanduser(bstack1ll1_opy_ (u"ࠪࢂࠬఒ")), bstack1ll1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫఓ"), bstack1ll1_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭ఔ"))
  bstack1l11l11_opy_ = {
    bstack1ll1_opy_ (u"࠭ࡩࡥࠩక"): bstack11l111ll_opy_,
    bstack1ll1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪఖ"): datetime.datetime.strftime(datetime.datetime.now(), bstack1ll1_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬగ")),
    bstack1ll1_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧఘ"): str(__version__)
  }
  if os.path.exists(bstack1l11ll11_opy_):
    bstack11ll11l11_opy_ = json.load(open(bstack1l11ll11_opy_,bstack1ll1_opy_ (u"ࠪࡶࡧ࠭ఙ")))
  else:
    bstack11ll11l11_opy_ = {}
  bstack11ll11l11_opy_[md5_hash] = bstack1l11l11_opy_
  with open(bstack1l11ll11_opy_, bstack1ll1_opy_ (u"ࠦࡼ࠱ࠢచ")) as outfile:
    json.dump(bstack11ll11l11_opy_, outfile)
def bstack1l1l11l1l_opy_(self):
  return
def bstack1llll1ll_opy_(self):
  return
def bstack11ll11l1l_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack111lll111_opy_(self, command_executor,
        desired_capabilities=None, browser_profile=None, proxy=None,
        keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1lll1111l_opy_
  global bstack1l1111lll_opy_
  global bstack11l1ll1ll_opy_
  global bstack1l1ll11_opy_
  global bstack11ll1ll_opy_
  global bstack1ll1l1ll_opy_
  global bstack1111l1l1_opy_
  global bstack11l1111l_opy_
  global bstack111ll1l_opy_
  CONFIG[bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧఛ")] = str(bstack1ll1l1ll_opy_) + str(__version__)
  command_executor = bstack11lllll1_opy_()
  logger.debug(bstack111ll11_opy_.format(command_executor))
  proxy = bstack11l11_opy_(CONFIG, proxy)
  bstack111l11l_opy_ = 0 if bstack1l1111lll_opy_ < 0 else bstack1l1111lll_opy_
  if bstack1l1ll11_opy_ is True:
    bstack111l11l_opy_ = int(multiprocessing.current_process().name)
  if bstack11ll1ll_opy_ is True:
    bstack111l11l_opy_ = int(str(threading.current_thread().name).split(bstack1ll1_opy_ (u"࠭࡟ࡣࡵࡷࡥࡨࡱ࡟ࠨజ"))[0])
  bstack11lll111_opy_ = bstack1lll1_opy_(CONFIG, bstack111l11l_opy_)
  logger.debug(bstack1l11ll11l_opy_.format(str(bstack11lll111_opy_)))
  if bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫఝ") in CONFIG and CONFIG[bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬఞ")]:
    bstack1l1l1l1ll_opy_(bstack11lll111_opy_)
  if desired_capabilities:
    bstack1l1111l_opy_ = bstack1l1l1l11_opy_(desired_capabilities)
    bstack1l1111l_opy_[bstack1ll1_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩట")] = bstack11ll1ll1_opy_(CONFIG)
    bstack1ll11l11_opy_ = bstack1lll1_opy_(bstack1l1111l_opy_)
    if bstack1ll11l11_opy_:
      bstack11lll111_opy_ = update(bstack1ll11l11_opy_, bstack11lll111_opy_)
    desired_capabilities = None
  if options:
    bstack1lll11111_opy_(options, bstack11lll111_opy_)
  if not options:
    options = bstack1l11l1111_opy_(bstack11lll111_opy_)
  if proxy and bstack1lll1111_opy_() >= version.parse(bstack1ll1_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪఠ")):
    options.proxy(proxy)
  if options and bstack1lll1111_opy_() >= version.parse(bstack1ll1_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪడ")):
    desired_capabilities = None
  if (
      not options and not desired_capabilities
  ) or (
      bstack1lll1111_opy_() < version.parse(bstack1ll1_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫఢ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack11lll111_opy_)
  logger.info(bstack11lll1lll_opy_)
  if bstack1lll1111_opy_() >= version.parse(bstack1ll1_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ణ")):
    bstack1111l1l1_opy_(self, command_executor=command_executor,
          options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1lll1111_opy_() >= version.parse(bstack1ll1_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭త")):
    bstack1111l1l1_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities, options=options,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1lll1111_opy_() >= version.parse(bstack1ll1_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨథ")):
    bstack1111l1l1_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1111l1l1_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive)
  try:
    bstack111ll1lll_opy_ = bstack1ll1_opy_ (u"ࠩࠪద")
    if bstack1lll1111_opy_() >= version.parse(bstack1ll1_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࡤ࠴ࠫధ")):
      bstack111ll1lll_opy_ = self.caps.get(bstack1ll1_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦన"))
    else:
      bstack111ll1lll_opy_ = self.capabilities.get(bstack1ll1_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧ఩"))
    if bstack111ll1lll_opy_:
      if bstack1lll1111_opy_() <= version.parse(bstack1ll1_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭ప")):
        self.command_executor._url = bstack1ll1_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣఫ") + bstack11l11lll1_opy_ + bstack1ll1_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧబ")
      else:
        self.command_executor._url = bstack1ll1_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦభ") + bstack111ll1lll_opy_ + bstack1ll1_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦమ")
      logger.debug(bstack111lll11l_opy_.format(bstack111ll1lll_opy_))
    else:
      logger.debug(bstack1ll1111_opy_.format(bstack1ll1_opy_ (u"ࠦࡔࡶࡴࡪ࡯ࡤࡰࠥࡎࡵࡣࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠧయ")))
  except Exception as e:
    logger.debug(bstack1ll1111_opy_.format(e))
  if bstack1ll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫర") in bstack1ll1l1ll_opy_:
    bstack1111l1l_opy_(bstack1l1111lll_opy_, bstack111ll1l_opy_)
  bstack1lll1111l_opy_ = self.session_id
  if bstack1ll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ఱ") in bstack1ll1l1ll_opy_:
    current_name = threading.current_thread().name
    new_name = current_name + bstack1ll1_opy_ (u"ࠧࡠࡤࡶࡸࡦࡩ࡫ࡠࠩల") + self.session_id
    threading.current_thread().name = new_name
  bstack11l1111l_opy_.append(self)
  if bstack1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫళ") in CONFIG and bstack1ll1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧఴ") in CONFIG[bstack1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭వ")][bstack111l11l_opy_]:
    bstack11l1ll1ll_opy_ = CONFIG[bstack1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧశ")][bstack111l11l_opy_][bstack1ll1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪష")]
  logger.debug(bstack1lll11l1l_opy_.format(bstack1lll1111l_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1llllll1l_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1lll1lll_opy_
      if(bstack1ll1_opy_ (u"ࠨࡩ࡯ࡦࡨࡼ࠳ࡰࡳࠣస") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1ll1_opy_ (u"ࠧࡿࠩహ")), bstack1ll1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ఺"), bstack1ll1_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫ఻")), bstack1ll1_opy_ (u"ࠪࡻ఼ࠬ")) as fp:
          fp.write(bstack1ll1_opy_ (u"ࠦࠧఽ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1ll1_opy_ (u"ࠧ࡯࡮ࡥࡧࡻࡣࡧࡹࡴࡢࡥ࡮࠲࡯ࡹࠢా")))):
          with open(args[1], bstack1ll1_opy_ (u"࠭ࡲࠨి")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1ll1_opy_ (u"ࠧࡢࡵࡼࡲࡨࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡡࡱࡩࡼࡖࡡࡨࡧࠫࡧࡴࡴࡴࡦࡺࡷ࠰ࠥࡶࡡࡨࡧࠣࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮࠭ీ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack11lll11ll_opy_)
            lines.insert(1, bstack1l1ll1l1l_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1ll1_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥు")), bstack1ll1_opy_ (u"ࠩࡺࠫూ")) as bstack11l1l11l1_opy_:
              bstack11l1l11l1_opy_.writelines(lines)
        CONFIG[bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬృ")] = str(bstack1ll1l1ll_opy_) + str(__version__)
        bstack111l11l_opy_ = 0 if bstack1l1111lll_opy_ < 0 else bstack1l1111lll_opy_
        if bstack1l1ll11_opy_ is True:
          bstack111l11l_opy_ = int(threading.current_thread().getName())
        CONFIG[bstack1ll1_opy_ (u"ࠦࡺࡹࡥࡘ࠵ࡆࠦౄ")] = False
        CONFIG[bstack1ll1_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦ౅")] = True
        bstack11lll111_opy_ = bstack1lll1_opy_(CONFIG, bstack111l11l_opy_)
        logger.debug(bstack1l11ll11l_opy_.format(str(bstack11lll111_opy_)))
        if CONFIG[bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪె")]:
          bstack1l1l1l1ll_opy_(bstack11lll111_opy_)
        if bstack1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪే") in CONFIG and bstack1ll1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ై") in CONFIG[bstack1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ౉")][bstack111l11l_opy_]:
          bstack11l1ll1ll_opy_ = CONFIG[bstack1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ొ")][bstack111l11l_opy_][bstack1ll1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩో")]
        args.append(os.path.join(os.path.expanduser(bstack1ll1_opy_ (u"ࠬࢄࠧౌ")), bstack1ll1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ్࠭"), bstack1ll1_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩ౎")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack11lll111_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1ll1_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥ౏"))
      bstack1lll1lll_opy_ = True
      return bstack11l1lll1l_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1ll111ll1_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack1lll1111l_opy_
    global bstack1l1111lll_opy_
    global bstack11l1ll1ll_opy_
    global bstack1l1ll11_opy_
    global bstack1ll1l1ll_opy_
    global bstack1111l1l1_opy_
    CONFIG[bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ౐")] = str(bstack1ll1l1ll_opy_) + str(__version__)
    bstack111l11l_opy_ = 0 if bstack1l1111lll_opy_ < 0 else bstack1l1111lll_opy_
    if bstack1l1ll11_opy_ is True:
      bstack111l11l_opy_ = int(threading.current_thread().getName())
    CONFIG[bstack1ll1_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤ౑")] = True
    bstack11lll111_opy_ = bstack1lll1_opy_(CONFIG, bstack111l11l_opy_)
    logger.debug(bstack1l11ll11l_opy_.format(str(bstack11lll111_opy_)))
    if CONFIG[bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ౒")]:
      bstack1l1l1l1ll_opy_(bstack11lll111_opy_)
    if bstack1ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ౓") in CONFIG and bstack1ll1_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ౔") in CONFIG[bstack1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵౕࠪ")][bstack111l11l_opy_]:
      bstack11l1ll1ll_opy_ = CONFIG[bstack1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶౖࠫ")][bstack111l11l_opy_][bstack1ll1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ౗")]
    import urllib
    import json
    bstack11ll1lll_opy_ = bstack1ll1_opy_ (u"ࠪࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠬౘ") + urllib.parse.quote(json.dumps(bstack11lll111_opy_))
    browser = self.connect(bstack11ll1lll_opy_)
    return browser
except Exception as e:
    pass
def bstack1llll_opy_():
    global bstack1lll1lll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1ll111ll1_opy_
        bstack1lll1lll_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1llllll1l_opy_
      bstack1lll1lll_opy_ = True
    except Exception as e:
      pass
def bstack1ll11lll1_opy_(context, bstack11ll1ll11_opy_):
  try:
    context.page.evaluate(bstack1ll1_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧౙ"), bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠩౚ")+ json.dumps(bstack11ll1ll11_opy_) + bstack1ll1_opy_ (u"ࠨࡽࡾࠤ౛"))
  except Exception as e:
    logger.debug(bstack1ll1_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢࡾࢁࠧ౜"), e)
def bstack1ll11lll_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1ll1_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤౝ"), bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ౞") + json.dumps(message) + bstack1ll1_opy_ (u"ࠪ࠰ࠧࡲࡥࡷࡧ࡯ࠦ࠿࠭౟") + json.dumps(level) + bstack1ll1_opy_ (u"ࠫࢂࢃࠧౠ"))
  except Exception as e:
    logger.debug(bstack1ll1_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠥࢁࡽࠣౡ"), e)
def bstack1llll1l_opy_(context, status, message = bstack1ll1_opy_ (u"ࠨࠢౢ")):
  try:
    if(status == bstack1ll1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢౣ")):
      context.page.evaluate(bstack1ll1_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ౤"), bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡴࡨࡥࡸࡵ࡮ࠣ࠼ࠪ౥") + json.dumps(bstack1ll1_opy_ (u"ࠥࡗࡨ࡫࡮ࡢࡴ࡬ࡳࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࠧ౦") + str(message)) + bstack1ll1_opy_ (u"ࠫ࠱ࠨࡳࡵࡣࡷࡹࡸࠨ࠺ࠨ౧") + json.dumps(status) + bstack1ll1_opy_ (u"ࠧࢃࡽࠣ౨"))
    else:
      context.page.evaluate(bstack1ll1_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢ౩"), bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡳࡵࡣࡷࡹࡸࠨ࠺ࠨ౪") + json.dumps(status) + bstack1ll1_opy_ (u"ࠣࡿࢀࠦ౫"))
  except Exception as e:
    logger.debug(bstack1ll1_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡿࢂࠨ౬"), e)
def bstack11l11l1l_opy_(self, url):
  global bstack1111l11l_opy_
  try:
    bstack1l11l_opy_(url)
  except Exception as err:
    logger.debug(bstack1l1l1111_opy_.format(str(err)))
  try:
    bstack1111l11l_opy_(self, url)
  except Exception as e:
    try:
      bstack11l11l11l_opy_ = str(e)
      if any(err_msg in bstack11l11l11l_opy_ for err_msg in bstack11ll1l1_opy_):
        bstack1l11l_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1l1l1111_opy_.format(str(err)))
    raise e
def bstack1ll111l11_opy_(self):
  global bstack11lll1l_opy_
  bstack11lll1l_opy_ = self
  return
def bstack1llll111_opy_(self, test):
  global CONFIG
  global bstack11lll1l_opy_
  global bstack1lll1111l_opy_
  global bstack11l1111ll_opy_
  global bstack11l1ll1ll_opy_
  global bstack1l11lll_opy_
  global bstack1llllllll_opy_
  global bstack11l1111l_opy_
  try:
    if not bstack1lll1111l_opy_:
      with open(os.path.join(os.path.expanduser(bstack1ll1_opy_ (u"ࠪࢂࠬ౭")), bstack1ll1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ౮"), bstack1ll1_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧ౯"))) as f:
        bstack1lllll1_opy_ = json.loads(bstack1ll1_opy_ (u"ࠨࡻࠣ౰") + f.read().strip() + bstack1ll1_opy_ (u"ࠧࠣࡺࠥ࠾ࠥࠨࡹࠣࠩ౱") + bstack1ll1_opy_ (u"ࠣࡿࠥ౲"))
        bstack1lll1111l_opy_ = bstack1lllll1_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack11l1111l_opy_:
    for driver in bstack11l1111l_opy_:
      if bstack1lll1111l_opy_ == driver.session_id:
        if test:
          bstack1ll1l1_opy_ = str(test.data)
        if not bstack11llllll_opy_ and bstack1ll1l1_opy_:
          bstack11l1l1l1_opy_ = {
            bstack1ll1_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩ౳"): bstack1ll1_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ౴"),
            bstack1ll1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ౵"): {
              bstack1ll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ౶"): bstack1ll1l1_opy_
            }
          }
          bstack1lll1l11l_opy_ = bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫ౷").format(json.dumps(bstack11l1l1l1_opy_))
          driver.execute_script(bstack1lll1l11l_opy_)
        if bstack11l1111ll_opy_:
          bstack1ll11l1l_opy_ = {
            bstack1ll1_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧ౸"): bstack1ll1_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪ౹"),
            bstack1ll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ౺"): {
              bstack1ll1_opy_ (u"ࠪࡨࡦࡺࡡࠨ౻"): bstack1ll1l1_opy_ + bstack1ll1_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭౼"),
              bstack1ll1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ౽"): bstack1ll1_opy_ (u"࠭ࡩ࡯ࡨࡲࠫ౾")
            }
          }
          bstack11l1l1l1_opy_ = {
            bstack1ll1_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧ౿"): bstack1ll1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫಀ"),
            bstack1ll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬಁ"): {
              bstack1ll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪಂ"): bstack1ll1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫಃ")
            }
          }
          if bstack11l1111ll_opy_.status == bstack1ll1_opy_ (u"ࠬࡖࡁࡔࡕࠪ಄"):
            bstack11l1llll_opy_ = bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫಅ").format(json.dumps(bstack1ll11l1l_opy_))
            driver.execute_script(bstack11l1llll_opy_)
            bstack1lll1l11l_opy_ = bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬಆ").format(json.dumps(bstack11l1l1l1_opy_))
            driver.execute_script(bstack1lll1l11l_opy_)
          elif bstack11l1111ll_opy_.status == bstack1ll1_opy_ (u"ࠨࡈࡄࡍࡑ࠭ಇ"):
            reason = bstack1ll1_opy_ (u"ࠤࠥಈ")
            bstack1l111ll11_opy_ = bstack1ll1l1_opy_ + bstack1ll1_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠫಉ")
            if bstack11l1111ll_opy_.message:
              reason = str(bstack11l1111ll_opy_.message)
              bstack1l111ll11_opy_ = bstack1l111ll11_opy_ + bstack1ll1_opy_ (u"ࠫࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠫಊ") + reason
            bstack1ll11l1l_opy_[bstack1ll1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨಋ")] = {
              bstack1ll1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬಌ"): bstack1ll1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭಍"),
              bstack1ll1_opy_ (u"ࠨࡦࡤࡸࡦ࠭ಎ"): bstack1l111ll11_opy_
            }
            bstack11l1l1l1_opy_[bstack1ll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬಏ")] = {
              bstack1ll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪಐ"): bstack1ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ಑"),
              bstack1ll1_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬಒ"): reason
            }
            bstack11l1llll_opy_ = bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫಓ").format(json.dumps(bstack1ll11l1l_opy_))
            driver.execute_script(bstack11l1llll_opy_)
            bstack1lll1l11l_opy_ = bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬಔ").format(json.dumps(bstack11l1l1l1_opy_))
            driver.execute_script(bstack1lll1l11l_opy_)
  elif bstack1lll1111l_opy_:
    try:
      data = {}
      bstack1ll1l1_opy_ = None
      if test:
        bstack1ll1l1_opy_ = str(test.data)
      if not bstack11llllll_opy_ and bstack1ll1l1_opy_:
        data[bstack1ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ಕ")] = bstack1ll1l1_opy_
      if bstack11l1111ll_opy_:
        if bstack11l1111ll_opy_.status == bstack1ll1_opy_ (u"ࠩࡓࡅࡘ࡙ࠧಖ"):
          data[bstack1ll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪಗ")] = bstack1ll1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫಘ")
        elif bstack11l1111ll_opy_.status == bstack1ll1_opy_ (u"ࠬࡌࡁࡊࡎࠪಙ"):
          data[bstack1ll1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ಚ")] = bstack1ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧಛ")
          if bstack11l1111ll_opy_.message:
            data[bstack1ll1_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨಜ")] = str(bstack11l1111ll_opy_.message)
      user = CONFIG[bstack1ll1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫಝ")]
      key = CONFIG[bstack1ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ಞ")]
      url = bstack1ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡳࡦࡵࡶ࡭ࡴࡴࡳ࠰ࡽࢀ࠲࡯ࡹ࡯࡯ࠩಟ").format(user, key, bstack1lll1111l_opy_)
      headers = {
        bstack1ll1_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫಠ"): bstack1ll1_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩಡ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1l11111l_opy_.format(str(e)))
  if bstack11lll1l_opy_:
    bstack1llllllll_opy_(bstack11lll1l_opy_)
  bstack1l11lll_opy_(self, test)
def bstack1l11l1l1l_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1l1l1l1_opy_
  bstack1l1l1l1_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack11l1111ll_opy_
  bstack11l1111ll_opy_ = self._test
def bstack1ll111l_opy_():
  global bstack11111_opy_
  try:
    if os.path.exists(bstack11111_opy_):
      os.remove(bstack11111_opy_)
  except Exception as e:
    logger.debug(bstack1ll1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪಢ") + str(e))
def bstack111ll1l1l_opy_():
  global bstack11111_opy_
  bstack11111ll1_opy_ = {}
  try:
    if not os.path.isfile(bstack11111_opy_):
      with open(bstack11111_opy_, bstack1ll1_opy_ (u"ࠨࡹࠪಣ")):
        pass
      with open(bstack11111_opy_, bstack1ll1_opy_ (u"ࠤࡺ࠯ࠧತ")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack11111_opy_):
      bstack11111ll1_opy_ = json.load(open(bstack11111_opy_, bstack1ll1_opy_ (u"ࠪࡶࡧ࠭ಥ")))
  except Exception as e:
    logger.debug(bstack1ll1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭ದ") + str(e))
  finally:
    return bstack11111ll1_opy_
def bstack1111l1l_opy_(platform_index, item_index):
  global bstack11111_opy_
  try:
    bstack11111ll1_opy_ = bstack111ll1l1l_opy_()
    bstack11111ll1_opy_[item_index] = platform_index
    with open(bstack11111_opy_, bstack1ll1_opy_ (u"ࠧࡽࠫࠣಧ")) as outfile:
      json.dump(bstack11111ll1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1ll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡹࡵ࡭ࡹ࡯࡮ࡨࠢࡷࡳࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫನ") + str(e))
def bstack11lllll_opy_(bstack11l111l1_opy_):
  global CONFIG
  bstack1lll1lll1_opy_ = bstack1ll1_opy_ (u"ࠧࠨ಩")
  if not bstack1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫಪ") in CONFIG:
    logger.info(bstack1ll1_opy_ (u"ࠩࡑࡳࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠡࡲࡤࡷࡸ࡫ࡤࠡࡷࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡲࡦࡲࡲࡶࡹࠦࡦࡰࡴࠣࡖࡴࡨ࡯ࡵࠢࡵࡹࡳ࠭ಫ"))
  try:
    platform = CONFIG[bstack1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ಬ")][bstack11l111l1_opy_]
    if bstack1ll1_opy_ (u"ࠫࡴࡹࠧಭ") in platform:
      bstack1lll1lll1_opy_ += str(platform[bstack1ll1_opy_ (u"ࠬࡵࡳࠨಮ")]) + bstack1ll1_opy_ (u"࠭ࠬࠡࠩಯ")
    if bstack1ll1_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪರ") in platform:
      bstack1lll1lll1_opy_ += str(platform[bstack1ll1_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫಱ")]) + bstack1ll1_opy_ (u"ࠩ࠯ࠤࠬಲ")
    if bstack1ll1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧಳ") in platform:
      bstack1lll1lll1_opy_ += str(platform[bstack1ll1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨ಴")]) + bstack1ll1_opy_ (u"ࠬ࠲ࠠࠨವ")
    if bstack1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨಶ") in platform:
      bstack1lll1lll1_opy_ += str(platform[bstack1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩಷ")]) + bstack1ll1_opy_ (u"ࠨ࠮ࠣࠫಸ")
    if bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧಹ") in platform:
      bstack1lll1lll1_opy_ += str(platform[bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ಺")]) + bstack1ll1_opy_ (u"ࠫ࠱ࠦࠧ಻")
    if bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ಼࠭") in platform:
      bstack1lll1lll1_opy_ += str(platform[bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧಽ")]) + bstack1ll1_opy_ (u"ࠧ࠭ࠢࠪಾ")
  except Exception as e:
    logger.debug(bstack1ll1_opy_ (u"ࠨࡕࡲࡱࡪࠦࡥࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡴࡶࡵ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡷ࡫ࡰࡰࡴࡷࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡵ࡮ࠨಿ") + str(e))
  finally:
    if bstack1lll1lll1_opy_[len(bstack1lll1lll1_opy_) - 2:] == bstack1ll1_opy_ (u"ࠩ࠯ࠤࠬೀ"):
      bstack1lll1lll1_opy_ = bstack1lll1lll1_opy_[:-2]
    return bstack1lll1lll1_opy_
def bstack1lllllll_opy_(path, bstack1lll1lll1_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1l1lll_opy_ = ET.parse(path)
    bstack1l111l1l_opy_ = bstack1l1lll_opy_.getroot()
    bstack11ll1l1l_opy_ = None
    for suite in bstack1l111l1l_opy_.iter(bstack1ll1_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩು")):
      if bstack1ll1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫೂ") in suite.attrib:
        suite.attrib[bstack1ll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪೃ")] += bstack1ll1_opy_ (u"࠭ࠠࠨೄ") + bstack1lll1lll1_opy_
        bstack11ll1l1l_opy_ = suite
    bstack1ll11ll11_opy_ = None
    for robot in bstack1l111l1l_opy_.iter(bstack1ll1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭೅")):
      bstack1ll11ll11_opy_ = robot
    bstack1l1ll11l_opy_ = len(bstack1ll11ll11_opy_.findall(bstack1ll1_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧೆ")))
    if bstack1l1ll11l_opy_ == 1:
      bstack1ll11ll11_opy_.remove(bstack1ll11ll11_opy_.findall(bstack1ll1_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨೇ"))[0])
      bstack11llll11_opy_ = ET.Element(bstack1ll1_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩೈ"), attrib={bstack1ll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ೉"):bstack1ll1_opy_ (u"࡙ࠬࡵࡪࡶࡨࡷࠬೊ"), bstack1ll1_opy_ (u"࠭ࡩࡥࠩೋ"):bstack1ll1_opy_ (u"ࠧࡴ࠲ࠪೌ")})
      bstack1ll11ll11_opy_.insert(1, bstack11llll11_opy_)
      bstack11ll1l1l1_opy_ = None
      for suite in bstack1ll11ll11_opy_.iter(bstack1ll1_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫್ࠧ")):
        bstack11ll1l1l1_opy_ = suite
      bstack11ll1l1l1_opy_.append(bstack11ll1l1l_opy_)
      bstack1ll1111l1_opy_ = None
      for status in bstack11ll1l1l_opy_.iter(bstack1ll1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ೎")):
        bstack1ll1111l1_opy_ = status
      bstack11ll1l1l1_opy_.append(bstack1ll1111l1_opy_)
    bstack1l1lll_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1ll1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡳࡵ࡬ࡲ࡬ࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠨ೏") + str(e))
def bstack1111ll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack111l1l_opy_
  global CONFIG
  if bstack1ll1_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨࠣ೐") in options:
    del options[bstack1ll1_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡵࡧࡴࡩࠤ೑")]
  bstack111ll11l_opy_ = bstack111ll1l1l_opy_()
  for bstack11lll_opy_ in bstack111ll11l_opy_.keys():
    path = os.path.join(os.getcwd(), bstack1ll1_opy_ (u"࠭ࡰࡢࡤࡲࡸࡤࡸࡥࡴࡷ࡯ࡸࡸ࠭೒"), str(bstack11lll_opy_), bstack1ll1_opy_ (u"ࠧࡰࡷࡷࡴࡺࡺ࠮ࡹ࡯࡯ࠫ೓"))
    bstack1lllllll_opy_(path, bstack11lllll_opy_(bstack111ll11l_opy_[bstack11lll_opy_]))
  bstack1ll111l_opy_()
  return bstack111l1l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1ll1ll11l_opy_(self, ff_profile_dir):
  global bstack11ll11l_opy_
  if not ff_profile_dir:
    return None
  return bstack11ll11l_opy_(self, ff_profile_dir)
def bstack11lll1l1l_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack11ll111l1_opy_
  bstack1l1l1l_opy_ = []
  if bstack1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ೔") in CONFIG:
    bstack1l1l1l_opy_ = CONFIG[bstack1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬೕ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1ll1_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦೖ")],
      pabot_args[bstack1ll1_opy_ (u"ࠦࡻ࡫ࡲࡣࡱࡶࡩࠧ೗")],
      argfile,
      pabot_args.get(bstack1ll1_opy_ (u"ࠧ࡮ࡩࡷࡧࠥ೘")),
      pabot_args[bstack1ll1_opy_ (u"ࠨࡰࡳࡱࡦࡩࡸࡹࡥࡴࠤ೙")],
      platform[0],
      bstack11ll111l1_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1ll1_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡨ࡬ࡰࡪࡹࠢ೚")] or [(bstack1ll1_opy_ (u"ࠣࠤ೛"), None)]
    for platform in enumerate(bstack1l1l1l_opy_)
  ]
def bstack111l111l_opy_(self, datasources, outs_dir, options,
  execution_item, command, verbose, argfile,
  hive=None, processes=0,platform_index=0,bstack1llll1l1l_opy_=bstack1ll1_opy_ (u"ࠩࠪ೜")):
  global bstack11lll1_opy_
  self.platform_index = platform_index
  self.bstack111lll1l1_opy_ = bstack1llll1l1l_opy_
  bstack11lll1_opy_(self, datasources, outs_dir, options,
    execution_item, command, verbose, argfile, hive, processes)
def bstack1ll1111l_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack111l111_opy_
  global bstack11111l_opy_
  if not bstack1ll1_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬೝ") in item.options:
    item.options[bstack1ll1_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ೞ")] = []
  for v in item.options[bstack1ll1_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ೟")]:
    if bstack1ll1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬೠ") in v:
      item.options[bstack1ll1_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩೡ")].remove(v)
    if bstack1ll1_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓࠨೢ") in v:
      item.options[bstack1ll1_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫೣ")].remove(v)
  item.options[bstack1ll1_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ೤")].insert(0, bstack1ll1_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚࠽ࡿࢂ࠭೥").format(item.platform_index))
  item.options[bstack1ll1_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ೦")].insert(0, bstack1ll1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔ࠽ࡿࢂ࠭೧").format(item.bstack111lll1l1_opy_))
  if bstack11111l_opy_:
    item.options[bstack1ll1_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ೨")].insert(0, bstack1ll1_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓ࠻ࡽࢀࠫ೩").format(bstack11111l_opy_))
  return bstack111l111_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack1l1l11ll1_opy_(command, item_index):
  global bstack11111l_opy_
  if bstack11111l_opy_:
    command[0] = command[0].replace(bstack1ll1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ೪"), bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠠ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽࠦࠧ೫") + str(item_index) + bstack11111l_opy_, 1)
  else:
    command[0] = command[0].replace(bstack1ll1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ೬"), bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡸࡪ࡫ࠡࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠢ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠡࠩ೭") + str(item_index), 1)
def bstack11l11llll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1lllll_opy_
  bstack1l1l11ll1_opy_(command, item_index)
  return bstack1lllll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack11l1lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1lllll_opy_
  bstack1l1l11ll1_opy_(command, item_index)
  return bstack1lllll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack111ll11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1lllll_opy_
  bstack1l1l11ll1_opy_(command, item_index)
  return bstack1lllll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack1ll1l11l_opy_(self, runner, quiet=False, capture=True):
  global bstack11l1111l1_opy_
  bstack11111111_opy_ = bstack11l1111l1_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack1ll1_opy_ (u"࠭ࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࡡࡤࡶࡷ࠭೮")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1ll1_opy_ (u"ࠧࡦࡺࡦࡣࡹࡸࡡࡤࡧࡥࡥࡨࡱ࡟ࡢࡴࡵࠫ೯")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack11111111_opy_
def bstack11l1ll1_opy_(self, name, context, *args):
  global bstack11llll111_opy_
  if name in [bstack1ll1_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠩ೰"), bstack1ll1_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫೱ")]:
    bstack11llll111_opy_(self, name, context, *args)
  if name == bstack1ll1_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠫೲ"):
    try:
      if(not bstack11llllll_opy_):
        bstack11ll1ll11_opy_ = str(self.feature.name)
        bstack1ll11lll1_opy_(context, bstack11ll1ll11_opy_)
        context.browser.execute_script(bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩೳ") + json.dumps(bstack11ll1ll11_opy_) + bstack1ll1_opy_ (u"ࠬࢃࡽࠨ೴"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack1ll1_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭೵").format(str(e)))
  if name == bstack1ll1_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩ೶"):
    try:
      if not hasattr(self, bstack1ll1_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࡠࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ೷")):
        self.driver_before_scenario = True
      if(not bstack11llllll_opy_):
        scenario_name = args[0].name
        feature_name = bstack11ll1ll11_opy_ = str(self.feature.name)
        bstack11ll1ll11_opy_ = feature_name + bstack1ll1_opy_ (u"ࠩࠣ࠱ࠥ࠭೸") + scenario_name
        if self.driver_before_scenario:
          bstack1ll11lll1_opy_(context, bstack11ll1ll11_opy_)
          context.browser.execute_script(bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨ೹") + json.dumps(bstack11ll1ll11_opy_) + bstack1ll1_opy_ (u"ࠫࢂࢃࠧ೺"))
    except Exception as e:
      logger.debug(bstack1ll1_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤ࡮ࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡥࡨࡲࡦࡸࡩࡰ࠼ࠣࡿࢂ࠭೻").format(str(e)))
  if name == bstack1ll1_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧ೼"):
    try:
      bstack1ll1l1l_opy_ = args[0].status.name
      if str(bstack1ll1l1l_opy_).lower() == bstack1ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ೽"):
        bstack1l1l11_opy_ = bstack1ll1_opy_ (u"ࠨࠩ೾")
        bstack1lll11l_opy_ = bstack1ll1_opy_ (u"ࠩࠪ೿")
        bstack11lll11l1_opy_ = bstack1ll1_opy_ (u"ࠪࠫഀ")
        try:
          import traceback
          bstack1l1l11_opy_ = self.exception.__class__.__name__
          bstack11111l1l_opy_ = traceback.format_tb(self.exc_traceback)
          bstack1lll11l_opy_ = bstack1ll1_opy_ (u"ࠫࠥ࠭ഁ").join(bstack11111l1l_opy_)
          bstack11lll11l1_opy_ = bstack11111l1l_opy_[-1]
        except Exception as e:
          logger.debug(bstack111111l_opy_.format(str(e)))
        bstack1l1l11_opy_ += bstack11lll11l1_opy_
        bstack1ll11lll_opy_(context, json.dumps(str(args[0].name) + bstack1ll1_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦം") + str(bstack1lll11l_opy_)), bstack1ll1_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧഃ"))
        if self.driver_before_scenario:
          bstack1llll1l_opy_(context, bstack1ll1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢഄ"), bstack1l1l11_opy_)
        context.browser.execute_script(bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭അ") + json.dumps(str(args[0].name) + bstack1ll1_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣആ") + str(bstack1lll11l_opy_)) + bstack1ll1_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪഇ"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ࠲ࠠࠣࡴࡨࡥࡸࡵ࡮ࠣ࠼ࠣࠫഈ") + json.dumps(bstack1ll1_opy_ (u"࡙ࠧࡣࡦࡰࡤࡶ࡮ࡵࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤഉ") + str(bstack1l1l11_opy_)) + bstack1ll1_opy_ (u"࠭ࡽࡾࠩഊ"))
      else:
        bstack1ll11lll_opy_(context, bstack1ll1_opy_ (u"ࠢࡑࡣࡶࡷࡪࡪࠡࠣഋ"), bstack1ll1_opy_ (u"ࠣ࡫ࡱࡪࡴࠨഌ"))
        if self.driver_before_scenario:
          bstack1llll1l_opy_(context, bstack1ll1_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ഍"))
        context.browser.execute_script(bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨഎ") + json.dumps(str(args[0].name) + bstack1ll1_opy_ (u"ࠦࠥ࠳ࠠࡑࡣࡶࡷࡪࡪࠡࠣഏ")) + bstack1ll1_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫഐ"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡹࡴࡢࡶࡸࡷࠧࡀࠢࡱࡣࡶࡷࡪࡪࠢࡾࡿࠪ഑"))
    except Exception as e:
      logger.debug(bstack1ll1_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩഒ").format(str(e)))
  if name == bstack1ll1_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨഓ"):
    try:
      if context.failed is True:
        bstack1lllll11l_opy_ = []
        bstack1lll1l_opy_ = []
        bstack1111lll1_opy_ = []
        bstack111llll_opy_ = bstack1ll1_opy_ (u"ࠩࠪഔ")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack1lllll11l_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack11111l1l_opy_ = traceback.format_tb(exc_tb)
            bstack111l1111_opy_ = bstack1ll1_opy_ (u"ࠪࠤࠬക").join(bstack11111l1l_opy_)
            bstack1lll1l_opy_.append(bstack111l1111_opy_)
            bstack1111lll1_opy_.append(bstack11111l1l_opy_[-1])
        except Exception as e:
          logger.debug(bstack111111l_opy_.format(str(e)))
        bstack1l1l11_opy_ = bstack1ll1_opy_ (u"ࠫࠬഖ")
        for i in range(len(bstack1lllll11l_opy_)):
          bstack1l1l11_opy_ += bstack1lllll11l_opy_[i] + bstack1111lll1_opy_[i] + bstack1ll1_opy_ (u"ࠬࡢ࡮ࠨഗ")
        bstack111llll_opy_ = bstack1ll1_opy_ (u"࠭ࠠࠨഘ").join(bstack1lll1l_opy_)
        if not self.driver_before_scenario:
          bstack1ll11lll_opy_(context, bstack111llll_opy_, bstack1ll1_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨങ"))
          bstack1llll1l_opy_(context, bstack1ll1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣച"), bstack1l1l11_opy_)
          context.browser.execute_script(bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧഛ") + json.dumps(bstack111llll_opy_) + bstack1ll1_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪജ"))
          context.browser.execute_script(bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ࠲ࠠࠣࡴࡨࡥࡸࡵ࡮ࠣ࠼ࠣࠫഝ") + json.dumps(bstack1ll1_opy_ (u"࡙ࠧ࡯࡮ࡧࠣࡷࡨ࡫࡮ࡢࡴ࡬ࡳࡸࠦࡦࡢ࡫࡯ࡩࡩࡀࠠ࡝ࡰࠥഞ") + str(bstack1l1l11_opy_)) + bstack1ll1_opy_ (u"࠭ࡽࡾࠩട"))
      else:
        if not self.driver_before_scenario:
          bstack1ll11lll_opy_(context, bstack1ll1_opy_ (u"ࠢࡇࡧࡤࡸࡺࡸࡥ࠻ࠢࠥഠ") + str(self.feature.name) + bstack1ll1_opy_ (u"ࠣࠢࡳࡥࡸࡹࡥࡥࠣࠥഡ"), bstack1ll1_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢഢ"))
          bstack1llll1l_opy_(context, bstack1ll1_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥണ"))
          context.browser.execute_script(bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩത") + json.dumps(bstack1ll1_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࡀࠠࠣഥ") + str(self.feature.name) + bstack1ll1_opy_ (u"ࠨࠠࡱࡣࡶࡷࡪࡪࠡࠣദ")) + bstack1ll1_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥࢁࢂ࠭ധ"))
          context.browser.execute_script(bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠤࡳࡥࡸࡹࡥࡥࠤࢀࢁࠬന"))
    except Exception as e:
      logger.debug(bstack1ll1_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫഩ").format(str(e)))
  if name in [bstack1ll1_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪപ"), bstack1ll1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬഫ")]:
    bstack11llll111_opy_(self, name, context, *args)
    if (name == bstack1ll1_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ബ") and self.driver_before_scenario) or (name == bstack1ll1_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ഭ") and not self.driver_before_scenario):
      try:
        context.browser.quit()
      except Exception:
        pass
def bstack111l11_opy_(config, startdir):
  return bstack1ll1_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࠳ࢁࠧമ").format(bstack1ll1_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢയ"))
class Notset:
  def __repr__(self):
    return bstack1ll1_opy_ (u"ࠤ࠿ࡒࡔ࡚ࡓࡆࡖࡁࠦര")
notset = Notset()
def bstack1lll1l1l1_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1ll1llll1_opy_
  if str(name).lower() == bstack1ll1_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪറ"):
    return bstack1ll1_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥല")
  else:
    return bstack1ll1llll1_opy_(self, name, default, skip)
def bstack1l1111l1_opy_(item, when):
  global bstack11llll1ll_opy_
  try:
    bstack11llll1ll_opy_(item, when)
  except Exception as e:
    pass
def bstack1l111l1l1_opy_():
  return
def bstack1llllll1_opy_(type, name, status, reason, bstack111111_opy_, bstack11l1lllll_opy_):
  bstack11l1l1l1_opy_ = {
    bstack1ll1_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬള"): type,
    bstack1ll1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩഴ"): {}
  }
  if type == bstack1ll1_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩവ"):
    bstack11l1l1l1_opy_[bstack1ll1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫശ")][bstack1ll1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨഷ")] = bstack111111_opy_
    bstack11l1l1l1_opy_[bstack1ll1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭സ")][bstack1ll1_opy_ (u"ࠫࡩࡧࡴࡢࠩഹ")] = json.dumps(str(bstack11l1lllll_opy_))
  if type == bstack1ll1_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ഺ"):
    bstack11l1l1l1_opy_[bstack1ll1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴ഻ࠩ")][bstack1ll1_opy_ (u"ࠧ࡯ࡣࡰࡩ഼ࠬ")] = name
  if type == bstack1ll1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫഽ"):
    bstack11l1l1l1_opy_[bstack1ll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬാ")][bstack1ll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪി")] = status
    if status == bstack1ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫീ"):
      bstack11l1l1l1_opy_[bstack1ll1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨു")][bstack1ll1_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ൂ")] = json.dumps(str(reason))
  bstack1lll1l11l_opy_ = bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬൃ").format(json.dumps(bstack11l1l1l1_opy_))
  return bstack1lll1l11l_opy_
def bstack11l11ll_opy_(item, call, rep):
  global bstack1ll11ll1l_opy_
  global bstack11l1111l_opy_
  name = bstack1ll1_opy_ (u"ࠨࠩൄ")
  try:
    if rep.when == bstack1ll1_opy_ (u"ࠩࡦࡥࡱࡲࠧ൅"):
      bstack111l1lll_opy_ = threading.current_thread().name
      bstack1ll1ll1l1_opy_ = bstack111l1lll_opy_.split(bstack1ll1_opy_ (u"ࠪࡣࡧࡹࡴࡢࡥ࡮ࡣࠬെ"))
      bstack11l1l1l_opy_ = bstack1ll1ll1l1_opy_[0]
      bstack1lll1111l_opy_ = bstack1ll1ll1l1_opy_[1]
      threading.current_thread().name = str(bstack11l1l1l_opy_)
      try:
        name = str(rep.nodeid)
        bstack1llllll11_opy_ = bstack1llllll1_opy_(bstack1ll1_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬേ"), name, bstack1ll1_opy_ (u"ࠬ࠭ൈ"), bstack1ll1_opy_ (u"࠭ࠧ൉"), bstack1ll1_opy_ (u"ࠧࠨൊ"), bstack1ll1_opy_ (u"ࠨࠩോ"))
        for driver in bstack11l1111l_opy_:
          if bstack1lll1111l_opy_ == driver.session_id:
            driver.execute_script(bstack1llllll11_opy_)
      except Exception as e:
        logger.debug(bstack1ll1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩൌ").format(str(e)))
      try:
        status = bstack1ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦ്ࠪ") if rep.outcome.lower() == bstack1ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫൎ") else bstack1ll1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ൏")
        reason = bstack1ll1_opy_ (u"࠭ࠧ൐")
        if status == bstack1ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ൑"):
          reason = rep.longrepr.reprcrash.message
        level = bstack1ll1_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭൒") if status == bstack1ll1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ൓") else bstack1ll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩൔ")
        data = name + bstack1ll1_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭ൕ") if status == bstack1ll1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬൖ") else name + bstack1ll1_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠡࠡࠩൗ") + reason
        bstack1ll1l11ll_opy_ = bstack1llllll1_opy_(bstack1ll1_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩ൘"), bstack1ll1_opy_ (u"ࠨࠩ൙"), bstack1ll1_opy_ (u"ࠩࠪ൚"), bstack1ll1_opy_ (u"ࠪࠫ൛"), level, data)
        bstack1llllll11_opy_ = bstack1llllll1_opy_(bstack1ll1_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ൜"), bstack1ll1_opy_ (u"ࠬ࠭൝"), status, reason, bstack1ll1_opy_ (u"࠭ࠧ൞"), bstack1ll1_opy_ (u"ࠧࠨൟ"))
        for driver in bstack11l1111l_opy_:
          if bstack1lll1111l_opy_ == driver.session_id:
            driver.execute_script(bstack1ll1l11ll_opy_)
            driver.execute_script(bstack1llllll11_opy_)
      except Exception as e:
        logger.debug(bstack1ll1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡩ࡯࡯ࡶࡨࡼࡹࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬൠ").format(str(e)))
  except Exception as e:
    logger.debug(bstack1ll1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡴࡢࡶࡨࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿࢂ࠭ൡ").format(str(e)))
  bstack1ll11ll1l_opy_(item, call, rep)
def bstack1ll1l11_opy_(framework_name):
  global bstack1ll1l1ll_opy_
  global bstack1lll1lll_opy_
  bstack1ll1l1ll_opy_ = framework_name
  logger.info(bstack111111ll_opy_.format(bstack1ll1l1ll_opy_.split(bstack1ll1_opy_ (u"ࠪ࠱ࠬൢ"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    Service.start = bstack1l1l11l1l_opy_
    Service.stop = bstack1llll1ll_opy_
    webdriver.Remote.__init__ = bstack111lll111_opy_
    webdriver.Remote.get = bstack11l11l1l_opy_
    WebDriver.close = bstack11ll11l1l_opy_
    bstack1lll1lll_opy_ = True
  except Exception as e:
    pass
  bstack1llll_opy_()
  if not bstack1lll1lll_opy_:
    bstack11ll1l11_opy_(bstack1ll1_opy_ (u"ࠦࡕࡧࡣ࡬ࡣࡪࡩࡸࠦ࡮ࡰࡶࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠨൣ"), bstack1llll11ll_opy_)
  if bstack11l11l1_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack1l1l1llll_opy_
    except Exception as e:
      logger.error(bstack1ll1l1ll1_opy_.format(str(e)))
  if (bstack1ll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ൤") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1ll1ll11l_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1ll111l11_opy_
      except Exception as e:
        logger.warn(bstack1ll1ll1_opy_ + str(e))
    except Exception as e:
      bstack11ll1l11_opy_(e, bstack1ll1ll1_opy_)
    Output.end_test = bstack1llll111_opy_
    TestStatus.__init__ = bstack1l11l1l1l_opy_
    QueueItem.__init__ = bstack111l111l_opy_
    pabot._create_items = bstack11lll1l1l_opy_
    try:
      from pabot import __version__ as bstack11l1lll11_opy_
      if version.parse(bstack11l1lll11_opy_) >= version.parse(bstack1ll1_opy_ (u"࠭࠲࠯࠳࠸࠲࠵࠭൥")):
        pabot._run = bstack111ll11ll_opy_
      elif version.parse(bstack11l1lll11_opy_) >= version.parse(bstack1ll1_opy_ (u"ࠧ࠳࠰࠴࠷࠳࠶ࠧ൦")):
        pabot._run = bstack11l1lll_opy_
      else:
        pabot._run = bstack11l11llll_opy_
    except Exception as e:
      pabot._run = bstack11l11llll_opy_
    pabot._create_command_for_execution = bstack1ll1111l_opy_
    pabot._report_results = bstack1111ll_opy_
  if bstack1ll1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ൧") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11ll1l11_opy_(e, bstack1l11l11ll_opy_)
    Runner.run_hook = bstack11l1ll1_opy_
    Step.run = bstack1ll1l11l_opy_
  if bstack1ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ൨") in str(framework_name).lower():
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      from _pytest import runner
      pytest_selenium.pytest_report_header = bstack111l11_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1l111l1l1_opy_
      Config.getoption = bstack1lll1l1l1_opy_
      runner._update_current_test_var = bstack1l1111l1_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack11l11ll_opy_
    except Exception as e:
      pass
def bstack111llll11_opy_():
  global CONFIG
  if bstack1ll1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ൩") in CONFIG and int(CONFIG[bstack1ll1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ൪")]) > 1:
    logger.warn(bstack1l11l111l_opy_)
def bstack11ll11ll1_opy_(arg):
  arg.append(bstack1ll1_opy_ (u"ࠧ࠳࠭ࡤࡣࡳࡸࡺࡸࡥ࠾ࡵࡼࡷࠧ൫"))
  arg.append(bstack1ll1_opy_ (u"ࠨ࠭ࡘࠤ൬"))
  arg.append(bstack1ll1_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫࠺ࡎࡱࡧࡹࡱ࡫ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡ࡫ࡰࡴࡴࡸࡴࡦࡦ࠽ࡴࡾࡺࡥࡴࡶ࠱ࡔࡾࡺࡥࡴࡶ࡚ࡥࡷࡴࡩ࡯ࡩࠥ൭"))
  global CONFIG
  bstack1ll1l11_opy_(bstack111l_opy_)
  os.environ[bstack1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩ൮")] = CONFIG[bstack1ll1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ൯")]
  os.environ[bstack1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭൰")] = CONFIG[bstack1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ൱")]
  from _pytest.config import main as bstack1ll11l111_opy_
  bstack1ll11l111_opy_(arg)
def bstack11l1_opy_(arg):
  bstack1ll1l11_opy_(bstack1l1lll11_opy_)
  from behave.__main__ import main as bstack1l1lll111_opy_
  bstack1l1lll111_opy_(arg)
def bstack1ll1l1111_opy_():
  logger.info(bstack1l1ll11l1_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1ll1_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ൲"), help=bstack1ll1_opy_ (u"࠭ࡇࡦࡰࡨࡶࡦࡺࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡤࡱࡱࡪ࡮࡭ࠧ൳"))
  parser.add_argument(bstack1ll1_opy_ (u"ࠧ࠮ࡷࠪ൴"), bstack1ll1_opy_ (u"ࠨ࠯࠰ࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬ൵"), help=bstack1ll1_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡵࡴࡧࡵࡲࡦࡳࡥࠨ൶"))
  parser.add_argument(bstack1ll1_opy_ (u"ࠪ࠱ࡰ࠭൷"), bstack1ll1_opy_ (u"ࠫ࠲࠳࡫ࡦࡻࠪ൸"), help=bstack1ll1_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡤࡧࡨ࡫ࡳࡴࠢ࡮ࡩࡾ࠭൹"))
  parser.add_argument(bstack1ll1_opy_ (u"࠭࠭ࡧࠩൺ"), bstack1ll1_opy_ (u"ࠧ࠮࠯ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬൻ"), help=bstack1ll1_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧർ"))
  bstack11llll1l_opy_ = parser.parse_args()
  try:
    bstack1l11lll1_opy_ = bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡩࡨࡲࡪࡸࡩࡤ࠰ࡼࡱࡱ࠴ࡳࡢ࡯ࡳࡰࡪ࠭ൽ")
    if bstack11llll1l_opy_.framework and bstack11llll1l_opy_.framework not in (bstack1ll1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪൾ"), bstack1ll1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬൿ")):
      bstack1l11lll1_opy_ = bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠮ࡺ࡯࡯࠲ࡸࡧ࡭ࡱ࡮ࡨࠫ඀")
    bstack1l1l1ll_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l11lll1_opy_)
    bstack1lllllll1_opy_ = open(bstack1l1l1ll_opy_, bstack1ll1_opy_ (u"࠭ࡲࠨඁ"))
    bstack1l11l1l1_opy_ = bstack1lllllll1_opy_.read()
    bstack1lllllll1_opy_.close()
    if bstack11llll1l_opy_.username:
      bstack1l11l1l1_opy_ = bstack1l11l1l1_opy_.replace(bstack1ll1_opy_ (u"࡚ࠧࡑࡘࡖࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧං"), bstack11llll1l_opy_.username)
    if bstack11llll1l_opy_.key:
      bstack1l11l1l1_opy_ = bstack1l11l1l1_opy_.replace(bstack1ll1_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪඃ"), bstack11llll1l_opy_.key)
    if bstack11llll1l_opy_.framework:
      bstack1l11l1l1_opy_ = bstack1l11l1l1_opy_.replace(bstack1ll1_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪ඄"), bstack11llll1l_opy_.framework)
    file_name = bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭අ")
    file_path = os.path.abspath(file_name)
    bstack111ll11l1_opy_ = open(file_path, bstack1ll1_opy_ (u"ࠫࡼ࠭ආ"))
    bstack111ll11l1_opy_.write(bstack1l11l1l1_opy_)
    bstack111ll11l1_opy_.close()
    logger.info(bstack11lllll11_opy_)
    try:
      os.environ[bstack1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧඇ")] = bstack11llll1l_opy_.framework if bstack11llll1l_opy_.framework != None else bstack1ll1_opy_ (u"ࠨࠢඈ")
      config = yaml.safe_load(bstack1l11l1l1_opy_)
      config[bstack1ll1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧඉ")] = bstack1ll1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡵࡨࡸࡺࡶࠧඊ")
      bstack1l111l_opy_(bstack1llll1l1_opy_, config)
    except Exception as e:
      logger.debug(bstack1111111_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1ll11l11l_opy_.format(str(e)))
def bstack1l111l_opy_(bstack11lllllll_opy_, config, bstack111lll11_opy_ = {}):
  global bstack1111ll1_opy_
  if not config:
    return
  bstack1ll1lll1_opy_ = bstack11111l1_opy_ if not bstack1111ll1_opy_ else ( bstack1llll1l11_opy_ if bstack1ll1_opy_ (u"ࠩࡤࡴࡵ࠭උ") in config else bstack1ll1l11l1_opy_ )
  data = {
    bstack1ll1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬඌ"): config[bstack1ll1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ඍ")],
    bstack1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨඎ"): config[bstack1ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩඏ")],
    bstack1ll1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫඐ"): bstack11lllllll_opy_,
    bstack1ll1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫඑ"): {
      bstack1ll1_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧඒ"): str(config[bstack1ll1_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪඓ")]) if bstack1ll1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫඔ") in config else bstack1ll1_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨඕ"),
      bstack1ll1_opy_ (u"࠭ࡲࡦࡨࡨࡶࡷ࡫ࡲࠨඖ"): bstack1l1llll1_opy_(os.getenv(bstack1ll1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠤ඗"), bstack1ll1_opy_ (u"ࠣࠤ඘"))),
      bstack1ll1_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫ඙"): bstack1ll1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪක"),
      bstack1ll1_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬඛ"): bstack1ll1lll1_opy_,
      bstack1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨග"): config[bstack1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩඝ")]if config[bstack1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪඞ")] else bstack1ll1_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤඟ"),
      bstack1ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫච"): str(config[bstack1ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬඡ")]) if bstack1ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ජ") in config else bstack1ll1_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨඣ"),
      bstack1ll1_opy_ (u"࠭࡯ࡴࠩඤ"): sys.platform,
      bstack1ll1_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩඥ"): socket.gethostname()
    }
  }
  update(data[bstack1ll1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫඦ")], bstack111lll11_opy_)
  try:
    response = bstack11111ll_opy_(bstack1ll1_opy_ (u"ࠩࡓࡓࡘ࡚ࠧට"), bstack11l1ll111_opy_, data, config)
    if response:
      logger.debug(bstack111ll1l11_opy_.format(bstack11lllllll_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1l1l111_opy_.format(str(e)))
def bstack11111ll_opy_(type, url, data, config):
  bstack1llll11l_opy_ = bstack1llll11_opy_.format(url)
  proxies = bstack1lll11l11_opy_(config, bstack1llll11l_opy_)
  if type == bstack1ll1_opy_ (u"ࠪࡔࡔ࡙ࡔࠨඨ"):
    response = requests.post(bstack1llll11l_opy_, json=data,
                    headers={bstack1ll1_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪඩ"): bstack1ll1_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨඪ")}, auth=(config[bstack1ll1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨණ")], config[bstack1ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪඬ")]), proxies=proxies)
  return response
def bstack1l1llll1_opy_(framework):
  return bstack1ll1_opy_ (u"ࠣࡽࢀ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࡾࢁࠧත").format(str(framework), __version__) if framework else bstack1ll1_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࡼࡿࠥථ").format(__version__)
def bstack1l1l11lll_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  try:
    bstack1ll1l111_opy_()
    logger.debug(bstack1ll111lll_opy_.format(str(CONFIG)))
    bstack1l1l111l_opy_()
    bstack1l1l1ll1_opy_()
  except Exception as e:
    logger.error(bstack1ll1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴ࠱ࠦࡥࡳࡴࡲࡶ࠿ࠦࠢද") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1l1lll1l1_opy_
  atexit.register(bstack11l1ll11_opy_)
  signal.signal(signal.SIGINT, bstack1111_opy_)
  signal.signal(signal.SIGTERM, bstack1111_opy_)
def bstack1l1lll1l1_opy_(exctype, value, traceback):
  global bstack11l1111l_opy_
  try:
    for driver in bstack11l1111l_opy_:
      driver.execute_script(
        bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ࠲ࠠࠣࡴࡨࡥࡸࡵ࡮ࠣ࠼ࠣࠫධ") + json.dumps(bstack1ll1_opy_ (u"࡙ࠧࡥࡴࡵ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣන") + str(value)) + bstack1ll1_opy_ (u"࠭ࡽࡾࠩ඲"))
  except Exception:
    pass
  bstack11lll1ll1_opy_(value)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack11lll1ll1_opy_(message = bstack1ll1_opy_ (u"ࠧࠨඳ")):
  global CONFIG
  try:
    if message:
      bstack111lll11_opy_ = {
        bstack1ll1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧප"): str(message)
      }
      bstack1l111l_opy_(bstack11ll1ll1l_opy_, CONFIG, bstack111lll11_opy_)
    else:
      bstack1l111l_opy_(bstack11ll1ll1l_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1l111llll_opy_.format(str(e)))
def bstack11l1ll1l_opy_(bstack1l11lll11_opy_, size):
  bstack1ll111111_opy_ = []
  while len(bstack1l11lll11_opy_) > size:
    bstack1l1l1l111_opy_ = bstack1l11lll11_opy_[:size]
    bstack1ll111111_opy_.append(bstack1l1l1l111_opy_)
    bstack1l11lll11_opy_   = bstack1l11lll11_opy_[size:]
  bstack1ll111111_opy_.append(bstack1l11lll11_opy_)
  return bstack1ll111111_opy_
def run_on_browserstack(bstack1lll1l1_opy_=None, bstack1ll1lllll_opy_=None):
  global CONFIG
  global bstack11l11lll1_opy_
  global bstack1ll1ll1l_opy_
  bstack1lll1l1l_opy_ = bstack1ll1_opy_ (u"ࠩࠪඵ")
  if bstack1lll1l1_opy_:
    CONFIG = bstack1lll1l1_opy_[bstack1ll1_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪබ")]
    bstack11l11lll1_opy_ = bstack1lll1l1_opy_[bstack1ll1_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬභ")]
    bstack1ll1ll1l_opy_ = bstack1lll1l1_opy_[bstack1ll1_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧම")]
    bstack1lll1l1l_opy_ = bstack1ll1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ඹ")
  if len(sys.argv) <= 1:
    logger.critical(bstack1lll111_opy_)
    return
  if sys.argv[1] == bstack1ll1_opy_ (u"ࠧ࠮࠯ࡹࡩࡷࡹࡩࡰࡰࠪය")  or sys.argv[1] == bstack1ll1_opy_ (u"ࠨ࠯ࡹࠫර"):
    logger.info(bstack1ll1_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡒࡼࡸ࡭ࡵ࡮ࠡࡕࡇࡏࠥࡼࡻࡾࠩ඼").format(__version__))
    return
  if sys.argv[1] == bstack1ll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩල"):
    bstack1ll1l1111_opy_()
    return
  args = sys.argv
  bstack1l1l11lll_opy_()
  global bstack11l1l1l11_opy_
  global bstack1l1ll11_opy_
  global bstack11ll1ll_opy_
  global bstack1l1111lll_opy_
  global bstack11ll111l1_opy_
  global bstack11111l_opy_
  global bstack111lll_opy_
  if not bstack1lll1l1l_opy_:
    if args[1] == bstack1ll1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ඾") or args[1] == bstack1ll1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭඿"):
      bstack1lll1l1l_opy_ = bstack1ll1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ව")
      args = args[2:]
    elif args[1] == bstack1ll1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ශ"):
      bstack1lll1l1l_opy_ = bstack1ll1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧෂ")
      args = args[2:]
    elif args[1] == bstack1ll1_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨස"):
      bstack1lll1l1l_opy_ = bstack1ll1_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩහ")
      args = args[2:]
    elif args[1] == bstack1ll1_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬළ"):
      bstack1lll1l1l_opy_ = bstack1ll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ෆ")
      args = args[2:]
    elif args[1] == bstack1ll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭෇"):
      bstack1lll1l1l_opy_ = bstack1ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ෈")
      args = args[2:]
    elif args[1] == bstack1ll1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ෉"):
      bstack1lll1l1l_opy_ = bstack1ll1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦ්ࠩ")
      args = args[2:]
    else:
      if not bstack1ll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭෋") in CONFIG or str(CONFIG[bstack1ll1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ෌")]).lower() in [bstack1ll1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ෍"), bstack1ll1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧ෎")]:
        bstack1lll1l1l_opy_ = bstack1ll1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧා")
        args = args[1:]
      elif str(CONFIG[bstack1ll1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫැ")]).lower() == bstack1ll1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨෑ"):
        bstack1lll1l1l_opy_ = bstack1ll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩි")
        args = args[1:]
      elif str(CONFIG[bstack1ll1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧී")]).lower() == bstack1ll1_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫු"):
        bstack1lll1l1l_opy_ = bstack1ll1_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ෕")
        args = args[1:]
      elif str(CONFIG[bstack1ll1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪූ")]).lower() == bstack1ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ෗"):
        bstack1lll1l1l_opy_ = bstack1ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩෘ")
        args = args[1:]
      elif str(CONFIG[bstack1ll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ෙ")]).lower() == bstack1ll1_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫේ"):
        bstack1lll1l1l_opy_ = bstack1ll1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬෛ")
        args = args[1:]
      else:
        os.environ[bstack1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨො")] = bstack1lll1l1l_opy_
        bstack11ll1l11l_opy_(bstack11l11l11_opy_)
  global bstack11l1lll1l_opy_
  if bstack1lll1l1_opy_:
    try:
      os.environ[bstack1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩෝ")] = bstack1lll1l1l_opy_
      bstack1l111l_opy_(bstack1lll11l1_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack1l111llll_opy_.format(str(e)))
  global bstack1111l1l1_opy_
  global bstack1l11lll_opy_
  global bstack1llllllll_opy_
  global bstack1l1l1l1_opy_
  global bstack11ll11l_opy_
  global bstack1lllll_opy_
  global bstack11lll1_opy_
  global bstack111l111_opy_
  global bstack1l11lllll_opy_
  global bstack11llll111_opy_
  global bstack11l1111l1_opy_
  global bstack1111l11l_opy_
  global bstack1l1l1l1l_opy_
  global bstack1ll1llll1_opy_
  global bstack11llll1ll_opy_
  global bstack111l1l_opy_
  global bstack1ll11ll1l_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1111l1l1_opy_ = webdriver.Remote.__init__
    bstack1l11lllll_opy_ = WebDriver.close
    bstack1111l11l_opy_ = WebDriver.get
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack11l1lll1l_opy_ = Popen.__init__
  except Exception as e:
    pass
  if bstack11ll111ll_opy_():
    if bstack1lll1111_opy_() < version.parse(bstack1l11ll1l_opy_):
      logger.error(bstack11l11111l_opy_.format(bstack1lll1111_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l1l1l1l_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1ll1l1ll1_opy_.format(str(e)))
  if bstack1lll1l1l_opy_ != bstack1ll1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨෞ") or (bstack1lll1l1l_opy_ == bstack1ll1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩෟ") and not bstack1lll1l1_opy_):
    bstack11l1ll11l_opy_()
  if (bstack1lll1l1l_opy_ in [bstack1ll1_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ෠"), bstack1ll1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ෡"), bstack1ll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭෢")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1ll1ll11l_opy_
        bstack1llllllll_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1ll1ll1_opy_ + str(e))
    except Exception as e:
      bstack11ll1l11_opy_(e, bstack1ll1ll1_opy_)
    if bstack1lll1l1l_opy_ != bstack1ll1_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ෣"):
      bstack1ll111l_opy_()
    bstack1l11lll_opy_ = Output.end_test
    bstack1l1l1l1_opy_ = TestStatus.__init__
    bstack1lllll_opy_ = pabot._run
    bstack11lll1_opy_ = QueueItem.__init__
    bstack111l111_opy_ = pabot._create_command_for_execution
    bstack111l1l_opy_ = pabot._report_results
  if bstack1lll1l1l_opy_ == bstack1ll1_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ෤"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11ll1l11_opy_(e, bstack1l11l11ll_opy_)
    bstack11llll111_opy_ = Runner.run_hook
    bstack11l1111l1_opy_ = Step.run
  if bstack1lll1l1l_opy_ == bstack1ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ෥"):
    try:
      from _pytest.config import Config
      bstack1ll1llll1_opy_ = Config.getoption
      from _pytest import runner
      bstack11llll1ll_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack11l1l111_opy_)
    try:
      from pytest_bdd import reporting
      bstack1ll11ll1l_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1ll1_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡱࠣࡶࡺࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࡵࠪ෦"))
  if bstack1lll1l1l_opy_ == bstack1ll1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ෧"):
    bstack1l1ll11_opy_ = True
    if bstack1lll1l1_opy_:
      bstack11ll111l1_opy_ = CONFIG.get(bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ෨"), {}).get(bstack1ll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ෩"))
      bstack1ll1l11_opy_(bstack1l11111_opy_)
      sys.path.append(os.path.dirname(os.path.abspath(bstack1lll1l1_opy_[bstack1ll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ෪")])))
      mod_globals = globals()
      mod_globals[bstack1ll1_opy_ (u"ࠧࡠࡡࡱࡥࡲ࡫࡟ࡠࠩ෫")] = bstack1ll1_opy_ (u"ࠨࡡࡢࡱࡦ࡯࡮ࡠࡡࠪ෬")
      mod_globals[bstack1ll1_opy_ (u"ࠩࡢࡣ࡫࡯࡬ࡦࡡࡢࠫ෭")] = os.path.abspath(bstack1lll1l1_opy_[bstack1ll1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭෮")])
      global bstack11l1111l_opy_
      try:
        exec(open(bstack1lll1l1_opy_[bstack1ll1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ෯")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1ll1_opy_ (u"ࠬࡉࡡࡶࡩ࡫ࡸࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠬ෰").format(str(e)))
          for driver in bstack11l1111l_opy_:
            bstack1ll1lllll_opy_.append({
              bstack1ll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ෱"): bstack1lll1l1_opy_[bstack1ll1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪෲ")],
              bstack1ll1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧෳ"): str(e),
              bstack1ll1_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ෴"): multiprocessing.current_process().name
            })
            driver.execute_script(
              bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡶࡸࡦࡺࡵࡴࠤ࠽ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ࠱ࠦࠢࡳࡧࡤࡷࡴࡴࠢ࠻ࠢࠪ෵") + json.dumps(bstack1ll1_opy_ (u"ࠦࡘ࡫ࡳࡴ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢ෶") + str(e)) + bstack1ll1_opy_ (u"ࠬࢃࡽࠨ෷"))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack11l1111l_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      bstack1111llll_opy_()
      bstack111llll11_opy_()
      if bstack1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ෸") in CONFIG:
        bstack1lllll11_opy_ = {
          bstack1ll1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ෹"): args[0],
          bstack1ll1_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨ෺"): CONFIG,
          bstack1ll1_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪ෻"): bstack11l11lll1_opy_,
          bstack1ll1_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ෼"): bstack1ll1ll1l_opy_
        }
        bstack1l11ll1l1_opy_ = []
        manager = multiprocessing.Manager()
        bstack1l1111l1l_opy_ = manager.list()
        for index, platform in enumerate(CONFIG[bstack1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ෽")]):
          bstack1lllll11_opy_[bstack1ll1_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ෾")] = index
          bstack1l11ll1l1_opy_.append(multiprocessing.Process(name=str(index),
                                        target=run_on_browserstack, args=(bstack1lllll11_opy_, bstack1l1111l1l_opy_)))
        for t in bstack1l11ll1l1_opy_:
          t.start()
        for t in bstack1l11ll1l1_opy_:
          t.join()
        bstack111lll_opy_ = list(bstack1l1111l1l_opy_)
      else:
        bstack1ll1l11_opy_(bstack1l11111_opy_)
        sys.path.append(os.path.dirname(os.path.abspath(args[0])))
        mod_globals = globals()
        mod_globals[bstack1ll1_opy_ (u"࠭࡟ࡠࡰࡤࡱࡪࡥ࡟ࠨ෿")] = bstack1ll1_opy_ (u"ࠧࡠࡡࡰࡥ࡮ࡴ࡟ࡠࠩ฀")
        mod_globals[bstack1ll1_opy_ (u"ࠨࡡࡢࡪ࡮ࡲࡥࡠࡡࠪก")] = os.path.abspath(args[0])
        exec(open(args[0]).read(), mod_globals)
  elif bstack1lll1l1l_opy_ == bstack1ll1_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨข") or bstack1lll1l1l_opy_ == bstack1ll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩฃ"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack11ll1l11_opy_(e, bstack1ll1ll1_opy_)
    bstack1111llll_opy_()
    bstack1ll1l11_opy_(bstack11l11ll1_opy_)
    if bstack1ll1_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩค") in args:
      i = args.index(bstack1ll1_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪฅ"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack11l1l1l11_opy_))
    args.insert(0, str(bstack1ll1_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫฆ")))
    pabot.main(args)
  elif bstack1lll1l1l_opy_ == bstack1ll1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨง"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack11ll1l11_opy_(e, bstack1ll1ll1_opy_)
    for a in args:
      if bstack1ll1_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞ࠧจ") in a:
        bstack1l1111lll_opy_ = int(a.split(bstack1ll1_opy_ (u"ࠩ࠽ࠫฉ"))[1])
      if bstack1ll1_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡇࡉࡋࡒࡏࡄࡃࡏࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧช") in a:
        bstack11ll111l1_opy_ = str(a.split(bstack1ll1_opy_ (u"ࠫ࠿࠭ซ"))[1])
      if bstack1ll1_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗࠬฌ") in a:
        bstack11111l_opy_ = str(a.split(bstack1ll1_opy_ (u"࠭࠺ࠨญ"))[1])
    bstack1l1l1l1l1_opy_ = None
    if bstack1ll1_opy_ (u"ࠧ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽ࠭ฎ") in args:
      i = args.index(bstack1ll1_opy_ (u"ࠨ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠧฏ"))
      args.pop(i)
      bstack1l1l1l1l1_opy_ = args.pop(i)
    if bstack1l1l1l1l1_opy_ is not None:
      global bstack111ll1l_opy_
      bstack111ll1l_opy_ = bstack1l1l1l1l1_opy_
    bstack1ll1l11_opy_(bstack11l11ll1_opy_)
    run_cli(args)
  elif bstack1lll1l1l_opy_ == bstack1ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩฐ"):
    try:
      from _pytest.config import _prepareconfig
      from _pytest.config import Config
      from _pytest import runner
      import importlib
      bstack1l1l1l11l_opy_ = importlib.find_loader(bstack1ll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࠬฑ"))
    except Exception as e:
      logger.warn(e, bstack11l1l111_opy_)
    bstack1111llll_opy_()
    try:
      if bstack1ll1_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭ฒ") in args:
        i = args.index(bstack1ll1_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧณ"))
        args.pop(i+1)
        args.pop(i)
      if bstack1ll1_opy_ (u"࠭࠭࠮ࡲ࡯ࡹ࡬࡯࡮ࡴࠩด") in args:
        i = args.index(bstack1ll1_opy_ (u"ࠧ࠮࠯ࡳࡰࡺ࡭ࡩ࡯ࡵࠪต"))
        args.pop(i+1)
        args.pop(i)
      if bstack1ll1_opy_ (u"ࠨ࠯ࡳࠫถ") in args:
        i = args.index(bstack1ll1_opy_ (u"ࠩ࠰ࡴࠬท"))
        args.pop(i+1)
        args.pop(i)
      if bstack1ll1_opy_ (u"ࠪ࠱࠲ࡴࡵ࡮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫธ") in args:
        i = args.index(bstack1ll1_opy_ (u"ࠫ࠲࠳࡮ࡶ࡯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬน"))
        args.pop(i+1)
        args.pop(i)
      if bstack1ll1_opy_ (u"ࠬ࠳࡮ࠨบ") in args:
        i = args.index(bstack1ll1_opy_ (u"࠭࠭࡯ࠩป"))
        args.pop(i+1)
        args.pop(i)
    except Exception as exc:
      logger.error(str(exc))
    config = _prepareconfig(args)
    bstack111llll1_opy_ = config.args
    bstack1ll1llll_opy_ = config.invocation_params.args
    bstack1ll1llll_opy_ = list(bstack1ll1llll_opy_)
    bstack1lll111l1_opy_ = [os.path.normpath(item) for item in bstack111llll1_opy_]
    bstack1l1ll1l_opy_ = [os.path.normpath(item) for item in bstack1ll1llll_opy_]
    bstack1l11l1lll_opy_ = [item for item in bstack1l1ll1l_opy_ if item not in bstack1lll111l1_opy_]
    if bstack1ll1_opy_ (u"ࠧ࠮࠯ࡦࡥࡨ࡮ࡥ࠮ࡥ࡯ࡩࡦࡸࠧผ") not in bstack1l11l1lll_opy_:
      bstack1l11l1lll_opy_.append(bstack1ll1_opy_ (u"ࠨ࠯࠰ࡧࡦࡩࡨࡦ࠯ࡦࡰࡪࡧࡲࠨฝ"))
    import platform as pf
    if pf.system().lower() == bstack1ll1_opy_ (u"ࠩࡺ࡭ࡳࡪ࡯ࡸࡵࠪพ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack111llll1_opy_ = [str(PurePosixPath(PureWindowsPath(bstack11ll1l_opy_)))
                    for bstack11ll1l_opy_ in bstack111llll1_opy_]
    if (bstack11llllll_opy_):
      bstack1l11l1lll_opy_.append(bstack1ll1_opy_ (u"ࠪ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧฟ"))
      bstack1l11l1lll_opy_.append(bstack1ll1_opy_ (u"࡙ࠫࡸࡵࡦࠩภ"))
    bstack1l11l1lll_opy_.append(bstack1ll1_opy_ (u"ࠬ࠳ࡰࠨม"))
    bstack1l11l1lll_opy_.append(bstack1ll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡵࡲࡵࡨ࡫ࡱࠫย"))
    bstack1l11l1lll_opy_.append(bstack1ll1_opy_ (u"ࠧ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠩร"))
    bstack1l11l1lll_opy_.append(bstack1ll1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨฤ"))
    bstack11l11l1ll_opy_ = []
    for spec in bstack111llll1_opy_:
      bstack1lll111ll_opy_ = []
      bstack1lll111ll_opy_.append(spec)
      bstack1lll111ll_opy_ += bstack1l11l1lll_opy_
      bstack11l11l1ll_opy_.append(bstack1lll111ll_opy_)
    bstack11ll1ll_opy_ = True
    bstack1l11ll_opy_ = 1
    if bstack1ll1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩล") in CONFIG:
      bstack1l11ll_opy_ = CONFIG[bstack1ll1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪฦ")]
    bstack1l11l111_opy_ = int(bstack1l11ll_opy_)*int(len(CONFIG[bstack1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧว")]))
    execution_items = []
    for bstack1lll111ll_opy_ in bstack11l11l1ll_opy_:
      for index, _ in enumerate(CONFIG[bstack1ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨศ")]):
        item = {}
        item[bstack1ll1_opy_ (u"࠭ࡡࡳࡩࠪษ")] = bstack1lll111ll_opy_
        item[bstack1ll1_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ส")] = index
        execution_items.append(item)
    bstack1l111ll_opy_ = bstack11l1ll1l_opy_(execution_items, bstack1l11l111_opy_)
    for execution_item in bstack1l111ll_opy_:
      bstack1l11ll1l1_opy_ = []
      for item in execution_item:
        bstack1l11ll1l1_opy_.append(bstack11l1lll1_opy_(name=str(item[bstack1ll1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧห")]),
                                            target=bstack11ll11ll1_opy_,
                                            args=(item[bstack1ll1_opy_ (u"ࠩࡤࡶ࡬࠭ฬ")],)))
      for t in bstack1l11ll1l1_opy_:
        t.start()
      for t in bstack1l11ll1l1_opy_:
        t.join()
  elif bstack1lll1l1l_opy_ == bstack1ll1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪอ"):
    try:
      from behave.__main__ import main as bstack1l1lll111_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack11ll1l11_opy_(e, bstack1l11l11ll_opy_)
    bstack1111llll_opy_()
    bstack11ll1ll_opy_ = True
    bstack1l11ll_opy_ = 1
    if bstack1ll1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫฮ") in CONFIG:
      bstack1l11ll_opy_ = CONFIG[bstack1ll1_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬฯ")]
    bstack1l11l111_opy_ = int(bstack1l11ll_opy_)*int(len(CONFIG[bstack1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩะ")]))
    config = Configuration(args)
    bstack111llll1_opy_ = config.paths
    bstack1ll11111_opy_ = []
    for arg in args:
      if os.path.normpath(arg) not in bstack111llll1_opy_:
        bstack1ll11111_opy_.append(arg)
    import platform as pf
    if pf.system().lower() == bstack1ll1_opy_ (u"ࠧࡸ࡫ࡱࡨࡴࡽࡳࠨั"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack111llll1_opy_ = [str(PurePosixPath(PureWindowsPath(bstack11ll1l_opy_)))
                    for bstack11ll1l_opy_ in bstack111llll1_opy_]
    bstack11l11l1ll_opy_ = []
    for spec in bstack111llll1_opy_:
      bstack1lll111ll_opy_ = []
      bstack1lll111ll_opy_ += bstack1ll11111_opy_
      bstack1lll111ll_opy_.append(spec)
      bstack11l11l1ll_opy_.append(bstack1lll111ll_opy_)
    execution_items = []
    for index, _ in enumerate(CONFIG[bstack1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫา")]):
      for bstack1lll111ll_opy_ in bstack11l11l1ll_opy_:
        item = {}
        item[bstack1ll1_opy_ (u"ࠩࡤࡶ࡬࠭ำ")] = bstack1ll1_opy_ (u"ࠪࠤࠬิ").join(bstack1lll111ll_opy_)
        item[bstack1ll1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪี")] = index
        execution_items.append(item)
    bstack1l111ll_opy_ = bstack11l1ll1l_opy_(execution_items, bstack1l11l111_opy_)
    for execution_item in bstack1l111ll_opy_:
      bstack1l11ll1l1_opy_ = []
      for item in execution_item:
        bstack1l11ll1l1_opy_.append(bstack11l1lll1_opy_(name=str(item[bstack1ll1_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫึ")]),
                                            target=bstack11l1_opy_,
                                            args=(item[bstack1ll1_opy_ (u"࠭ࡡࡳࡩࠪื")],)))
      for t in bstack1l11ll1l1_opy_:
        t.start()
      for t in bstack1l11ll1l1_opy_:
        t.join()
  else:
    bstack11ll1l11l_opy_(bstack11l11l11_opy_)
  if not bstack1lll1l1_opy_:
    bstack11l111l1l_opy_()
def bstack11l111l1l_opy_():
  [bstack1l1111l11_opy_, bstack11l1111_opy_] = bstack11111l11_opy_()
  if bstack1l1111l11_opy_ is not None and bstack1llll1111_opy_() != -1:
    sessions = bstack11l11ll1l_opy_(bstack1l1111l11_opy_)
    bstack111l1l1l_opy_(sessions, bstack11l1111_opy_)
def bstack1111l11_opy_(bstack1l1ll11ll_opy_):
    if bstack1l1ll11ll_opy_:
        return bstack1l1ll11ll_opy_.capitalize()
    else:
        return bstack1l1ll11ll_opy_
def bstack1ll1lll11_opy_(bstack1ll1111ll_opy_):
    if bstack1ll1_opy_ (u"ࠧ࡯ࡣࡰࡩุࠬ") in bstack1ll1111ll_opy_ and bstack1ll1111ll_opy_[bstack1ll1_opy_ (u"ࠨࡰࡤࡱࡪู࠭")] != bstack1ll1_opy_ (u"ฺࠩࠪ"):
        return bstack1ll1111ll_opy_[bstack1ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨ฻")]
    else:
        bstack1ll1l1_opy_ = bstack1ll1_opy_ (u"ࠦࠧ฼")
        if bstack1ll1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ฽") in bstack1ll1111ll_opy_ and bstack1ll1111ll_opy_[bstack1ll1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭฾")] != None:
            bstack1ll1l1_opy_ += bstack1ll1111ll_opy_[bstack1ll1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ฿")] + bstack1ll1_opy_ (u"ࠣ࠮ࠣࠦเ")
            if bstack1ll1111ll_opy_[bstack1ll1_opy_ (u"ࠩࡲࡷࠬแ")] == bstack1ll1_opy_ (u"ࠥ࡭ࡴࡹࠢโ"):
                bstack1ll1l1_opy_ += bstack1ll1_opy_ (u"ࠦ࡮ࡕࡓࠡࠤใ")
            bstack1ll1l1_opy_ += (bstack1ll1111ll_opy_[bstack1ll1_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩไ")] or bstack1ll1_opy_ (u"࠭ࠧๅ"))
            return bstack1ll1l1_opy_
        else:
            bstack1ll1l1_opy_ += bstack1111l11_opy_(bstack1ll1111ll_opy_[bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨๆ")]) + bstack1ll1_opy_ (u"ࠣࠢࠥ็") + (bstack1ll1111ll_opy_[bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱ่ࠫ")] or bstack1ll1_opy_ (u"้ࠪࠫ")) + bstack1ll1_opy_ (u"ࠦ࠱๊ࠦࠢ")
            if bstack1ll1111ll_opy_[bstack1ll1_opy_ (u"ࠬࡵࡳࠨ๋")] == bstack1ll1_opy_ (u"ࠨࡗࡪࡰࡧࡳࡼࡹࠢ์"):
                bstack1ll1l1_opy_ += bstack1ll1_opy_ (u"ࠢࡘ࡫ࡱࠤࠧํ")
            bstack1ll1l1_opy_ += bstack1ll1111ll_opy_[bstack1ll1_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ๎")] or bstack1ll1_opy_ (u"ࠩࠪ๏")
            return bstack1ll1l1_opy_
def bstack1111l_opy_(bstack1ll11ll_opy_):
    if bstack1ll11ll_opy_ == bstack1ll1_opy_ (u"ࠥࡨࡴࡴࡥࠣ๐"):
        return bstack1ll1_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡧࡳࡧࡨࡲࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡧࡳࡧࡨࡲࠧࡄࡃࡰ࡯ࡳࡰࡪࡺࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ๑")
    elif bstack1ll11ll_opy_ == bstack1ll1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ๒"):
        return bstack1ll1_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡴࡨࡨࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡲࡦࡦࠥࡂࡋࡧࡩ࡭ࡧࡧࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩ๓")
    elif bstack1ll11ll_opy_ == bstack1ll1_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ๔"):
        return bstack1ll1_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽࡫ࡷ࡫ࡥ࡯࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥ࡫ࡷ࡫ࡥ࡯ࠤࡁࡔࡦࡹࡳࡦࡦ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ๕")
    elif bstack1ll11ll_opy_ == bstack1ll1_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣ๖"):
        return bstack1ll1_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡸࡥࡥ࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡶࡪࡪࠢ࠿ࡇࡵࡶࡴࡸ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ๗")
    elif bstack1ll11ll_opy_ == bstack1ll1_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࠧ๘"):
        return bstack1ll1_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࠤࡧࡨࡥ࠸࠸࠶࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࠦࡩࡪࡧ࠳࠳࠸ࠥࡂ࡙࡯࡭ࡦࡱࡸࡸࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪ๙")
    elif bstack1ll11ll_opy_ == bstack1ll1_opy_ (u"ࠨࡲࡶࡰࡱ࡭ࡳ࡭ࠢ๚"):
        return bstack1ll1_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡥࡰࡦࡩ࡫࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡥࡰࡦࡩ࡫ࠣࡀࡕࡹࡳࡴࡩ࡯ࡩ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ๛")
    else:
        return bstack1ll1_opy_ (u"ࠨ࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡧࡲࡡࡤ࡭࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡧࡲࡡࡤ࡭ࠥࡂࠬ๜")+bstack1111l11_opy_(bstack1ll11ll_opy_)+bstack1ll1_opy_ (u"ࠩ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ๝")
def bstack111l1l1_opy_(session):
    return bstack1ll1_opy_ (u"ࠪࡀࡹࡸࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡳࡱࡺࠦࡃࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠠࡴࡧࡶࡷ࡮ࡵ࡮࠮ࡰࡤࡱࡪࠨ࠾࠽ࡣࠣ࡬ࡷ࡫ࡦ࠾ࠤࡾࢁࠧࠦࡴࡢࡴࡪࡩࡹࡃࠢࡠࡤ࡯ࡥࡳࡱࠢ࠿ࡽࢀࡀ࠴ࡧ࠾࠽࠱ࡷࡨࡃࢁࡽࡼࡿ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁ࠵ࡴࡳࡀࠪ๞").format(session[bstack1ll1_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦࡣࡺࡸ࡬ࠨ๟")],bstack1ll1lll11_opy_(session), bstack1111l_opy_(session[bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡸࡺࡡࡵࡷࡶࠫ๠")]), bstack1111l_opy_(session[bstack1ll1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭๡")]), bstack1111l11_opy_(session[bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ๢")] or session[bstack1ll1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨ๣")] or bstack1ll1_opy_ (u"ࠩࠪ๤")) + bstack1ll1_opy_ (u"ࠥࠤࠧ๥") + (session[bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭๦")] or bstack1ll1_opy_ (u"ࠬ࠭๧")), session[bstack1ll1_opy_ (u"࠭࡯ࡴࠩ๨")] + bstack1ll1_opy_ (u"ࠢࠡࠤ๩") + session[bstack1ll1_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ๪")], session[bstack1ll1_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫ๫")] or bstack1ll1_opy_ (u"ࠪࠫ๬"), session[bstack1ll1_opy_ (u"ࠫࡨࡸࡥࡢࡶࡨࡨࡤࡧࡴࠨ๭")] if session[bstack1ll1_opy_ (u"ࠬࡩࡲࡦࡣࡷࡩࡩࡥࡡࡵࠩ๮")] else bstack1ll1_opy_ (u"࠭ࠧ๯"))
def bstack111l1l1l_opy_(sessions, bstack11l1111_opy_):
  try:
    bstack1lll11ll_opy_ = bstack1ll1_opy_ (u"ࠢࠣ๰")
    if not os.path.exists(bstack11ll_opy_):
      os.mkdir(bstack11ll_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll1_opy_ (u"ࠨࡣࡶࡷࡪࡺࡳ࠰ࡴࡨࡴࡴࡸࡴ࠯ࡪࡷࡱࡱ࠭๱")), bstack1ll1_opy_ (u"ࠩࡵࠫ๲")) as f:
      bstack1lll11ll_opy_ = f.read()
    bstack1lll11ll_opy_ = bstack1lll11ll_opy_.replace(bstack1ll1_opy_ (u"ࠪࡿࠪࡘࡅࡔࡗࡏࡘࡘࡥࡃࡐࡗࡑࡘࠪࢃࠧ๳"), str(len(sessions)))
    bstack1lll11ll_opy_ = bstack1lll11ll_opy_.replace(bstack1ll1_opy_ (u"ࠫࢀࠫࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠧࢀࠫ๴"), bstack11l1111_opy_)
    bstack1lll11ll_opy_ = bstack1lll11ll_opy_.replace(bstack1ll1_opy_ (u"ࠬࢁࠥࡃࡗࡌࡐࡉࡥࡎࡂࡏࡈࠩࢂ࠭๵"), sessions[0].get(bstack1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡴࡡ࡮ࡧࠪ๶")) if sessions[0] else bstack1ll1_opy_ (u"ࠧࠨ๷"))
    with open(os.path.join(bstack11ll_opy_, bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡳࡧࡳࡳࡷࡺ࠮ࡩࡶࡰࡰࠬ๸")), bstack1ll1_opy_ (u"ࠩࡺࠫ๹")) as stream:
      stream.write(bstack1lll11ll_opy_.split(bstack1ll1_opy_ (u"ࠪࡿ࡙ࠪࡅࡔࡕࡌࡓࡓ࡙࡟ࡅࡃࡗࡅࠪࢃࠧ๺"))[0])
      for session in sessions:
        stream.write(bstack111l1l1_opy_(session))
      stream.write(bstack1lll11ll_opy_.split(bstack1ll1_opy_ (u"ࠫࢀࠫࡓࡆࡕࡖࡍࡔࡔࡓࡠࡆࡄࡘࡆࠫࡽࠨ๻"))[1])
    logger.info(bstack1ll1_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡫ࡤࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡣࡷ࡬ࡰࡩࠦࡡࡳࡶ࡬ࡪࡦࡩࡴࡴࠢࡤࡸࠥࢁࡽࠨ๼").format(bstack11ll_opy_));
  except Exception as e:
    logger.debug(bstack111l11ll_opy_.format(str(e)))
def bstack11l11ll1l_opy_(bstack1l1111l11_opy_):
  global CONFIG
  try:
    host = bstack1ll1_opy_ (u"࠭ࡡࡱ࡫࠰ࡧࡱࡵࡵࡥࠩ๽") if bstack1ll1_opy_ (u"ࠧࡢࡲࡳࠫ๾") in CONFIG else bstack1ll1_opy_ (u"ࠨࡣࡳ࡭ࠬ๿")
    user = CONFIG[bstack1ll1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ຀")]
    key = CONFIG[bstack1ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ກ")]
    bstack1111lll_opy_ = bstack1ll1_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪຂ") if bstack1ll1_opy_ (u"ࠬࡧࡰࡱࠩ຃") in CONFIG else bstack1ll1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨຄ")
    url = bstack1ll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡽࢀ࠾ࢀࢃࡀࡼࡿ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡹࡥࡴࡵ࡬ࡳࡳࡹ࠮࡫ࡵࡲࡲࠬ຅").format(user, key, host, bstack1111lll_opy_, bstack1l1111l11_opy_)
    headers = {
      bstack1ll1_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧຆ"): bstack1ll1_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬງ"),
    }
    proxies = bstack1lll11l11_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack1ll1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨຈ")], response.json()))
  except Exception as e:
    logger.debug(bstack1l1l11l1_opy_.format(str(e)))
def bstack11111l11_opy_():
  global CONFIG
  try:
    if bstack1ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧຉ") in CONFIG:
      host = bstack1ll1_opy_ (u"ࠬࡧࡰࡪ࠯ࡦࡰࡴࡻࡤࠨຊ") if bstack1ll1_opy_ (u"࠭ࡡࡱࡲࠪ຋") in CONFIG else bstack1ll1_opy_ (u"ࠧࡢࡲ࡬ࠫຌ")
      user = CONFIG[bstack1ll1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪຍ")]
      key = CONFIG[bstack1ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬຎ")]
      bstack1111lll_opy_ = bstack1ll1_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩຏ") if bstack1ll1_opy_ (u"ࠫࡦࡶࡰࠨຐ") in CONFIG else bstack1ll1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧຑ")
      url = bstack1ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡻࡾ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠯࡬ࡶࡳࡳ࠭ຒ").format(user, key, host, bstack1111lll_opy_)
      headers = {
        bstack1ll1_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭ຓ"): bstack1ll1_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫດ"),
      }
      if bstack1ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫຕ") in CONFIG:
        params = {bstack1ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨຖ"):CONFIG[bstack1ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧທ")], bstack1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨຘ"):CONFIG[bstack1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨນ")]}
      else:
        params = {bstack1ll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬບ"):CONFIG[bstack1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫປ")]}
      proxies = bstack1lll11l11_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack111l1l11_opy_ = response.json()[0][bstack1ll1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡢࡶ࡫࡯ࡨࠬຜ")]
        if bstack111l1l11_opy_:
          bstack11l1111_opy_ = bstack111l1l11_opy_[bstack1ll1_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥࡢࡹࡷࡲࠧຝ")].split(bstack1ll1_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦ࠱ࡧࡻࡩ࡭ࡦࠪພ"))[0] + bstack1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡷ࠴࠭ຟ") + bstack111l1l11_opy_[bstack1ll1_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩຠ")]
          logger.info(bstack1l11l11l_opy_.format(bstack11l1111_opy_))
          bstack1l11lll1l_opy_ = CONFIG[bstack1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪມ")]
          if bstack1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪຢ") in CONFIG:
            bstack1l11lll1l_opy_ += bstack1ll1_opy_ (u"ࠩࠣࠫຣ") + CONFIG[bstack1ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ຤")]
          if bstack1l11lll1l_opy_!= bstack111l1l11_opy_[bstack1ll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩລ")]:
            logger.debug(bstack1ll1l1lll_opy_.format(bstack111l1l11_opy_[bstack1ll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ຦")], bstack1l11lll1l_opy_))
          return [bstack111l1l11_opy_[bstack1ll1_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩວ")], bstack11l1111_opy_]
    else:
      logger.warn(bstack1lll11lll_opy_)
  except Exception as e:
    logger.debug(bstack11ll11ll_opy_.format(str(e)))
  return [None, None]
def bstack1l11l_opy_(url, bstack11lll1ll_opy_=False):
  global CONFIG
  global bstack11l1l1ll1_opy_
  if not bstack11l1l1ll1_opy_:
    hostname = bstack1l1lll1l_opy_(url)
    is_private = bstack1lll1ll11_opy_(hostname)
    if (bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫຨ") in CONFIG and not CONFIG[bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬຩ")]) and (is_private or bstack11lll1ll_opy_):
      bstack11l1l1ll1_opy_ = hostname
def bstack1l1lll1l_opy_(url):
  return urlparse(url).hostname
def bstack1lll1ll11_opy_(hostname):
  for bstack1l1111_opy_ in bstack111lll1_opy_:
    regex = re.compile(bstack1l1111_opy_)
    if regex.match(hostname):
      return True
  return False