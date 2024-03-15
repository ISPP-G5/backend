from nexong.api.Event.views import EventApiViewSet
from rest_framework.routers import DefaultRouter
from nexong.api.CenterExit.views import CenterExitApiViewSet
from nexong.api.Student.views import StudentApiViewSet
from .Authentication.views import *
from .Meeting.views import *
from .Event.views import *
from .Lesson.views import *
from .Donation.views import *
from .Evaluation.views import *
from .PunctualDonation.views import *
from .HomeDocument.views import *

router_api = DefaultRouter()
router_api.register(prefix="user", viewset=UserApiViewSet, basename="user")
router_api.register(prefix="meeting", viewset=MeetingApiViewSet, basename="meeting")
router_api.register(prefix="event", viewset=EventApiViewSet, basename="event")
router_api.register(prefix="lesson", viewset=LessonApiViewSet, basename="lesson")
router_api.register(
    prefix="lesson-attendance",
    viewset=LessonAttendanceApiViewSet,
    basename="lesson-attendance",
)
router_api.register(prefix="donation", viewset=DonationApiViewSet, basename="donation")
router_api.register(
    prefix="volunteer", viewset=VolunteerApiViewSet, basename="volunteer"
)
router_api.register(
    prefix="lesson-event", viewset=LessonEventApiViewSet, basename="lessonevent"
)
router_api.register(prefix="student", viewset=StudentApiViewSet, basename="student")
router_api.register(
    prefix="center-exit", viewset=CenterExitApiViewSet, basename="center-exit"
)
router_api.register(
    prefix="student-evaluation",
    viewset=StudentEvaluationApiViewSet,
    basename="studentevaluation",
)
router_api.register(
    prefix="evaluation-type",
    viewset=EvaluationTypeApiViewSet,
    basename="evaluationtype",
)
router_api.register(prefix="educator", viewset=EducatorApiViewSet, basename="educator")
router_api.register(prefix="partner", viewset=PartnerApiViewSet, basename="partner")
router_api.register(prefix="family", viewset=FamilyApiViewSet, basename="family")
router_api.register(
    prefix="punctual-donation",
    viewset=PunctualDonationApiViewSet,
    basename="punctual-donation",
)
router_api.register(
    prefix="home-document", viewset=HomeDocumentApiViewSet, basename="home-document"
)
router_api.register(
    prefix="education-center",
    viewset=EducationCenterApiViewSet,
    basename="education-center",
)
