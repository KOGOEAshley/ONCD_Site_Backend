from django.db import migrations


def creer_bareme_par_defaut(apps, schema_editor):
    BaremeCotisation = apps.get_model("cotisations", "BaremeCotisation")
    valeurs_defaut = {
        "liberal": 75000,
        "secteur_public": 50000,
        "secteur_prive": 60000,
        "mixte": 85000,
    }
    for secteur, montant in valeurs_defaut.items():
        BaremeCotisation.objects.get_or_create(secteur=secteur, defaults={"montant": montant})


def supprimer_bareme(apps, schema_editor):
    BaremeCotisation = apps.get_model("cotisations", "BaremeCotisation")
    BaremeCotisation.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("cotisations", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(creer_bareme_par_defaut, supprimer_bareme),
    ]