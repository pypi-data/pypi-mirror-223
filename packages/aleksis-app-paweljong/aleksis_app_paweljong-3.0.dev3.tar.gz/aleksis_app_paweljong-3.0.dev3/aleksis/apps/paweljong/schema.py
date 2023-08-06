from django.utils import timezone

import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from aleksis.core.models import Person
from aleksis.core.util.core_helpers import has_person

from .models import Checkpoint, Event


class EventType(DjangoObjectType):
    class Meta:
        model = Event


class CheckpointType(DjangoObjectType):
    class Meta:
        model = Checkpoint


class CheckpointCheckInMutation(graphene.Mutation):
    class Arguments:
        event_slug = graphene.String(required=True)
        person_id = graphene.Int(required=True)
        comment = graphene.String(required=True)
        lat = graphene.Int(required=False)
        lon = graphene.Int(required=False)

    checkpoint = graphene.Field(CheckpointType)

    @classmethod
    def mutate(
        cls,
        root,
        info,
        event_slug,
        person_id,
        comment,
        lat=None,
        lon=None,
    ):
        if not has_person(info.context.user) or not info.context.user.has_perm("paweljong.event_checkpoint_rule"):
            raise PermissionDenied()

        try:
            event = Event.objects.get(slug=event_slug)
        except Event.DoesNotExist:
            raise GraphQLError(f"No Event with slug {event_slug}.")

        try:
            person = Person.objects.get(pk=person_id)
        except Person.DoesNotExist:
            raise GraphQLError(f"No Person with ID {person_id}.")

        checkpoint = Checkpoint()

        checkpoint.event = event
        checkpoint.person = person
        checkpoint.checked_by = info.context.user.person

        checkpoint.comment = comment
        checkpoint.timestamp = timezone.now()
        if lat and lon:
            checkpoint.lat = lat
            checkpoint.lon = lon

        checkpoint.save()

        return CheckpointCheckInMutation(checkpoint=checkpoint)


class Mutation(graphene.ObjectType):
    checkpoint_check_in = CheckpointCheckInMutation.Field()
