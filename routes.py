import os
import json
import uuid
import pandas as pd
from flask import Blueprint, render_template, request, redirect, url_for
from configparser import ConfigParser
from config import Configurations
from functions import Functions
from models.review import Review

directory_path = os.getcwd()
constants = ConfigParser()
constants.read(directory_path + "/constants.ini")
config = Configurations().get_config()
function = Functions()
home_blueprint = Blueprint()


# @app.route("/testbed")
# def testbed():
#     print('/testbed')
#     return render_template('testbed.html')


# @app.route("/")
# @app.route("/index")
# def index():
#     print('/index')
#     photo_array = json.loads(constants.get("Columns", "SCORE"))
#     return render_template('index.html', photo_array=photo_array, map_view="stations", map_lat=51.5, map_lng=-0.1,
#                            row_loop=range(3), col_loop=range(4))


@the_pub_crawls.route("/pub/map")
def pub_map():
    print('/pub/map')
    df_stations = function.get_stations()
    df_pubs_stations = pd.merge(function.get_pubs(), df_stations, how='left', on='station')
    df_truncated = pd.DataFrame().assign(name=df_pubs_stations['name'], station=df_pubs_stations['station'])
    df_result = df_truncated.groupby(['station'], as_index=False).count()
    df_result_latlng = pd.merge(df_result, df_stations, how='left', on='station')
    df_sorted = df_result_latlng.rename(columns={'name': 'count'}).astype(str)
    # sort_values(by='count', ascending=False)
    # print(df_sorted)

    df_sorted['colour'] = constants.get("Colours", "RED")
    stations_json = function.df_to_dict(df_sorted)

    pubs_reviews_json = function.df_to_dict(function.get_pubs_reviews())
    view="venues"
    return render_template('pub_map.html', google_key=config['google_key'], stations=stations_json,
                           pubs_reviews=pubs_reviews_json, icon_hole=True, info_box=True, map_view=view)


# @app.route("/pub/map/stations")
# def map_stations():
#     print('/pub/map/stations')
#     df_stations = function.get_stations()
#     df_pubs = function.get_pubs()
#     df_pubs_reviews = function.get_pubs_reviews()
#     df_reviewed_only = df_pubs_reviews.loc[df_pubs_reviews['colour'] != constants.get("Colours", "NEW")]
#     # df_pubs_stations = pd.merge(get_pubs(), df_stations, how='left', on='station_identity')
#     df_pubs_station = function.get_pubs_station()
#     # df_truncated = pd.DataFrame().assign(name=df_pubs_station['name'], station=df_pubs_station['station_identity'])
#     df_truncated = df_reviewed_only[['name', 'station_identity']]
#     df_result = df_truncated.groupby(['station_identity'], as_index=False).count()
#
#     df_result_latlng = pd.merge(df_result, df_stations, how='left', on='station_identity')
#     df_sorted = df_result_latlng.rename(columns={'name': 'count'}).astype(str)
#     df_sorted['colour'] = constants.get("Colours", "RED")
#     stations_json = function.df_to_dict(df_sorted)
#     pubs_reviews_json = function.df_to_dict(df_pubs_reviews)
#     view = "stations"
#     return render_template('pub_map.html', google_key=config['google_key'], stations=stations_json,
#                            pubs_reviews=pubs_reviews_json, icon_hole=False,
#                            info_box=False, map_view=view, map_lat=51.5, map_lng=-0.1)

@the_pub_crawls.route("/pub/list")
def pub_list():
    print('/pub/list')
    # pubs_json = df_to_dict(get_pubs())
    pubs_reviews = function.get_pubs_reviews().sort_values(by=['score'], ascending=False)
    dfxx = pubs_reviews.loc[pubs_reviews['star'] == 0]
    print(dfxx[['star']])
    pubs_reviews_json = function.df_to_dict(pubs_reviews)
    view = "list"
    return render_template('pub_list.html', pubs_reviews=pubs_reviews_json, map_view=view, map_lat=51.5, map_lng=-0.1)


