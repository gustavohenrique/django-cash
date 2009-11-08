# -*- coding: utf-8 -*-
from models import Tag, TagItem
from django.contrib.contenttypes.models import ContentType

def aplicar_tags(obj, tags):
    tipo_dinamico = ContentType.objects.get_for_model(obj)

    TagItem.objects.filter(
        content_type=tipo_dinamico,
        object_id=obj.id,
        ).delete()

    tags = tags.split(' ')
    for tag_nome in tags:
        tag, nova = Tag.objects.get_or_create(nome=tag_nome)

        TagItem.objects.get_or_create(
            tag=tag,
            content_type=tipo_dinamico,
            object_id=obj.id,
            )

def tags_para_objeto(obj):
    tipo_dinamico = ContentType.objects.get_for_model(obj)

    tags = TagItem.objects.filter(
        content_type=tipo_dinamico,
        object_id=obj.id,
        )

    return ' '.join([item.tag.nome for item in tags])
