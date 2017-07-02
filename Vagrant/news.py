#!/usr/bin/env python3
#
# dsfsklafaskfa;sl

from flask import Flask, request, redirect, url_for

from newsdb import get_popular_articles, get_popular_authors

app = Flask(__name__)

# HTML template for the News Analysis Report page
HTML_WRAP = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>News Analysis Reports</title>
    <style>
      h1, form { text-align: center; }
      textarea { width: 400px; height: 100px; }
      div.post { border: 1px solid #999;
                 padding: 10px 10px;
                 margin: 10px 20%%; }
      hr.postbound { width: 50%%; }
      em.date { color: #999 }
    </style>
  </head>
  <body>
    <h1>News Analysis Reports</h1>
    <h2>Most popular three articles</h2>
    <!-- post content will go here -->
%s
  </body>
</html>
'''

# HTML template for an individual comment
POST = '''\
    <div class=post><em class=date>%s</em>%s</div>

'''

POST1 = '''\
    <div class=post><em class=date>%s</em>%s</div>

'''


@app.route('/', methods=['GET'])
def main():
  '''Main page of the forum.'''
  # posts = "".join(POST % (title, popularity) for title, popularity in get_popular_articles())
  # html = HTML_WRAP % posts
  # return html

  posts1 = "".join(POST1 % (name, popularity) for name, popularity in get_popular_authors())
  html1 = HTML_WRAP % posts1
  return html1


# @app.route('/', methods=['POST'])
# def post():
#   '''New post submission.'''
#   message = request.form['content']
#   add_post(message)
#   return redirect(url_for('main'))


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=7000)

