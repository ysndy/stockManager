import pandas as pd
import pandas_datareader.data as web
import datetime
import time


def test2():
    start_time = time.time()
    start = datetime.datetime(2019, 2, 20)
    end = datetime.datetime(2020, 10, 8)
    gs = web.DataReader('078930.KS', 'yahoo')
    ma5 = gs['Close'].rolling(window=5).mean()
    print(ma5)
    print("time :", time.time() - start_time)


def test1():
    start_time = time.time()
    code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]

    # 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌
    code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)

    # 우리가 필요한 것은 회사명과 종목코드이기 때문에 필요없는 column들은 제외해준다.
    code_df = code_df[['회사명', '종목코드']]

    # 한글로된 컬럼명을 영어로 바꿔준다.

    code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})

    # print(code_df)

    def get_url(item_name, code_df):
        code = code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False)
        code = code.replace(" ", "", 1)
        print(code)
        url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
        print("요청 URL = {}".format(url))
        return url

    # 신라젠의 일자데이터 url 가져오기
    item_name = 'HMM'
    url = get_url(item_name, code_df)

    # 일자 데이터를 담을 df라는 DataFrame 정의
    df = pd.DataFrame()

    # 1페이지에서 20페이지의 데이터만 가져오기
    for page in range(1, 31):
        pg_url = '{url}&page={page}'.format(url=url, page=page)
        df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)

    # df.dropna()를 이용해 결측값 있는 행 제거
    df = df.dropna()

    # 상위 5개 데이터 확인하기

    ma20 = df['종가'].rolling(window=5).mean()
    print(ma20)
    print("time :", time.time() - start_time)
    # https://excelsior-cjh.tistory.com/109 [EXCELSIOR]
