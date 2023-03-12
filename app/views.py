from datetime import date
from flask import render_template, request, redirect, url_for
from .functions import *
from .models.pub import Pub
from .models.review import Review

config = Configurations().get_config()
function = Functions()


@flask_app.route("/testbed")
def testbed():
    print('/testbed')
    return render_template('testbed.html')


@flask_app.route("/")
@flask_app.route("/index")
def index():
    print('/index')
    photo_array = json.loads(constants.get("Columns", "SCORE"))
    return render_template('index.html', photo_array=photo_array, map_view="stations", map_lat=51.5, map_lng=-0.1,
                           row_loop=range(3), col_loop=range(4))


@flask_app.route("/pub/map/stations")
def map_stations():
    print('/pub/map/stations')
    df_stations = function.get_stations()
    df_pubs_reviews = function.get_pubs_reviews()
    df_reviewed_only = df_pubs_reviews.loc[df_pubs_reviews['colour'] != constants.get("Colours", "NEW")]
    df_truncated = df_reviewed_only[['name', 'station_identity']]
    df_result = df_truncated.groupby(['station_identity'], as_index=False).count()

    df_result_latlng = pd.merge(df_result, df_stations, how='left', on='station_identity')
    df_sorted = df_result_latlng.rename(columns={'name': 'count'}).astype(str)
    df_sorted['colour'] = constants.get("Colours", "RED")
    stations_json = function.df_to_dict(df_sorted)
    pubs_reviews_json = function.df_to_dict(df_pubs_reviews)
    view = "stations"
    return render_template('pub_map.html', google_key=config['google_key'], stations=stations_json,
                           pubs_reviews=pubs_reviews_json, icon_hole=False,
                           info_box=False, map_view=view, map_lat=51.5, map_lng=-0.1)


@flask_app.route("/pub/list")
def pub_list():
    print('/pub/list')
    pubs_reviews = function.get_pubs_reviews().sort_values(by=['score'], ascending=False)
    pubs_reviews_json = function.df_to_dict(pubs_reviews)
    view = "list"
    return render_template('pub_list.html', pubs_reviews=pubs_reviews_json, map_view=view, map_lat=51.5, map_lng=-0.1)


@flask_app.route("/pub/add/")
def pub_add():
    print('/pub/add')
    stations_json = function.df_to_dict(function.get_records(constants.get("Aws_prefix", "STATION"),
                                           json.loads(constants.get("Columns", "STATION"))))

    new_pub_id = str(function.generate_uuid())
    date_now = date.today().strftime("%B %d, %Y")

    add_pub = Pub(pub_identity=new_pub_id, pub_deletion=False, place="", name="", address="", latitude=51.5,
                  longitude=-0.1, station_identity="", category="")

    add_review = Review(review_identity=str(function.generate_uuid()), pub_identity=new_pub_id, review_deletion=False,
                        visit=date_now,
                        star="", atmosphere=0, cleanliness=0, clientele=0, decor=0, entertainment=0, food=0,
                        friendliness=0, opening=0, price=0, selection=0, reviewer="")
    df_pub_review = pd.merge(pd.DataFrame([add_pub.__dict__]), pd.DataFrame([add_review.__dict__]), on='pub_identity')
    pub_review_json = function.df_to_dict(df_pub_review)
    pubs_reviews_json = function.df_to_dict(function.get_pubs_reviews())
    return render_template("pub_add.html", google_key=config['google_key'], pubs_reviews=pubs_reviews_json,
                           pub_review=pub_review_json, stations=stations_json,
                           pub_review_fields=json.loads(constants.get("Columns", "PUB_REVIEW")),
                           list_visible=json.loads(constants.get("Columns", "REVIEW_VISIBLE")),
                           list_required=json.loads(constants.get("Columns", "REQUIRED")),
                           input_controls=json.loads(constants.get("Columns", "INPUT")),
                           dropdown_controls=json.loads(constants.get("Columns", "DROPDOWN")),
                           slider_controls=json.loads(constants.get("Columns", "SLIDER")),
                           score_list=json.loads(constants.get("Columns", "SCORE_REVIEW")))


