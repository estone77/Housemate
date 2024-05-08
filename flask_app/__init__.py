from flask import Flask, render_template, request, redirect
from flask_bcrypt import Bcrypt
from pprint import pprint

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "8732523825befs98dgskgu45nsdbgf87532GSSDG4g"
