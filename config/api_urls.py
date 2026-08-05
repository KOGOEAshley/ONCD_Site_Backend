from django.urls import path
from rest_framework.routers import DefaultRouter
from praticiens.views import PraticienViewSet, LoginView, InscriptionView, mon_profil, mon_attestation
from cliniques.views import CliniqueViewSet
from formations.views import mes_formations, mon_attestation_formation
from actualites.views import ActualiteViewSet
from evenements.views import EvenementViewSet
from elearning.views import ModuleELearningViewSet, mes_modules, terminer_module
from exposition.views import ExposantViewSet, ReserverStandView
from stages.views import StageViewSet, PostulerStageView
from documents.views import DocumentTelechargeableViewSet
from institution.views import MembreConseilViewSet

router = DefaultRouter()
router.register("praticiens", PraticienViewSet)
router.register("cliniques", CliniqueViewSet)
router.register("actualites", ActualiteViewSet)
router.register("evenements", EvenementViewSet)
router.register("modules-elearning", ModuleELearningViewSet)
router.register("exposants", ExposantViewSet)
router.register("stages", StageViewSet)
router.register("bibliotheque", DocumentTelechargeableViewSet)
router.register("conseil", MembreConseilViewSet)

urlpatterns = router.urls + [
    path("login/", LoginView.as_view()),
    path("inscription/", InscriptionView.as_view()),
    path("mon-profil/", mon_profil),
    path("mon-attestation/", mon_attestation),
    path("mes-formations/", mes_formations),
    path("mon-attestation-formation/<int:participation_id>/", mon_attestation_formation),
    path("mes-modules/", mes_modules),
    path("terminer-module/<int:inscription_id>/", terminer_module),
    path("reserver-stand/", ReserverStandView.as_view()),
    path("postuler-stage/", PostulerStageView.as_view()),
]