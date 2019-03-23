# -*- coding: utf-8 -*-

import requests
import pandas as pd

STEAM_APPLIST_URL = 'https://api.steampowered.com/ISteamApps/GetAppList/v2/'


class AppList():
    """ Class used to query appid from app list """

    def __init__(self):
        self.applist = None

    def populate_app_list(self):
        """ Populate list of apps from Steam """

        try:
            json_app_list = self._request_json_list()
            self.applist = pd.DataFrame(json_app_list)
            self.applist.sort_values(by=['appid'], inplace=True)

        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
        
        return self

    def get_app_name(self, appid):
        """
        Return appname from appid

        Call example:
            AppList().populate_app_list().get_app_name(500)

        Returns:
              App_name (str) is found
              None otherwise
        """

        if self.applist is None:
            print('Call get_app_list first!')
            return None

        if self._is_id_valid(appid):
            app_index = self._loc_app_id(appid)
            app_name = str(app_index.values[0])
            return app_name
        else:
            print('AppID {} does not exist'.format(appid))
            return None

    def _loc_app_id(self, appid):
        return self.applist.loc[self.applist['appid'] == appid, 'name']

    def _request_json_list(self):
        return requests.get(STEAM_APPLIST_URL).json()['applist']['apps']

    def _is_id_valid(self, appid):
        return (appid in self.applist['appid'].values)