@flask_app.route("/pub/<pub_id>", methods=['GET', 'POST'])
def pub(pub_id):
    print('/pub/<pub_id>')
    # try:
    df_pub_review = function.get_pub_review(pub_id)
    if request.method == 'GET':
        print('/pub/<pub_id>/GET')
        pub_review_json = function.df_to_dict(df_pub_review)
        return render_template("pub_read.html", google_key=config['google_key'],
                               pub_review=pub_review_json,
                               pub_review_fields=json.loads(constants.get("Columns", "PUB_REVIEW")),
                               list_visible=json.loads(constants.get("Columns", "REVIEW_VISIBLE")))
    if request.method == 'POST':
        print('/pub/<id_code>/POST')

        print(request.form['station_identity'])
        print(request.form['category'].lower())

        new_pub = Pub(pub_identity=pub_id, pub_deletion=request.form['pub_deletion'], place=request.form['place'],
                      name=request.form['name'], address=request.form['address'],
                      latitude=request.form['latitude'], longitude=request.form['longitude'],
                      station_identity=request.form['station_identity'], category=request.form['category'].lower())
        df_new_pub = pd.DataFrame([new_pub.__dict__])

        print(request.form.get('star'))
        print(request.form['atmosphere'])

        star_str = request.form.get('star')
        star_str_lower = star_str.lower()

        new_review = Review(review_identity=request.form['pub_identity'], pub_identity=pub_id,
                            review_deletion=request.form['review_deletion'],
                            visit=request.form['visit'],
                            star=star_str_lower, atmosphere=request.form['atmosphere'],
                            cleanliness=request.form['cleanliness'], clientele=request.form['clientele'],
                            decor=request.form['decor'], entertainment=request.form['entertainment'],
                            food=request.form['food'], friendliness=request.form['friendliness'],
                            opening=request.form['opening'], price=request.form['price'],
                            selection=request.form['selection'], reviewer=request.form['reviewer'])
        df_new_review = pd.DataFrame([new_review.__dict__])

        if df_pub_review.empty:
            print('NEW RECORD')
            # # # # # NEW RECORD # # # # #
            place = request.form['place']

            df_place = df_pub_review.loc[df_pub_review['place'] == str(place)]
            if df_place.empty:
                print('UNIQUE PLACE ID')
                # print('df_new_pub: ' + str(df_new_pub))
                df_pubs = function.get_pubs()
                # # # # # NEW and UNIQUE PLACE ID RECORD - save record # # # # #
                df_pubs_appended = pd.concat([df_pubs, df_new_pub], ignore_index=True)
                s3_resp = function.write_csv_to_s3(df_pubs_appended.to_csv(sep=',', encoding='utf-8', index=False),
                                          constants.get("Aws_key", "PUB"))
                # print(s3_resp)
                df_reviews = function.get_reviews()
                df_reviews_appended = pd.concat([df_reviews, df_new_review], ignore_index=True)

                s3_resp = function.write_csv_to_s3(df_reviews_appended.to_csv(sep=',', encoding='utf-8', index=False),
                                          constants.get("Aws_key", "REVIEW"))

                df_pub_review = function.get_pub_review(pub_id)
                pub_review_json = function.df_to_dict(df_pub_review)
                return render_template('pub_read.html', google_key=config['google_key'],
                                       pub_review=pub_review_json,
                                       pub_review_fields=json.loads(constants.get("Columns", "PUB_REVIEW")),
                                       review_fields=json.loads(constants.get("Columns", "REVIEW")),
                                       list_visible=json.loads(constants.get("Columns", "REVIEW_VISIBLE")))
            else:
                print('DUPLCATE PLACE ID')
                df_pubs_reviews = function.get_pubs_reviews()
                df_pub_review = df_pubs_reviews.loc[df_pubs_reviews['place'] == str(place)]
                pub_review_json = function.df_to_dict(df_pub_review)
                dupe_id = df_pub_review['pub_identity']
                return render_template("pop_up_dupe.html", pub_review=pub_review_json, dupe_id=dupe_id)
        else:
            print('EDITED PUB')
            # # # # # EDITED OLD RECORD - return to edit screen without saving # # # # #
            df_pubs = function.get_pubs()
            df_pubs.loc[df_pubs['pub_identity'] == pub_id, 'pub_deletion'] = request.form['pub_deletion']
            df_pubs.loc[df_pubs['pub_identity'] == pub_id, 'place'] = request.form['place']
            df_pubs.loc[df_pubs['pub_identity'] == pub_id, 'name'] = request.form['name']
            df_pubs.loc[df_pubs['pub_identity'] == pub_id, 'address'] = request.form['address']
            df_pubs.loc[df_pubs['pub_identity'] == pub_id, 'latitude'] = request.form['latitude']
            df_pubs.loc[df_pubs['pub_identity'] == pub_id, 'longitude'] = request.form['longitude']
            df_pubs.loc[df_pubs['pub_identity'] == pub_id, 'station_identity'] = request.form['station_identity']
            df_pubs.loc[df_pubs['pub_identity'] == pub_id, 'category'] = request.form['category'].lower()

            s3_resp = function.write_csv_to_s3(df_pubs.to_csv(sep=',', encoding='utf-8', index=False),
                                               constants.get("Aws_key", "PUB"))

            df_reviews = function.get_reviews()
            df_reviews.loc[df_reviews['pub_identity'] == pub_id, 'visit'] = request.form['visit']
            star_str = request.form.get('star')
            star_str_lower = star_str.lower()
            df_reviews.loc[df_reviews['pub_identity'] == pub_id, 'star'] = star_str_lower
            df_reviews.loc[df_reviews['pub_identity'] == pub_id, 'atmosphere'] = request.form['atmosphere']
            df_reviews.loc[df_reviews['pub_identity'] == pub_id, 'cleanliness'] = request.form['cleanliness']
            df_reviews.loc[df_reviews['pub_identity'] == pub_id, 'clientele'] = request.form['clientele']
            df_reviews.loc[df_reviews['pub_identity'] == pub_id, 'decor'] = request.form['decor']
            df_reviews.loc[df_reviews['pub_identity'] == pub_id, 'entertainment'] = request.form['entertainment']
            df_reviews.loc[df_reviews['pub_identity'] == pub_id, 'food'] = request.form['food']
            df_reviews.loc[df_reviews['pub_identity'] == pub_id, 'friendliness'] = request.form['friendliness']
            df_reviews.loc[df_reviews['pub_identity'] == pub_id, 'opening'] = request.form['opening']
            df_reviews.loc[df_reviews['pub_identity'] == pub_id, 'price'] = request.form['price']
            df_reviews.loc[df_reviews['pub_identity'] == pub_id, 'selection'] = request.form['selection']
            df_reviews.loc[df_reviews['pub_identity'] == pub_id, 'reviewer'] = request.form['reviewer']

            s3_resp = function.write_csv_to_s3(df_reviews.to_csv(sep=',', encoding='utf-8', index=False),
                                               constants.get("Aws_key", "REVIEW"))
            df_pub_review = function.get_pub_review(pub_id)
            pub_review_json = function.df_to_dict(df_pub_review)
            return render_template('pub_read.html', google_key=config['google_key'],
                                   pub_review=pub_review_json,
                                   pub_review_fields=json.loads(constants.get("Columns", "PUB_REVIEW")),
                                   list_visible=json.loads(constants.get("Columns", "REVIEW_VISIBLE")))


