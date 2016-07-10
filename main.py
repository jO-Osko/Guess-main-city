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

    # Ce nekaj potrebujemo veckrat to najraje damo v posebno metodo
    def city_guess(self, cities):
        return random.choice(cities)

    def get(self):
        mesta = dict()
        mesta["city_guess"] = self.city_guess(Cities)

        return self.render_template("main.html", params=mesta)

    def post(self):
        # random select, choice za random zadeve
        # drugace pa v href v html
        # ali pa static mapa s slikami, da niso dolgi hrefi in do njih dostopanje
        answered_city = self.request.get("city_name")

        city_id = int(self.request.get("city_id"))  # Nekako si je potrebno zapomniti, katero mesto je bilo na zacetku izbrano kot pravilni odgovor.

        # Sedaj dobimo pravilni odgovor (poiscemo mesto po id-ju, ter vzamemo njegovo ime)

        correct_city = None

        # To bi bilo bolj pravilno z uporabo slovarja, ki bi iz

        for city in Cities:
            if city.city_id == city_id:
                correct_city = city
                break
        else:  # to se izvede, ce for loop ni bil breakan
            print("Nekdo se je poigral z naso spletno stranjo")
            correct_city = Cities[0]  # Nastavimo pravo mesto na prvo mest

        if answered_city == correct_city.name:
            result = "You've guessed the main city of this country."
        else:
            result = "You haven't guessed the main city of this country."

        mesta = dict()
        mesta["city_guess"] = self.city_guess(Cities)
        mesta["guess_city_name"] = result
        mesta["message"] = "entered was: " + answered_city

        return self.render_template("main.html", params=mesta)

Ljubljana = City("Ljubljana", "Slovenia", "https://www.visitljubljana.com/assets/tiles/_resampled/FillWzExMzIsNTU4XQ/19-green-capital-tours.jpg", 1)
Zagreb = City("Zagreb", "Croatia", "http://www.summer-ballet-croatia.com/zagreb.jpg", 2)
Beograd = City("Beograd", "Serbia", "https://upload.wikimedia.org/wikipedia/commons/d/d1/Belgrade_iz_balona.jpg", 3)
Vienna = City("Vienna", "Austria", "http://www.austria.info/media/17083/thumbnails/stadtansicht-wien--oesterreich-werbung-julius-silver--d.jpg.3146489.jpg", 4)
Rome = City("Rome", "Italy", "http://www.accunet.org/images/Rome%20Seminar/Rome.jpg", 5)
Berlin = City("Berlin", "Germany", "https://fly.stanstedairport.com/travel/images/destination_carousel_berlin", 6)
London = City("London", "England", "https://media.timeout.com/images/100644443/image.jpg", 7)
Paris = City("Paris", "France", "http://www.premiumtours.co.uk/images/product/original/67_1.jpg", 8)

Cities = [Ljubljana, Zagreb, Beograd, Vienna, Rome, Berlin, London, Paris]

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler)
], debug=True)
