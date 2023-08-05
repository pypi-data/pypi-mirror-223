# -*- coding: utf-8 -*-
#
# Copyright 2017 MindGo, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


__config__ = {
    "signal_mode": True,  # 模拟交易信号模式，否则直接下单
    "persist_path": "./persist/strategy/",
    "trade_api": None,
}


def load_mod():
    from .mod import RealtimeTradeMod
    return RealtimeTradeMod()