# @app.route("/pub/add/")
# def pub_add():
#     print('/pub/add')
#     stations_json = function.df_to_dict(function.get_records(constants.get("Aws_prefix", "STATION"),
#                                            json.loads(constants.get("Columns", "STATION"))))
#
#     new_pub_id = str(generate_uuid())
#     date_now = date.today().strftime("%B %d, %Y")
#
#     add_pub = Pub(pub_identity=new_pub_id, pub_deletion=False, place="", name="", address="", latitude=51.5,
#                   longitude=-0.1, station_identity="", category="")
#
#     add_review = Review(review_identity=str(generate_uuid()), pub_identity=new_pub_id, review_deletion=False,
#                         visit=date_now,
#                         star="", atmosphere=0, cleanliness=0, clientele=0, decor=0, entertainment=0, food=0,
#                         friendliness=0, opening=0, price=0, selection=0, reviewer="")
#     df_pub_review = pd.merge(pd.DataFrame([add_pub.__dict__]), pd.DataFrame([add_review.__dict__]), on='pub_identity')
#     pub_review_json = function.df_to_dict(df_pub_review)
#     pubs_reviews_json = function.df_to_dict(function.get_pubs_reviews())
#     return render_template("pub_add.html", google_key=config['google_key'], pubs_reviews=pubs_reviews_json,
#                            pub_review=pub_review_json, stations=stations_json,
#                            pub_review_fields=json.loads(constants.get("Columns", "PUB_REVIEW")),
#                            list_visible=json.loads(constants.get("Columns", "REVIEW_VISIBLE")),
#                            list_required=json.loads(constants.get("Columns", "REQUIRED")))


