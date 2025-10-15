from flask import Blueprint, redirect, url_for
bp = Blueprint("root_redirect", __name__)
@bp.get("/")
def index(): return redirect(url_for("routes.dashboard"))
