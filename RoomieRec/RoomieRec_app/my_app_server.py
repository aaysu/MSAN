from flask import Flask, request
import pandas as pd
import re
from datetime import datetime
from clean_data import clean
from filter_data import filter
from cluster_data import cluster
from gmaps_fns import *
from webpage import searchpage, recpage

pd.set_option('display.max_colwidth', -1)
listings = clean('craigslist.csv')
listings = listings.assign(index=range(len(listings)))


app = Flask(__name__)


@app.route('/')
def search_page():
    return searchpage()


@app.route('/recommendation/', methods = ['GET'])
def post_rec():
    if request.args.get('max_price', '') != '':
        max_price = float(re.sub("[\$]", "", request.args.get('max_price', '')))
    else:
        max_price = None
    if request.args.get('min_price', '') != '':
        min_price = float(re.sub("[\$]", "", request.args.get('min_price', '')))
    else:
        min_price = None
    if request.args.get('movein', '') != '':
        movein = datetime.strptime(request.args.get('movein', ''), '%Y-%m-%d')
    else:
        movein = None
    if request.args.get('work', '') != '':
        work = str(request.args.get('work', ''))
    else:
        work = None
    if request.args.get('local', '') in types:
        local = str(request.args.get('local', ''))
    else:
        local = None
    neighborhoods = request.args.getlist('neighborhood[]')
    attributes = request.args.getlist('attributes[]')
    description = re.sub(r'\\[ntr]', ' ', request.args.get('description', ''))
    description = re.sub('\\s+', ' ', description)
    input = [max_price, min_price, movein, neighborhoods, attributes, description, work, local]
    keep = filter(listings, input)
    filtered_listings = listings.ix[keep]
    match = cluster(filtered_listings, description, keep)
    df_match = listings.ix[match]
    df_match = df_match[['title', 'price', 'neighborhood', 'movein', 'attributes', 'description',
                         'latitude', 'longitude']]
    if bool(input[6] and input[7]):
        final_listings = add_gmaps_cols(df_match, input[6], input[7])
        json = final_listings.to_json()
        return recpage(json)
    else:
        json = df_match.to_json()
        return recpage(json)


if __name__ == "__main__":
    # app.debug = True # only have this on for debugging!
    app.run(host='0.0.0.0', port=8001) # need this to access from the outside world!
