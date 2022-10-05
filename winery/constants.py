from datetime import date

CHOICE_CHOICES = [("year", "year"), ("varietal", "varietal"), ("vineyard", "vineyard")]

YEAR_CHOICES = [
    (i, i) for i in range(date.today().year, 2012, -1)
]

VARIETAL_CHOICES = [
    ('pinot_gris', "Pinot Gris"),
    ('black_muscat', "Black Muscat"),
]

VINEYARD_CHOICES = [
    ('blue_grouse', "Blue Grouse"),
]