@flask_app.route("/pub/edit/<pub_id>")
def pub_edit(pub_id):
    print('/pub/edit/<pub_id>')
    # try:
    stations_json = function.df_to_dict(
        function.get_records(constants.get("Aws_prefix", "STATION"), json.loads(constants.get("Columns", "STATION"))))
    df_pub_review = function.get_pub_review(pub_id)
    pub_review_json = function.df_to_dict(df_pub_review)
    return render_template('pub_edit.html', google_key=config['google_key'],
                           pub_review=pub_review_json,
                           stations=stations_json, pub_review_fields=json.loads(constants.get("Columns", "PUB_REVIEW")),
                           list_visible=json.loads(constants.get("Columns", "REVIEW_VISIBLE")),
                           list_required=json.loads(constants.get("Columns", "REQUIRED")),
                           input_controls=json.loads(constants.get("Columns", "INPUT")),
                           dropdown_controls=json.loads(constants.get("Columns", "DROPDOWN")),
                           slider_controls=json.loads(constants.get("Columns", "SLIDER")),
                           score_list=json.loads(constants.get("Columns", "SCORE_REVIEW")))

    # except Exception as e:
    #     print(e)
    #     return render_template('404.html', error=e)


@flask_app.route("/pub/delete/<pub_id>")
def pub_delete(pub_id):
    # , methods = ['GET', 'POST'])
    print('/pub/delete/<pub_id>')
    # if request.method == 'GET':
    #     print('/pub/delete/<pub_id>: GET')
    #     df_pub = get_pub(pub_id)
    #     pub_json = df_to_dict(df_pub)
    #     pub_review = get_pub_review(pub_id)
    #     pub_review_json = df_to_dict(pub_review)
    #     return render_template('pop_up_delete.html', pub_review=pub_review_json)
    # if request.method == 'POST':
    #     print('/pub/delete/<pub_id>: POST')
    df_pubs = function.get_pubs()
    df_reviews = function.get_reviews()
    # try:
    df_pubs.loc[df_pubs['pub_identity'] == pub_id, 'pub_deletion'] = True
    s3_resp = function.write_csv_to_s3(df_pubs.to_csv(sep=',', encoding='utf-8', index=False),
                              constants.get("Aws_key", "PUB"))
    # print(s3_resp)
    df_reviews.loc[df_reviews['pub_identity'] == pub_id, 'review_deletion'] = True
    s3_resp = function.write_csv_to_s3(df_reviews.to_csv(sep=',', encoding='utf-8', index=False),
                              constants.get("Aws_key", "REVIEW"))
    # print(s3_resp)
    pubs_json = function.df_to_dict(function.get_pubs())
    pubs_reviews_json = function.df_to_dict(function.get_pubs_reviews())
    stations_json = function.df_to_dict(function.get_stations())
    view = "stations"
    return redirect(url_for('map_stations'))

        # except Exception as e:
        #     print(e)
        #     return render_template('404.html', error=e)