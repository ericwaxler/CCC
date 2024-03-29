import os

import pandas as pd
import numpy as np

import chart_studio.plotly as py
import plotly.graph_objs as go

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData, Table, Column, types

from flask import Flask, Response, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

import datetime, dateutil

import io
import random
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
import pandas as pd
import numpy as np

app = Flask(__name__)


#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = #your DB uri
app.config['IMAGES_URL'] = '/plots'
db = SQLAlchemy(app)

#engine = create_engine('your DB uri')
metadata = MetaData()
metadata.reflect(engine, only=['prices', 'pivot'])

"""Table('prices', metadata,
            Column('Currency', String),
            Column("Date", text),
            Column("Open", double),
            Column("High", double),
            Column("Low", double),
            Column("Close", double),
            Column("Volume", text),
            Column("Market Cap", text),
            Column("UnixDate", bigint)
        )"""
# reflect an existing database into a new model
Base = automap_base(metadata=metadata)
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
Prices = Base.classes.prices
Pivot = Base.classes.pivot


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/ml")
def ml():
    return render_template("ml.html")

@app.route("/analysis")
def analysis():
    return render_template("analysis.html")

@app.route("/currencies")
def names():
    """Return a list of sample names."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(Pivot).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the column names (sample names)
    return jsonify(list(df.columns[1:]))


@app.route("/historic/<coin>")
def sample_historic(coin):
    """Return the historic data for a given sample."""
    
    stmt = db.session.query(Prices).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Filter the data based on the sample number and
    results = df.loc[df['Currency'] == coin, ['Currency','Date','Open','High','Low','Close','Volume','MarketCap','UnixDate']]

    results.sort_values(by='UnixDate', ascending=False, inplace=True)
    results = results.head(100)

    # Create a dictionary entry for each row of metadata information
    sample_data = {
        "Date": results.Date.values.tolist(),
        "Open": results.Open.values.tolist(),
        "High": results.High.values.tolist(),
        "Low": results.Low.values.tolist(),
        "Close": results.Close.values.tolist(),
        "Volume": results.Volume.values.tolist(),
        "MarketCap": results.MarketCap.values.tolist(),
    }

    return jsonify(sample_data)


@app.route("/samples/<sample>")
def samples(sample):
    """Return `otu_ids`, `otu_labels`,and `sample_values`."""
    stmt = db.session.query(Samples).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Filter the data based on the sample number and
    # only keep rows with values above 1
    sample_data = df.loc[df[sample] > 1, ["otu_id", "otu_label", sample]]

    # Sort by sample
    sample_data.sort_values(by=sample, ascending=False, inplace=True)

    # Format the data to send as json
    data = {
        "otu_ids": sample_data.otu_id.values.tolist(),
        "sample_values": sample_data[sample].values.tolist(),
        "otu_labels": sample_data.otu_label.tolist(),
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run()
