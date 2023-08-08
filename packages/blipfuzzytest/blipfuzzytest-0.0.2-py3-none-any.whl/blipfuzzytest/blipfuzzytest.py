import requests
import pandas as pd
import json
from tqdm import tqdm

class blipfuzzytest:

  urls = {'menu':'https://fuzzymatch.cs.blip.ai/api/v2/fuzzy-match/','map':'https://fuzzymatch.cs.blip.ai/api/v2/fuzzy-match/map'}
  methods = ["default", "ratio", "partialRatio", "tokenSet", "partialTokenSet", "tokenSort", "partialTokenSort", "tokenAbbreviation", "partialTokenAbbreviation"]

  def __init__(self, authorization, organization):
    self.header = {'accept': 'application/json', 'authorization': authorization, 'organization': organization, "Content-Type": "application/json-patch+json"}

  def run_onemethod_file(self, file_df, method, score_threshold):
    df_full = pd.DataFrame(columns= ['input', 'expectedMatch', 'method', 'matchScore', 'reliableMatch', 'matchCategory', 'map_matchElement', 'menu_menuOption', 'expectedResult']) #matchCategory = match.category (map) ou match.menuDescription (menu)

    for idx, row in tqdm(file_df.iterrows()):
      if isinstance(row[3], str):
        #montando o map
        map_keys = [element.strip() for element in row[2].split(',')]
        counter_map_values = 0
        map = {}
        while counter_map_values < len(map_keys):
          map.update({map_keys[counter_map_values] : [element.strip() for element in row[counter_map_values + 3].split(',')]})
          counter_map_values += 1

        body_unit = {"map": map, "userInput": row[0], "fuzzyMethod": method, "scoreThreshold": score_threshold} #montando o corpo
        result = self.fuzzy_call(self.urls['map'], body_unit) #fazendo a chamada
        result_match_category = True if row[1].strip() == result['match']['category'] or row[1].strip() == result['match']['element'] else False #validando se o retorno é igual ao resultado esperado
        #montando a próxima linha do df final
        df_unit = pd.DataFrame([{'input': row[0],
                                 'expectedMatch': row[1],
                                 'method': method,
                                 'matchScore': result['match']['score'],
                                 'reliableMatch': result['reliableMatch'],
                                 'matchCategory': result['match']['category'],
                                 'map_matchElement': result['match']['element'],
                                 'menu_menuOption': None,
                                 'expectedResult': result_match_category}])

        df_full = pd.concat([df_full, df_unit])

      else:
        menu = [element.strip() for element in row[2].split(',')] #montando o menu
        body_unit = {"menu": menu, "userInput": row[0], "fuzzyMethod": method, "scoreThreshold": score_threshold} #montando o corpo
        result = self.fuzzy_call(self, self.urls['menu'], body_unit) #fazendo a chamada

        if 'menuOption' in result['match']:
          result_match_category = True if row[1] == result['match']['menuDescription'] or row[1] == result['match']['menuOption'] else False #validando se o retorno é igual ao resultado esperado
          menu_option = result['match']['menuOption']
        else:
          result_match_category = True if row[1] == result['match']['menuDescription'] else False #validando se o retorno é igual ao resultado esperado
          menu_option = None

        #montando a próxima linha do df final
        df_unit = pd.DataFrame([{'input': row[0],
                                 'expectedMatch': row[1],
                                 'method': method,
                                 'matchScore': result['match']['score'],
                                 'reliableMatch': result['reliableMatch'],
                                 'matchCategory': result['match']['menuDescription'],
                                 'map_matchElement': None,
                                 'menu_menuOption': menu_option,
                                 'expectedResult': result_match_category}])

        df_full = pd.concat([df_full, df_unit])

    df_full.reset_index(drop=True, inplace=True)
    print('A distribuição de Acertos e Erros para as previsões é de:', df_full['expectedResult'].value_counts(normalize=True).mul(100).astype(str)+'%')
    return df_full

  def run_allmethods_file(self, file_df, score_threshold):
    df_full = pd.DataFrame(columns= ['input', 'expectedMatch', 'method', 'matchScore', 'reliableMatch', 'matchCategory', 'map_matchElement', 'menu_menuOption', 'expectedResult']) #matchCategory = match.category (map) ou match.menuDescription (menu)

    for idx, row in tqdm(file_df.iterrows()):
      if isinstance(row[3], str):
        #montando o map
        map_keys = [element.strip() for element in row[2].split(',')]
        counter_map_values = 0
        map = {}
        while counter_map_values < len(map_keys):
          map.update({map_keys[counter_map_values] : [element.strip() for element in row[counter_map_values + 3].split(',')]})
          counter_map_values += 1

        for method in self.methods:
          body_unit = {"map": map, "userInput": row[0], "fuzzyMethod": method, "scoreThreshold": score_threshold} #montando o corpo
          result = self.fuzzy_call(self, self.urls['map'], body_unit) #fazendo a chamada
          result_match_category = True if row[1].strip() == result['match']['category'] or row[1].strip() == result['match']['element'] else False #validando se o retorno é igual ao resultado esperado
          #montando a próxima linha do df final
          df_unit = pd.DataFrame([{'input': row[0],
                                  'expectedMatch': row[1],
                                  'method': method,
                                  'matchScore': result['match']['score'],
                                  'reliableMatch': result['reliableMatch'],
                                  'matchCategory': result['match']['category'],
                                  'map_matchElement': result['match']['element'],
                                  'menu_menuOption': None,
                                  'expectedResult': result_match_category}])

          df_full = pd.concat([df_full, df_unit])

      else:
        menu = [element.strip() for element in row[2].split(',')] #montando o menu

        for method in tqdm(self.methods):
          body_unit = {"menu": menu, "userInput": row[0], "fuzzyMethod": method, "scoreThreshold": score_threshold} #montando o corpo
          result = self.fuzzy_call(self, self.urls['menu'], body_unit) #fazendo a chamada

          if 'menuOption' in result['match']:
            result_match_category = True if row[1] == result['match']['menuDescription'] or row[1] == result['match']['menuOption'] else False #validando se o retorno é igual ao resultado esperado
            menu_option = result['match']['menuOption']
          else:
            result_match_category = True if row[1] == result['match']['menuDescription'] else False #validando se o retorno é igual ao resultado esperado
            menu_option = None

          #montando a próxima linha do df final
          df_unit = pd.DataFrame([{'input': row[0],
                                  'expectedMatch': row[1],
                                  'method': method,
                                  'matchScore': result['match']['score'],
                                  'reliableMatch': result['reliableMatch'],
                                  'matchCategory': result['match']['menuDescription'],
                                  'map_matchElement': None,
                                  'menu_menuOption': menu_option,
                                  'expectedResult': result_match_category}])

          df_full = pd.concat([df_full, df_unit])

    df_full.reset_index(drop=True, inplace=True)
    print('A distribuição de Acertos e Erros para as previsões é de:', df_full['expectedResult'].value_counts(normalize=True).mul(100).astype(str)+'%')
    return df_full

  def run_onemethod_map(self, inputs, method, score_threshold, map):
      body_list = []
      method_list = []

      for input in inputs:
        body_unit = {"map": map, "userInput": input, "fuzzyMethod": method, "scoreThreshold": score_threshold}
        body_list.append(body_unit)
        method_list.append(method)

      results = []
      for body in tqdm(body_list):
        result = self.fuzzy_call(self.urls['map'], body)
        results.append(result)

      df_processed = pd.json_normalize(results)
      df_processed.insert(loc=1, column='method', value=method_list)
      return df_processed

  def run_allmethods_map(self, inputs, score_threshold, map):
     body_list = []
     method_list = []
     results = []

     for input in inputs:
        for method in self.methods:
          body_unit = {"map": map, "userInput": input, "fuzzyMethod": method, "scoreThreshold": score_threshold}
          body_list.append(body_unit)  #talvez já chamar a API aqui
          #print(json.dumps(body_unit))
          method_list.append(method)

     for body in tqdm(body_list):
      result = self.fuzzy_call(self.urls['map'], body)
      results.append(result)
      #print(result)
     df_processed = pd.json_normalize(results)
     df_processed.insert(loc=1, column='method', value=method_list)
     return df_processed

  def fuzzy_call(self, url, body):
     result = requests.post(url=url, headers=self.header, json=body).json()
     if result == {'message': 'No match was found'}:
       result = {'input': body['userInput'], 'match': {'category': 'No match was found', 'element': 'No match was found', 'score': 0}, 'reliableMatch': False}
     return result

  def test_onemethod_menu(self, menu, userInput, score, method=None):
    myobj = {
      "menu": menu,
      "userInput": userInput,
      "scoreThreshold":score,
      "fuzzyMethod":method
  }

    result = self.fuzzy_call(self.urls['menu'], myobj)
    result['method'] = method
    return(result)

  def test_allmethods_menu(self, menu, userInput, score, method=None):
      y = []
      for m in tqdm(self.methods):
        myobj = {
          "menu": menu,
          "userInput": userInput,
          "scoreThreshold":score,
          "fuzzyMethod":m
      }

        result = self.fuzzy_call(self.urls['menu'], myobj)
        #result['method'] = str(m)
        y.append(result)
      return(y)

  def run_onemethod_menu(self, menu, inputs, score, method):
    result = [self.test_onemethod_menu(menu, input, score, method) for input in tqdm(inputs)]
    df = pd.DataFrame(result)
    for m in range(len(df)):
      df['menuDescription'] = df.match[m]['menuDescription']
      df['menuOption'] = df.match[m]['menuOption'] if 'menuOption' in df.match[m] else None
      df['score'] = df.match[m]['score']
    df = df.drop(columns=['match'])
    return(df)

  def run_allmethods_menu(self, menu, inputs, score):
    result = [pd.DataFrame(self.test_allmethods_menu(menu, input, score)) for input in tqdm(inputs)]
    df = pd.concat(result)
    df = df.reset_index()
    for m in range(len(df)):
      df['menuDescription'] = df.match[m]['menuDescription']
      df['menuOption'] = df.match[m]['menuOption'] if 'menuOption' in df.match[m] else None
      df['score'] = df.match[m]['score']
    df = df.drop(columns=['match','index'])
    df = df.set_index(['input', 'method'])
    return(df)