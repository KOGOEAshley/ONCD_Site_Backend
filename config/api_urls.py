from django.urls import path
from rest_framework.routers import DefaultRouter
from praticiens.views import PraticienViewSet, LoginView, InscriptionView, mon_profil, mon_attestation
from cliniques.views import CliniqueViewSet

router = DefaultRouter()
router.register("praticiens", PraticienViewSet)
router.register("cliniques", CliniqueViewSet)

urlpatterns = router.urls + [
    path("login/", LoginView.as_view()),
    path("inscription/", InscriptionView.as_view()),
    path("mon-profil/", mon_profil),
    path("mon-attestation/", mon_attestation),
]