# @app.route("/pub/<pub_id>", methods=['GET', 'POST'])
# def pub(pub_id):
#     print('/pub/<pub_id>')
#     # try:
#     # df_pub = get_pub(pub_id)
#     # df_review = get_review(pub_id)
#     df_pub_review = function.get_pub_review(pub_id)
#     if request.method == 'GET':
#         print('/pub/<pub_id>/GET')
#         # pub_json = df_to_dict(df_pub)
#         # df_pub_review = get_pub_review(pub_id)
#         pub_review_json = function.df_to_dict(df_pub_review)
#         # pub_json = df_to_dict(df_pub)
#         # if df_review.empty:
#         #     print('NO REVIEW')
#         return render_template("pub_read.html", google_key=config['google_key'],
#                                pub_review=pub_review_json,
#                                # pub_fields=json.loads(constants.get("Columns", "PUB")),
#                                # review_fields=json.loads(constants.get("Columns", "REVIEW")),
#                                pub_review_fields=json.loads(constants.get("Columns", "PUB_REVIEW")),
#                                list_visible=json.loads(constants.get("Columns", "REVIEW_VISIBLE")))
#         # else:
#         # #     review_json = df_to_dict(df_review)
#         # #     print('HAS REVIEW')
#         #     return render_template("pub_read.html", google_key=config['google_key'],
#         #                            pub_review=pub_review_json, pub=pub_json,
#         #                            pub_fields=json.loads(constants.get("Columns", "PUB")),
#         #                            review_fields=json.loads(constants.get("Columns", "REVIEW")),
#         #                            pub_review_fields=json.loads(constants.get("Columns", "PUB_REVIEW")),
#         #                            list_visible=json.loads(constants.get("Columns", "REVIEW_VISIBLE")))
#     if request.method == 'POST':
#         print('/pub/<id_code>/POST')
#         new_pub = Pub(pub_identity=pub_id, pub_deletion=request.form['pub_deletion'], place=request.form['place'],
#                       name=request.form['name'], address=request.form['address'],
#                       latitude=request.form['latitude'], longitude=request.form['longitude'],
#                       station=request.form['station'], category=request.form['category'].lower())
#         df_new_pub = pd.DataFrame([new_pub.__dict__])
#         new_review = Review(review_identity=request.form['pub_identity'], pub_identity=pub_id,
#                             review_deletion=request.form['review_deletion'],
#                             visit=request.form['visit'],
#                             star=request.form.get('star_select').lower(), atmosphere=request.form['atmosphere'],
#                             cleanliness=request.form['cleanliness'], clientele=request.form['clientele'],
#                             decor=request.form['decor'], entertainment=request.form['entertainment'],
#                             food=request.form['food'], friendliness=request.form['friendliness'],
#                             opening=request.form['opening'], price=request.form['price'],
#                             selection=request.form['selection'], reviewer=request.form['reviewer'])
#         df_new_review = pd.DataFrame([new_review.__dict__])
#
#         if df_pub_review.empty:
#             print('NEW RECORD')
#             # # # # # NEW RECORD # # # # #
#             place = request.form['place']
#
#             df_place = df_pub_review.loc[df_pub_review['place'] == str(place)]
#             if df_place.empty:
#                 print('UNIQUE PLACE ID')
#                 # print('df_new_pub: ' + str(df_new_pub))
#                 df_pubs = function.get_pubs()
#                 # # # # # NEW and UNIQUE PLACE ID RECORD - save record # # # # #
#                 df_pubs_appended = pd.concat([df_pubs, df_new_pub], ignore_index=True)
#                 s3_resp = function.write_csv_to_s3(df_pubs_appended.to_csv(sep=',', encoding='utf-8', index=False),
#                                           constants.get("Aws_key", "PUB"))
#                 # print(s3_resp)
#                 df_reviews = function.get_reviews()
#                 df_reviews_appended = pd.concat([df_reviews, df_new_review], ignore_index=True)
#
#                 s3_resp = function.write_csv_to_s3(df_reviews_appended.to_csv(sep=',', encoding='utf-8', index=False),
#                                           constants.get("Aws_key", "REVIEW"))
#
#                 new_pub_json = function.df_to_dict(df_new_pub)
#                 df_pub_review = function.get_pub_review(pub_id)
#                 pub_review_json = function.df_to_dict(df_pub_review)
#                 # if df_review.empty:
#                 #     print('NO REVIEW')
#                 return render_template('pub_read.html', google_key=config['google_key'],
#                                        pub_review=pub_review_json,
#                                        # pub_fields=json.loads(constants.get("Columns", "PUB")),
#                                        pub_review_fields=json.loads(constants.get("Columns", "PUB_REVIEW")),
#                                        review_fields=json.loads(constants.get("Columns", "REVIEW")),
#                                        list_visible=json.loads(constants.get("Columns", "REVIEW_VISIBLE")))
#
#                 # else:
#                 #     print('REVIEW')
#                 #     review_json = df_to_dict(df_review)
#                 #     return render_template('pub_read.html', google_key=config['google_key'],
#                 #                            pub=new_pub_json, review=review_json,
#                 #                            pub_fields=json.loads(constants.get("Columns", "PUB")),
#                 #                            pub_review_fields=json.loads(constants.get("Columns", "PUB_REVIEW")),
#                 #                            review_fields=json.loads(constants.get("Columns", "REVIEW")),
#                 #                            list_visible=json.loads(constants.get("Columns", "PUB_REVIEW_VISIBLE")))
#             else:
#                 print('DUPLCATE PLACE ID')
#                 df_pubs_reviews = function.get_pubs_reviews()
#                 df_pub_review = df_pubs_reviews.loc[df_pubs_reviews['place'] == str(place)]
#                 pub_review_json = function.df_to_dict(df_pub_review)
#                 dupe_id = df_pub_review['pub_identity']
#                 return render_template("pop_up_dupe.html", pub_review=pub_review_json, dupe_id=dupe_id)
#         else:
#             print('EDITED PUB')
#             # # # # # EDITED OLD RECORD - return to edit screen without saving # # # # #
#             df_pubs = function.get_pubs()
#             df_pubs.loc[df_pubs['pub_identity'] == pub_id, 'pub_deletion'] = request.form['pub_deletion']
#             df_pubs.loc[df_pubs['pub_identity'] == pub_id, 'place'] = request.form['place']
#             df_pubs.loc[df_pubs['pub_identity'] == pub_id, 'name'] = request.form['name']
#             df_pubs.loc[df_pubs['pub_identity'] == pub_id, 'address'] = request.form['address']
#             df_pubs.loc[df_pubs['pub_identity'] == pub_id, 'latitude'] = request.form['latitude']
#             df_pubs.loc[df_pubs['pub_identity'] == pub_id, 'longitude'] = request.form['longitude']
#             df_pubs.loc[df_pubs['pub_identity'] == pub_id, 'station'] = request.form['station']
#             df_pubs.loc[df_pubs['pub_identity'] == pub_id, 'category'] = request.form['category'].lower()
#
#             s3_resp = function.write_csv_to_s3(df_pubs.to_csv(sep=',', encoding='utf-8', index=False),
#                                       constants.get("Aws_key", "PUB"))
#
#             df_reviews = function.get_reviews()
#             df_reviews.loc[df_reviews['pub_identity'] == pub_id, 'visit'] = request.form['visit']
#             df_reviews.loc[df_reviews['pub_identity'] == pub_id, 'star'] = request.form.get('star_select').lower()
#             df_reviews.loc[df_reviews['pub_identity'] == pub_id, 'atmosphere'] = request.form['atmosphere']
#             df_reviews.loc[df_reviews['pub_identity'] == pub_id, 'cleanliness'] = request.form['cleanliness']
#             df_reviews.loc[df_reviews['pub_identity'] == pub_id, 'clientele'] = request.form['clientele']
#             df_reviews.loc[df_reviews['pub_identity'] == pub_id, 'decor'] = request.form['decor']
#             df_reviews.loc[df_reviews['pub_identity'] == pub_id, 'entertainment'] = request.form['entertainment']
#             df_reviews.loc[df_reviews['pub_identity'] == pub_id, 'food'] = request.form['food']
#             df_reviews.loc[df_reviews['pub_identity'] == pub_id, 'friendliness'] = request.form['friendliness']
#             df_reviews.loc[df_reviews['pub_identity'] == pub_id, 'opening'] = request.form['opening']
#             df_reviews.loc[df_reviews['pub_identity'] == pub_id, 'price'] = request.form['price']
#             df_reviews.loc[df_reviews['pub_identity'] == pub_id, 'selection'] = request.form['selection']
#             df_reviews.loc[df_reviews['pub_identity'] == pub_id, 'reviewer'] = request.form['reviewer']
#
#             s3_resp = function.write_csv_to_s3(df_reviews.to_csv(sep=',', encoding='utf-8', index=False),
#                                       constants.get("Aws_key", "REVIEW"))
#             # print(s3_resp)
#             # result = object.put(Body=txt_data)
#             # res = s3_resp.get('ResponseMetadata')
#             # if res.get('HTTPStatusCode') == 200:
#             #     print('File Uploaded Successfully')
#             # else:
#             #     print('File Not Uploaded')
#             # pub_json = df_to_dict(get_pub(pub_id))
#
#             df_pub_review = function.get_pub_review(pub_id)
#             pub_review_json = function.df_to_dict(df_pub_review)
#
#             # pub_review_json = df_to_dict(get_pub_review(pub_id))
#             # if df_review.empty:
#             # print('NO REVIEW')
#             return render_template('pub_read.html', google_key=config['google_key'],
#                                    pub_review=pub_review_json,
#                                    # pub_fields=json.loads(constants.get("Columns", "PUB")),
#                                    # review_fields=json.loads(constants.get("Columns", "REVIEW")),
#                                    pub_review_fields=json.loads(constants.get("Columns", "PUB_REVIEW")),
#                                    list_visible=json.loads(constants.get("Columns", "REVIEW_VISIBLE")))
#             # else:
#             #     return render_template('pub_read.html', google_key=config['google_key'], pub=pub_json,
#             #                            review=review_json, pub_review=pub_review_json,
#             #                            pub_fields=json.loads(constants.get("Columns", "PUB")),
#             #                            review_fields=json.loads(constants.get("Columns", "REVIEW")),
#             #                            pub_review_fields=json.loads(constants.get("Columns", "PUB_REVIEW")),
#             #                            list_visible=json.loads(constants.get("Columns", "PUB_REVIEW_VISIBLE")))
#     # except Exception as e:
#     #     print(e)
#     #     return render_template('404.html', error=e, identity=id_code)


