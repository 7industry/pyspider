#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from service.market_service import MarketService
# from headless.kabumap import Kabumap
# from headless.kabuyoho import Kabuyoho
# from headless.minkabu import Minkabu
# from headless.nikkei import Nikkei
# from headless.reuters import Reuters
# from headless.toyokeizai import Toyokeizai
# from headless.yahoo import Yahoo
# from model.SchemaModel import EquityProfile

MarketService.batch_down()

# Kabumap.update_equity_statistics('6659')
# Nikkei.update_equity_statistics('6659')
# Kabuyoho.update_equity_statistics('6659')
# Minkabu.update_equity_statistics('6659')
# Yahoo.update_equity_statistics('6659')

# Reuters.update_equity_statistics('6659')

# Toyokeizai.update_equity_statistics('6659')