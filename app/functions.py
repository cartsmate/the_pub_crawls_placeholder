import io
import json
import uuid
import boto3
import numpy as np
import pandas as pd
from app import *
from .config import Configurations

config = Configurations().get_config()


class Functions:

    def generate_uuid(self):
        new_id = str(uuid.uuid4())
        return new_id

    def df_to_dict(self, df):
        df_dict = df.to_dict(orient='records')
        return df_dict

    def get_records(self, aws_prefix, list_of_columns):
        df = self.read_s3_csv_to_df(aws_prefix, list_of_columns)
        del_consol = aws_prefix + "_deletion"
        df_false = df.loc[df[del_consol] != True]
        return df_false

    def get_pubs(self):
        df_pubs = self.get_records(constants.get("Aws_prefix", "PUB"), json.loads(constants.get("Columns", "PUB")))
        return df_pubs

    def get_pubs_station(self):
        df_pubs = self.get_pubs()
        df_stations = self.get_stations()
        df_stations = df_stations[['station_identity', 'station']]
        df_pubs_station = pd.merge(df_pubs, df_stations, how='left', on='station_identity')
        return df_pubs_station

    def get_pubs_by_star(self, star_id):
        # print(star)
        df_pubs_reviews = self.get_pubs_reviews()
        # print(df_pubs_reviews)
        df_pubs_by_star = df_pubs_reviews.loc[df_pubs_reviews['star'] == star_id]
        # print(df_pubs_by_star)
        return df_pubs_by_star

    def get_pubs_by_category(self, cat_id):
        df_pubs_reviews = self.get_pubs_reviews()
        df_pubs_by_category = df_pubs_reviews.loc[df_pubs_reviews['category'] == cat_id]
        return df_pubs_by_category

    def get_pubs_by_station(self, loc_id):
        df_pubs_reviews = self.get_pubs_reviews()
        df_pubs_by_station = df_pubs_reviews.loc[df_pubs_reviews['station'] == loc_id]
        return df_pubs_by_station

    def get_reviews(self):
        df_reviews = self.get_records(constants.get("Aws_prefix", "REVIEW"),
                                      json.loads(constants.get("Columns", "REVIEW")))
        return df_reviews

    def get_stations(self):
        df_stations = self.get_records(constants.get("Aws_prefix", "STATION"),
                                       json.loads(constants.get("Columns", "STATION")))
        return df_stations

    def get_pubs_reviews(self):
        # print('get_pubs_reviews')
        df_pubs_reviews = pd.merge(self.get_pubs_station(), self.get_reviews(), how='left', on='pub_identity')
        df_pubs_reviews['score'] = df_pubs_reviews.loc[:, ['atmosphere', 'cleanliness', 'clientele', 'decor',
                                                           'entertainment', 'food', 'friendliness', 'opening', 'price',
                                                           'selection']].sum(axis=1)
        df_pubs_reviews['colour'] = np.where(df_pubs_reviews['reviewer'] == 'BOTH', constants.get("Colours", "RED"),
                                             np.where(df_pubs_reviews['reviewer'] == 'ANDY',
                                                      constants.get("Colours", "RED"),
                                                      np.where(df_pubs_reviews['reviewer'] == 'AVNI',
                                                               constants.get("Colours", "RED"),
                                                               constants.get("Colours", "NEW"))))
        # df_pubs_reviews['colour'] = constants.get("Colours", "RED")
        df_pubs_reviews.fillna(0, inplace=True)
        # print(df_pubs_reviews)
        #     .drop(columns=['deletion_x', 'identity_y', 'deletion_y']) \
        #     .rename(columns={'identity_x': 'identity'})
        return df_pubs_reviews

    def get_record(self, dfs, id_code):
        df = dfs.loc[dfs['pub_identity'] == id_code]
        return df

    def get_pub_station(self, id_code):
        df_pub = self.get_pub(id_code)
        df_stations = self.get_stations()
        df_stations = df_stations[['station_identity', 'station']]
        df_pub_station = pd.merge(df_pub, df_stations, how='left', on='station_identity')
        return df_pub_station

    def get_pub(self, id_code):
        df_pub = self.get_record(self.get_records(constants.get("Aws_prefix", "PUB"),
                                                  json.loads(constants.get("Columns", "PUB"))), id_code)
        return df_pub

    def get_review(self, pub_id):
        df_reviews = self.get_records(constants.get("Aws_prefix", "REVIEW"),
                                      json.loads(constants.get("Columns", "REVIEW")))
        df_review = df_reviews.loc[df_reviews['pub_identity'] == pub_id]
        return df_review

    def get_pub_review(self, id_code):
        df_pub_review = pd.merge(self.get_pub_station(id_code), self.get_review(id_code), how='left', on='pub_identity')

        df_pub_review['score'] = df_pub_review.loc[:, ['atmosphere', 'cleanliness', 'clientele', 'decor',
                                                       'entertainment', 'food', 'friendliness', 'opening', 'price',
                                                       'selection']].sum(axis=1)
        df_pub_review['colour'] = np.where(df_pub_review['reviewer'] == 'BOTH', constants.get("Colours", "RED"),
                                           np.where(df_pub_review['reviewer'] == 'ANDY',
                                                    constants.get("Colours", "RED"),
                                                    np.where(df_pub_review['reviewer'] == 'AVNI',
                                                             constants.get("Colours", "RED"),
                                                             constants.get("Colours", "NEW"))))
        return df_pub_review

    def write_csv_to_s3(self, upload_object: object, s3_obj_name: object) -> object:
        client = boto3.client("s3", aws_access_key_id=config['access_id'], aws_secret_access_key=config['access_key'])
        client.put_object(Body=upload_object, Bucket=config['bucket_name'], Key=s3_obj_name)
        s3_resp = client.head_object(Bucket=config['bucket_name'], Key=s3_obj_name)
        return s3_resp

    def read_s3_csv_to_df(self, prefix, list_of_columns):
        s3 = boto3.resource('s3',
                            aws_access_key_id=config['access_id'],
                            aws_secret_access_key=config['access_key'])
        my_bucket = s3.Bucket(config['bucket_name'])
        bucket_list = []
        for obj in my_bucket.objects.filter(Prefix=prefix):  # .all():
            # print('file: ' + str(obj))
            if obj.key.find(".csv") != -1:
                # print(obj.key)
                bucket_list.append(obj.key)
        # print('bucket_list: ' + str(bucket_list))
        if len(bucket_list) == 1:
            list_of_objects = []  # Initializing empty list of dataframes
            for bucket in bucket_list:  # pubs.csv
                # print('file: ' + file)
                obj = s3.Object(config['bucket_name'], bucket)
                # print('obj: ' + str(obj))  # key='pubs.csv'
                data = obj.get()['Body'].read()
                # print('data: ' + str(data))   #file in bytes
                list_of_objects.append(pd.read_csv(io.BytesIO(data), header=0, delimiter=",", low_memory=False))
            obj_df = pd.DataFrame(columns=list_of_columns)
            # print('obj_df: ' + obj_df)
            for obj in list_of_objects:
                # print(obj)
                temp_df = pd.DataFrame(data=obj)
                obj_df = pd.DataFrame(np.concatenate([obj_df.values, temp_df.values]), columns=obj_df.columns)
        else:
            obj_df = None
            print('error in processing')
        return obj_df