# @app.route("/pub/edit/<pub_id>")
# def pub_edit(pub_id):
#     print('/pub/edit/<pub_id>')
#     # try:
#     stations_json = function.df_to_dict(
#         function.get_records(constants.get("Aws_prefix", "STATION"), json.loads(constants.get("Columns", "STATION"))))
#     # print(stations_json)
#     df_pub_review = function.get_pub_review(pub_id)
#     pub_review_json = function.df_to_dict(df_pub_review)
#     # df_pub_review = get_pub_review(pub_id)
#     # pub_review_json = df_to_dict(df_pub_review)
#     # if not df_pub.empty:
#     #     print('Edit record located')
#     #
#     # df_review = get_review(pub_id)
#     # if df_pub_review.empty:
#     #     return render_template('pub_edit.html', google_key=config['google_key'],
#     #                            pub=pub_json, pub_review=pub_review_json,
#     #                            stations=stations_json, pub_fields=json.loads(constants.get("Columns", "PUB")),
#     #                            list_visible=json.loads(constants.get("Columns", "PUB_NO_REVIEW_VISIBLE")))
#     # else:
#     return render_template('pub_edit.html', google_key=config['google_key'],
#                            pub_review=pub_review_json,
#                            stations=stations_json, pub_review_fields=json.loads(constants.get("Columns", "PUB_REVIEW")),
#                            list_visible=json.loads(constants.get("Columns", "PUB_VISIBLE")),
#                            list_required=json.loads(constants.get("Columns", "REVIEW_VISIBLE")))
#
#     # except Exception as e:
#     #     print(e)
#     #     return render_template('404.html', error=e)


