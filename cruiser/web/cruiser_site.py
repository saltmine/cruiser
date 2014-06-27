from flask import Flask, jsonify, request as R, render_template

from ..models import images

app = Flask(__name__)

@app.route('/get_classify/')
def get_classify_url():
  return jsonify({'to_classify_count': images.get_to_classify_count(),
                  'to_classify': images.get_to_classify()})


@app.route('/save_classify/')
def save_classify():
  prod_id = R.values.get('to_classify_id')
  save = 0
  save_txt = R.values.get('save_image', '0').strip()
  if save_txt and save_txt.isdigit():
    save = int(save_txt)
  if save:
    images.save_classify(prod_id)
  else:
    images.ignore_classify(prod_id)
  return jsonify({'ok': True})


@app.route('/get_comparison/')
def get_comparison():
  a, b = images.get_pair()
  return jsonify({'a': a, 'b': b})


@app.route('/save_comparison/')
def save_comparison():
  winner = R.values.get('winner')
  loser = R.values.get('loser')
  if winner and loser:
    images.settle_victory(winner, loser)
  return jsonify({'ok': True})


@app.route('/set_ignored/')
def set_ignored():
  images.set_ignored(R.values.get('to_ignore', ''))
  return jsonify({'ok': True})


@app.route('/classify/')
def classify():
  return render_template('classify.j2')


@app.route('/rank/')
@app.route('/')
def rank():
  return render_template('rank.j2')


@app.route('/top/', defaults={'offset':0})
@app.route('/top/<int:offset>/')
def top_products(offset):
  offset = max(offset, 0)
  top_prods = images.get_rev_range(offset, offset+49, withscores=True)
  return render_template('top.j2', offset=offset, top_prods=top_prods)


if __name__ == "__main__":
  app.run('0.0.0.0', debug=True)
