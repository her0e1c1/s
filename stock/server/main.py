# coding: utf-8
from flask import Flask, render_template, request, jsonify, abort

from stock import query
from stock import service


app = Flask(__name__)


@app.route("/", methods=["GET"])
# @app.route("/company/", methods=["GET"])
def index():
    try:
        v = int(request.args.get("ratio_closing_minus_rolling_mean_25"))
    except:
        v = None
    try:
        v2 = int(request.args.get("closing_rsi_14"))
    except:
        v2 = None
    company_list = service.get_companies(
        ratio_closing_minus_rolling_mean_25=v,
        closing_rsi_14=v2,
    )
    return render_template('index.html', **{"company_list": company_list,
                                            "last_date": service.last_date()})


@app.route("/company/<int:id>", methods=["GET"])
def company(id):
    company = query.Company.first(id=id)
    if not company:
        abort(404)
    return render_template('company.html', **{"company": company})


@app.route("/api/<int:company_id>", methods=["GET"])
def api(company_id):
    company = query.Company.first(id=company_id)
    if not company:
        abort(404)
    q = query.DayInfo.get(company_id)
    return jsonify({
        "company": company.w.to_dict(),
        "rolling_means": [
            {"name": "rolling_mean25", "data": q.rolling_mean(period=25)},
            {"name": "rolling_mean5", "data": q.rolling_mean(period=5)},
        ],
        "ohlc": q.ohlc(),
        "columns": [
            {"name": "volume", "data": q.volume()},
        ],
        "percentages": [
            {"name": "RSI", "data": q.RSI(period=14)},
        ],
        "macd": [
            {"name": "macd_line", "data": q.macd_line(), "yAxis": 3},
            {"name": "macd_signal", "data": q.macd_signal(), "yAxis": 3},
        ],
    })