# @app.route("/pub/delete/<pub_id>")
# def pub_delete(pub_id):
#     # , methods = ['GET', 'POST'])
#     print('/pub/delete/<pub_id>')
#     # if request.method == 'GET':
#     #     print('/pub/delete/<pub_id>: GET')
#     #     df_pub = get_pub(pub_id)
#     #     pub_json = df_to_dict(df_pub)
#     #     pub_review = get_pub_review(pub_id)
#     #     pub_review_json = df_to_dict(pub_review)
#     #     return render_template('pop_up_delete.html', pub_review=pub_review_json)
#     # if request.method == 'POST':
#     #     print('/pub/delete/<pub_id>: POST')
#     df_pubs = function.get_pubs()
#     df_reviews = function.get_reviews()
#     # try:
#     df_pub = function.get_pub(pub_id)
#     # print('df_pub: ' + str(df_pub))
#     # if df_pub.empty:
#     #     print('df_pub empty')
#     #     # add nothing found to delete
#     # else:
#     #     print('df_pub marked for deletion')
#     df_pubs.loc[df_pubs['pub_identity'] == pub_id, 'pub_deletion'] = True
#     s3_resp = function.write_csv_to_s3(df_pubs.to_csv(sep=',', encoding='utf-8', index=False),
#                               constants.get("Aws_key", "PUB"))
#     # print(s3_resp)
#     df_reviews.loc[df_reviews['pub_identity'] == pub_id, 'review_deletion'] = True
#     s3_resp = function.write_csv_to_s3(df_reviews.to_csv(sep=',', encoding='utf-8', index=False),
#                               constants.get("Aws_key", "REVIEW"))
#     # print(s3_resp)
#     pubs_json = function.df_to_dict(function.get_pubs())
#     pubs_reviews_json = function.df_to_dict(function.get_pubs_reviews())
#     stations_json = function.df_to_dict(function.get_stations())
#     view = "stations"
#     return redirect(url_for('map_stations'))
#
#         # except Exception as e:
#         #     print(e)
#         #     return render_template('404.html', error=e)


