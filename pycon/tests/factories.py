from datetime import timedelta, datetime
import random
from django.utils.timezone import utc, localtime

import factory
import factory.django
import factory.fuzzy

from django.contrib.auth import models as auth

from pycon.models import PyConProposalCategory, PyConProposal, \
    PyConTalkProposal, PyConTutorialProposal, ThunderdomeGroup, PyConLightningTalkProposal, \
    ScheduledEvent, EduSummitTalkProposal

from symposion.proposals.models import ProposalKind
from symposion.proposals.tests.factories import ProposalBaseFactory
from symposion.reviews.models import ProposalResult, ProposalGroup


def aware_now():
    """Return the current time as an aware datetime object in the
    current time zone"""
    return localtime(datetime.utcnow().replace(tzinfo=utc))


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = auth.User

    username = factory.fuzzy.FuzzyText()
    first_name = factory.fuzzy.FuzzyText()
    last_name = factory.fuzzy.FuzzyText()
    email = factory.Sequence(lambda n: 'user{}@example.com'.format(n))


class ProposalGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProposalGroup

    review_start = factory.fuzzy.FuzzyDateTime(start_dt=aware_now() - timedelta(days=2),
                                               end_dt=aware_now() - timedelta(days=1))
    vote_start = factory.fuzzy.FuzzyDateTime(start_dt=aware_now() - timedelta(days=2),
                                             end_dt=aware_now() - timedelta(days=1))
    vote_end = factory.fuzzy.FuzzyDateTime(start_dt=aware_now() + timedelta(days=1),
                                           end_dt=aware_now() + timedelta(days=2))


class ProposalResultFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProposalResult

    group = factory.SubFactory(ProposalGroupFactory)


class PyConProposalCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PyConProposalCategory


class PyConProposalFactory(ProposalBaseFactory):
    class Meta:
        model = PyConProposal
        abstract = True

    category = factory.SubFactory(PyConProposalCategoryFactory)
    audience_level = factory.LazyAttribute(lambda a: random.choice([1, 2, 3]))


class PyConTalkProposalFactory(PyConProposalFactory):
    class Meta:
        model = PyConTalkProposal

    duration = 0

    kind = ProposalKind.objects.get(slug='talk')
    outline = "outline"
    audience = "audience"


class PyConTutorialProposalFactory(PyConProposalFactory):
    class Meta:
        model = PyConTutorialProposal

    kind = ProposalKind.objects.get(slug='tutorial')
    domain_level = 1
    outline = "outline"
    audience = "audience"


class ScheduledEventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ScheduledEvent

    name = factory.fuzzy.FuzzyText()
    slug = factory.fuzzy.FuzzyText()
    start = factory.fuzzy.FuzzyDateTime(start_dt=aware_now() - timedelta(days=2),
                                        end_dt=aware_now() - timedelta(days=1))
    end = factory.fuzzy.FuzzyDateTime(start_dt=aware_now() + timedelta(days=1),
                                      end_dt=aware_now() + timedelta(days=2))
    description = factory.fuzzy.FuzzyText()
    published = True


class ThunderdomeGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ThunderdomeGroup


class PyConLightningTalkProposalFactory(PyConProposalFactory):
    class Meta:
        model = PyConLightningTalkProposal

    kind = ProposalKind.objects.get(slug='lightning-talk')


class PyConEduSummitProposalFactory(PyConProposalFactory):
    class Meta:
        model = EduSummitTalkProposal

    kind = ProposalKind.objects.get(slug='edusummit')
