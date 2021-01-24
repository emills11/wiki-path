from flask import render_template, redirect, url_for, request
from app import app
from app.forms import PathForm
from app.wiki_path import WikiPath

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = PathForm()

    if form.validate_on_submit():
        return redirect(url_for('.path', start=form.start_page.data, target=form.target_page.data))

    return render_template('wiki-path.html', form=form)


@app.route('/path')
def path():
    start, target = request.args.get('start'), request.args.get('target')
    wp = WikiPath(start, target)
    str_path = wp.findPathBidirectional()
    if str_path:
        return render_template('path.html', path=str_path)
    else:
        return render_template('no-path.html')