@the_pub_crawls.route("/review/<pub_id>", methods=['GET', 'POST'])
def review(pub_id):
    print('/review/<pub_id>')
    # try:
    df_reviews = function.get_reviews()
    df_review = function.get_review(pub_id)
    review_json = function.df_to_dict(df_review)
    df_pub = function.get_pub(pub_id)
    pub_json = function.df_to_dict(df_pub)
    if request.method == 'GET':
        print('pub/ : GET')
        if df_review.empty:
            print('No record found')
            return render_template('404.html', error='no review', identity=pub_id)
        elif df_review.shape[0] > 1:
            print('Too many reviews')
            return render_template('404.html', error='too many reviews', identity=pub_id)
        else:
            print('Review found')
            pub_review = function.get_pub_review(pub_id)
            pub_review_json = function.df_to_dict(pub_review)
            return render_template("review_read.html", google_key=config['google_key'], pub=pub_json,
                                   review=review_json, pub_review=pub_review_json,
                                   pub_fields=json.loads(constants.get("Columns", "PUB")),
                                   review_fields=json.loads(constants.get("Columns", "REVIEW")),
                                   pub_review_fields=json.loads(constants.get("Columns", "PUB_REVIEW")),
                                   list_visible=json.loads(constants.get("Columns", "REVIEW_VISIBLE")))
    if request.method == 'POST':
        print('review/ : POST')
        if df_review.empty:
            print('NEW REVIEW')
            # # # # # NEW RECORD # # # # #
            new_review = Review(review_identity=request.form['pub_identity'], pub_identity=pub_id,
                                review_deletion=request.form['review_deletion'],
                                visit=request.form['visit'],
                                star=request.form.get('star_select'), atmosphere=request.form['atmosphere'],
                                cleanliness=request.form['cleanliness'], clientele=request.form['clientele'],
                                decor=request.form['decor'], entertainment=request.form['entertainment'],
                                food=request.form['food'], friendliness=request.form['friendliness'],
                                opening=request.form['opening'], price=request.form['price'],
                                selection=request.form['selection'], reviewer=request.form['reviewer'])
            df_new_review = pd.DataFrame([new_review.__dict__])
            df_reviews_appended = pd.concat([df_reviews, df_new_review], ignore_index=True)

            s3_resp = function.write_csv_to_s3(df_reviews_appended.to_csv(sep=',', encoding='utf-8', index=False),
                                      constants.get("Aws_key", "REVIEW"))
            # print(s3_resp)
            df_pubs = function.get_pubs()

            s3_resp = function.write_csv_to_s3(df_pubs.to_csv(sep=',', encoding='utf-8', index=False),
                                      constants.get("Aws_key", "PUB"))

            # print(s3_resp)
            review_json = function.df_to_dict(df_new_review)
            df_pub = function.get_pub(pub_id)
            pub_json = function.df_to_dict(df_pub)
            pub_review = function.get_pub_review(pub_id)
            pub_review_json = function.df_to_dict(pub_review)
            return render_template('review_read.html', google_key=config['google_key'], pub=pub_json,
                                   review=review_json, pub_review=pub_review_json,
                                   pub_fields=json.loads(constants.get("Columns", "PUB")),
                                   review_fields=json.loads(constants.get("Columns", "REVIEW")),
                                   pub_review_fields=json.loads(constants.get("Columns", "PUB_REVIEW")),
                                   list_visible=json.loads(constants.get("Columns", "REVIEW_VISIBLE")))
        else:
            print('EDITED RECORD')
            # # # # # EDITED OLD RECORD - return to edit screen without saving # # # # #
            df_reviews.loc[df_reviews['pub'] == pub_id, 'visit'] = request.form['visit']
            df_reviews.loc[df_reviews['pub'] == pub_id, 'star'] = request.form.get('star_select')
            df_reviews.loc[df_reviews['pub'] == pub_id, 'atmosphere'] = request.form['atmosphere']
            df_reviews.loc[df_reviews['pub'] == pub_id, 'cleanliness'] = request.form['cleanliness']
            df_reviews.loc[df_reviews['pub'] == pub_id, 'clientele'] = request.form['clientele']
            df_reviews.loc[df_reviews['pub'] == pub_id, 'decor'] = request.form['decor']
            df_reviews.loc[df_reviews['pub'] == pub_id, 'entertainment'] = request.form['entertainment']
            df_reviews.loc[df_reviews['pub'] == pub_id, 'food'] = request.form['food']
            df_reviews.loc[df_reviews['pub'] == pub_id, 'friendliness'] = request.form['friendliness']
            df_reviews.loc[df_reviews['pub'] == pub_id, 'opening'] = request.form['opening']
            df_reviews.loc[df_reviews['pub'] == pub_id, 'price'] = request.form['price']
            df_reviews.loc[df_reviews['pub'] == pub_id, 'selection'] = request.form['selection']
            df_reviews.loc[df_reviews['pub'] == pub_id, 'reviewer'] = request.form['reviewer']

            s3_resp = function.write_csv_to_s3(df_reviews.to_csv(sep=',', encoding='utf-8', index=False),
                                      constants.get("Aws_key", "REVIEW"))
            # print(s3_resp)
            df_review = function.get_review(pub_id)
            review_json = function.df_to_dict(df_review)
            pub_review = function.get_pub_review(pub_id)
            pub_review_json = function.df_to_dict(pub_review)
            return render_template('review_read.html', google_key=config['google_key'], pub=pub_json,
                                   review=review_json, pub_review=pub_review_json,
                                   pub_fields=json.loads(constants.get("Columns", "PUB")),
                                   review_fields=json.loads(constants.get("Columns", "REVIEW")),
                                   pub_review_fields=json.loads(constants.get("Columns", "PUB_REVIEW")),
                                   list_visible=json.loads(constants.get("Columns", "REVIEW_VISIBLE")))
    # except Exception as e:
    #     print(e)
    #     return render_template('404.html', error=e)


