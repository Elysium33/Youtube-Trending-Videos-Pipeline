from api_functions import *
from credentials import db_pass, db_name, db_user
import sqlalchemy




if __name__ == '__main__':
    region_codes = ['US', 'CA', 'DE', 'FR', 'GB', 'IN', 'JP', 'KR', 'MX', 'RU']

    engine = sqlalchemy.create_engine(f'postgresql+psycopg2://{db_user}:{db_pass}@localhost:5432/{db_name}')

    for code in region_codes:

        next_page_token = ""
        data_list_1, next_page_token = get_videos(code, next_page_token)

        data_list_2 = get_videos(code, next_page_token)[0]

        df = pd.DataFrame(data_list_1)
        df_2 = pd.DataFrame(data_list_2)

        df = pd.concat([df, df_2], ignore_index=True)
        

        df.to_sql(
            name = f'youtube_trending_data_{code}',
            con = engine,
            index = False,
            if_exists = 'append'
        )
        print(f"{code} data has been added to database.")