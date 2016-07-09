#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import City
import random


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        '''
        def city_guess(Cities):
            return random.choice(Cities)

        mesta = dict()
        mesta["city_guess"] = city_guess(Cities)
        '''

        return self.render_template("main.html")

    def post(self):
        # random select, choice za random zadeve
        # drugace pa v href v html
        # ali pa static mapa s slikami, da niso dolgi hrefi in do njih dostopanje
        city = self.request.get("city_name")

        def city_guess(Cities):
            return random.choice(Cities)

        def guess_city_name(city):
            if city == city_guess(Cities):
                return "You've guessed the main city of this country."
            else:
                return "You haven't guessed the main city of this country."

        mesta = dict()
        mesta["city_guess"] = city_guess(Cities)
        mesta["guess_city_name"] = guess_city_name(city)

        self.write("entered was: " + city)

        return self.render_template("main.html", params=mesta)

Ljubljana = City("Ljubljana", "Slovenia", "https://www.visitljubljana.com/assets/tiles/_resampled/FillWzExMzIsNTU4XQ/19-green-capital-tours.jpg")
Zagreb = City("Zagreb", "Croatia", "http://www.summer-ballet-croatia.com/zagreb.jpg")
Beograd = City("Beograd", "Serbia", "https://upload.wikimedia.org/wikipedia/commons/d/d1/Belgrade_iz_balona.jpg")
Vienna = City("Vienna", "Austria", "http://www.austria.info/media/17083/thumbnails/stadtansicht-wien--oesterreich-werbung-julius-silver--d.jpg.3146489.jpg")
Rome = City("Rome", "Italy", "http://www.accunet.org/images/Rome%20Seminar/Rome.jpg")
Berlin = City("Berlin", "Germany", "https://fly.stanstedairport.com/travel/images/destination_carousel_berlin")
London = City("London", "England", "https://media.timeout.com/images/100644443/image.jpg")
Paris = City("Paris", "France", "http://www.premiumtours.co.uk/images/product/original/67_1.jpg")

Cities = [Ljubljana, Zagreb, Beograd, Vienna, Rome, Berlin, London, Paris]

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler)
], debug=True)