@the_pub_crawls.route("/review/add/<pub_id>")
def review_add(pub_id):
    print('/review/add/<pub_id>')
    # try:
    pub_json = function.df_to_dict(function.get_pub(pub_id))
    add_review = Review(review_identity=str(uuid.uuid4()), pub_identity=pub_id, review_deletion=False, visit=datetime.date.today(),
                        star="", atmosphere=0, cleanliness=0, clientele=0, decor=0, entertainment=0, food=0,
                        friendliness=0, opening=0, price=0, selection=0, reviewer="")
    review_json = function.df_to_dict(pd.DataFrame([add_review.__dict__]))
    print(review_json)
    return render_template("review_add.html", google_key=config['google_key'], pub=pub_json,
                           review=review_json,
                           pub_fields=json.loads(constants.get("Columns", "PUB")),
                           review_fields=json.loads(constants.get("Columns", "REVIEW")),
                           list_visible=json.loads(constants.get("Columns", "REVIEW_VISIBLE")))
    # except Exception as e:
    #     print(e)
    #     return render_template('404.html', error=e)


@the_pub_crawls.route("/review/edit/<pub_id>", methods=['GET', 'POST'])
def review_edit(pub_id):
    print('/review/edit/<pub_id>"')
    # try:
    df_review = function.get_review(pub_id)
    pub_json = function.df_to_dict(function.get_pub(pub_id))
    # df_pub_review = get_pub_review(pub_id)
    # pub_review_json = df_to_dict(df_pub_review)
    if df_review.empty:
        print('No record found')
        return render_template('404.html', error='no review', identity=pub_id)
    elif df_review.shape[0] > 1:
        print('Too many reviews')
        return render_template('404.html', error='too many reviews', identity=pub_id)
    else:
        print('EDIT RECORD LOCATED')
        review_json = function.df_to_dict(df_review)
        return render_template('review_edit.html', google_key=config['google_key'], pub=pub_json,
                               review=review_json,
                               pub_fields=json.loads(constants.get("Columns", "PUB")),
                               review_fields=json.loads(constants.get("Columns", "REVIEW")),
                               list_visible=json.loads(constants.get("Columns", "REVIEW_VISIBLE")))
    # except Exception as e:
    #     print(e)
    #     return render_template('404.html', error=e)


