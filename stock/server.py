import io
from flask import Flask, make_response, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
# from matplotlib.dates import DateFormatter
from stock import query


app = Flask(__name__)


@app.route("/images/<db>/<code>")
def image(db, code):
    fig = Figure()
    ax = fig.add_subplot(111)
    quandl_code = db + "/" + code
    series = query.get(quandl_code=quandl_code)
    if "offset" in request.args:
        offset = -int(request.args["offset"])
        series = series[offset:]
    ax.plot(series)
    if "predict" in request.args:
        y = query.predict(quandl_code=quandl_code)
        ax.axhline(y, color="red")
    # ax.plot_date(x, y, '-')
    # ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    # fig.autofmt_xdate()
    canvas = FigureCanvas(fig)
    png_output = io.BytesIO()
    canvas.print_png(png_output)
    response = make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response


if __name__ == "__main__":
    app.run(port=80, host="0.0.0.0")
