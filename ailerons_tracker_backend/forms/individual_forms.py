
from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import DateField, IntegerField, RadioField, StringField, SelectField, TextAreaField
from wtforms.validators import Length, DataRequired, Optional, NumberRange


class NewIndividualForm(FlaskForm):
    name = StringField(
        'Surnom',
        [DataRequired('Veuillez renseigner un surnom.'),
         Length(min=3, max=25),])

    sex = SelectField(
        'Sexe',
        choices=[
            ("Male", "Male"),
            ("Femelle", "Femelle"),
            ("Inconnu", "Inconnu")],

        validators=[
            DataRequired('Veuillez renseigner le sexe.')])

    images = MultipleFileField(
        'Photos',
        [Optional()])

    description = StringField(
        "Description",
        [DataRequired('Veuillez renseigner une description.')])

    size = IntegerField(
        'Envergure au balisage',
        [NumberRange(1, 20)])

    date = DateField(
        'Date du balisage',
        [DataRequired('Veuillez renseigner la date.')])

    situation = RadioField(
        choices=[
            ('Seul', 'Seul'),
            ('En groupe', 'En groupe'),
            ('Avec partenaire', 'Avec partenaire')],

        validators=[
            DataRequired('Veuillez renseigner la situation.')])

    behavior = TextAreaField(
        'Comportement observé',
        default="Rédigez vos observations ici",
        validators=[
            DataRequired('Veuillez renseigner le comportement observé.')])


class EditIndividualForm(FlaskForm):
    name = StringField(
        'Surnom', [Optional(), Length(min=3, max=25)])

    sex = SelectField(
        'Sexe',
        choices=[
            ("Male", "Male"),
            ("Femelle", "Femelle"),
            ("Inconnu", "Inconnu")],
        validators=[Optional()])

    images = MultipleFileField(
        'Photos',
        [Optional()])

    description = StringField(
        "Description", [Optional()])

    size = IntegerField(
        'Envergure au balisage',
        [Optional(), NumberRange(1, 20)])

    date = DateField(
        'Date du balisage', [Optional()])

    situation = RadioField(
        choices=[
            ('Seul', 'Seul'),
            ('En groupe', 'En groupe'),
            ('Avec partenaire', 'Avec partenaire')],
        validators=[Optional()])

    behavior = TextAreaField(
        'Comportement observé',
        default="Rédigez vos observations ici",
        validators=[Optional()])