@the_pub_crawls.route("/review/delete/<pub_id>")
def review_delete(pub_id):
    print('/review/delete/<pub_id>')
    # print('pub_id: ' + str(pub_id))
    # try:
    df_review = function.get_review(pub_id)
    # print('df_review: ' + str(df_review))
    if df_review.empty:
        print('No record found')
        return render_template('404.html', error='no review', identity=pub_id)
    elif df_review.shape[0] > 1:
        print('Too many reviews')
        return render_template('404.html', error='too many reviews', identity=pub_id)
    else:
        print('EDIT RECORD LOCATED')
        df_reviews = function.get_reviews()
        df_reviews.loc[df_reviews['pub_identity'] == pub_id, 'review_deletion'] = True
        df_review = function.get_review(pub_id)
        # print('df_review: ' + str(df_review))
        s3_resp = function.write_csv_to_s3(df_reviews.to_csv(sep=',', encoding='utf-8', index=False),
                                  constants.get("Aws_key", "REVIEW"))
        # print(s3_resp)
        df_pubs = function.get_pubs()
        # if request.form['reviewer'] == "BOTH":
        #     set_colour = str(constants.get("Colours", "BOTH"))
        # elif request.form['reviewer'] == "ANDY":
        #     set_colour = str(constants.get("Colours", "ANDY"))
        # elif request.form['reviewer'] == "AVNI":
        #     set_colour = str(constants.get("Colours", "AVNI"))
        # else:
        #     set_colour = str(constants.get("Colours", "NEW"))
        # df_pubs.loc[df_pubs['identity'] == pub_id, 'colour'] = set_colour
        s3_resp = function.write_csv_to_s3(df_pubs.to_csv(sep=',', encoding='utf-8', index=False),
                                  constants.get("Aws_key", "PUB"))
        # print(s3_resp)
        pub_json = function.df_to_dict(function.get_pub(pub_id))
        # print('pub_json: ' + str(pub_json))
        return redirect(url_for('pub', pub_id=pub_id, google_key=config['google_key'], pub=pub_json))

    # except Exception as e:
    #     print(e)
    #     return render_template('404.html', error=e)


@the_pub_crawls.route("/pub/star/<star_id>")
def star(star_id):
    print('/pub/star/<star_id>')
    df_pubs_by_star = function.get_pubs_by_star(star_id)
    # print(df_pubs_by_star)
    pubs_rev_star_json = function.df_to_dict(df_pubs_by_star)
    view = "star"
    return render_template('pub_list.html', pubs_reviews=pubs_rev_star_json, map_view=view, map_lat=51.5, map_lng=-0.1)


@the_pub_crawls.route("/pub/location/<loc_id>")
def location(loc_id):
    print('/pub/location/<loc_id>')
    df_pubs_by_station = function.get_pubs_by_station(loc_id)
    pubs_rev_loc_json = function.df_to_dict(df_pubs_by_station)
    # print(df_pubs_by_station[['pub_identity', 'name', 'station']])
    view = "station"
    return render_template('pub_list.html', pubs_reviews=pubs_rev_loc_json, map_view=view, map_lat=51.5, map_lng=-0.1)


@the_pub_crawls.route("/pub/category/<cat_id>")
def category(cat_id):
    print('/pub/category/<cat_id>')
    df_pubs_by_category = function.get_pubs_by_category(cat_id)
    pubs_rev_cat_json = function.df_to_dict(df_pubs_by_category)
    view = "category"
    return render_template('pub_list.html', pubs_reviews=pubs_rev_cat_json, map_view=view, map_lat=51.5, map_lng=-0.1)
