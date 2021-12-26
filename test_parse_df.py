import pandas as pd


class Client:

    def load_data(self):
        data = [
            {'lang': 'en', 'region': 'us', 'type': 'news',
             'value': 'domain', 'end': {'www.a': {'channel': 'a', 'child': 'a'}}},
            {'lang': 'en', 'region': 'us', 'type': 'news',
             'value': 'domain', 'end': {'www.a1': {'channel': 'a1', 'child': 'a1'}}},
            {'lang': 'en', 'region': 'us', 'type': 'news',
             'value': 'url_prefix', 'end': {'www.b': {'channel': 'b', 'child': 'b'}}},
            {'lang': 'en', 'region': 'us', 'type': 'news',
             'value': 'url_prefix', 'end': {'www.b1': {'channel': 'b1', 'child': 'b1'}}},
            {'lang': 'en', 'region': 'us', 'type': 'news',
             'value': 'pre_url', 'end': {'www.c': {'channel': 'c', 'child': 'c'}}},
            {'lang': 'en', 'region': 'us', 'type': 'news',
             'value': 'pre_url', 'end': {'www.c1': {'channel': 'c1', 'child': 'c1'}}},
            {'lang': 'en', 'region': 'us', 'type': 'video',
             'value': 'domain', 'end': {'www.d': {'channel': 'd', 'child': 'd'}}},
            {'lang': 'en', 'region': 'us', 'type': 'video',
             'value': 'domain', 'end': {'www.e': {'channel': 'e', 'child': 'e'}}},
            {'lang': 'en', 'region': 'us', 'type': 'video',
             'value': 'domain', 'end': {'www.f': {'channel': 'f', 'child': 'f'}}},
            {'lang': 'en', 'region': 'sg', 'type': 'news',
             'value': 'domain', 'end': {'www.g': {'channel': 'g', 'child': 'g'}}},
            {'lang': 'en', 'region': 'sg', 'type': 'news',
             'value': 'url_prefix', 'end': {'www.h': {'channel': 'h', 'child': 'h'}}},
            {'lang': 'en', 'region': 'sg', 'type': 'video',
             'value': 'pre_url', 'end': {'www.i': {'channel': 'i', 'child': 'i'}}},
            {'lang': 'en', 'region': 'sg', 'type': 'video',
             'value': 'domain', 'end': {'www.j': {'channel': 'j', 'child': 'j'}}},
            {'lang': 'en', 'region': 'sg', 'type': 'video',
             'value': 'url_prefix', 'end': {'www.k': {'channel': 'k', 'child': 'k'}}},
            {'lang': 'zh', 'region': 'ch', 'type': 'news',
             'value': 'domain', 'end': {'www.l': {'channel': 'l', 'child': 'l'}}},
            {'lang': 'zh', 'region': 'ch', 'type': 'video',
             'value': 'pre_url', 'end': {'www.m': {'channel': 'm', 'child': 'm'}}},
            {'lang': 'zh', 'region': 'ch', 'type': 'video',
             'value': 'pre_url', 'end': {'www.n': {'channel': 'n', 'child': 'n'}}},
        ]
        df = pd.DataFrame(data)
        return df

    def _combine_list(self, sr, field):
        ends = sr[field]
        ret = {}
        for end in ends:
            ret.update(end)
        return ret

    def _combine_filed(self, sr, key_field, value_field):
        key = sr[key_field]
        value = sr[value_field]
        return {key: value}

    def _process_end_df(self, df):
        df = df.groupby(['lang', 'region', 'type', 'value'])['end'].apply(list).reset_index()
        df['end'] = df.apply(lambda x: self._combine_list(x, 'end'), axis=1)
        return df

    def _process_value_df(self, df):
        grouped_value = df.groupby('value')
        df = grouped_value.apply(self._process_end_df).reset_index(drop=True)
        df['value'] = df.apply(lambda x: self._combine_filed(x, 'value', 'end'), axis=1)
        del df['end']
        df = df.groupby(['lang', 'region', 'type'])['value'].apply(list).reset_index()
        df['value'] = df.apply(lambda x: self._combine_list(x, 'value'), axis=1)
        return df

    def _process_type_df(self, df):
        grouped_type = df.groupby('type')
        df = grouped_type.apply(self._process_value_df).reset_index(drop=True)
        df['type'] = df.apply(lambda x: self._combine_filed(x, 'type', 'value'), axis=1)
        del df['value']
        df = df.groupby(['lang', 'region'])['type'].apply(list).reset_index()
        df['type'] = df.apply(lambda x: self._combine_list(x, 'type'), axis=1)
        return df

    def _process_lang_df(self, df):
        grouped_region = df.groupby('region')
        df = grouped_region.apply(self._process_type_df).reset_index(drop=True)
        df['region'] = df.apply(lambda x: self._combine_filed(x, 'region', 'type'), axis=1)
        del df['type']
        df = df.groupby('lang')['region'].apply(list).reset_index()
        df['region'] = df.apply(lambda x: self._combine_list(x, 'region'), axis=1)
        return df

    def execute(self):
        df = self.load_data()
        grouped_lang = df.groupby('lang')
        df = grouped_lang.apply(self._process_lang_df).reset_index(drop=True)
        df['lang'] = df.apply(lambda x: self._combine_filed(x, 'lang', 'region'), axis=1)
        del df['region']
        langs = df['lang'].to_list()
        ret = {}
        for lang in langs:
            ret.update(lang)
        return ret


if __name__ == '__main__':
    import json

    client = Client()
    ret = client.execute()
    with open('white.json', 'w') as f:
        json.dump(ret, f, indent=2)
