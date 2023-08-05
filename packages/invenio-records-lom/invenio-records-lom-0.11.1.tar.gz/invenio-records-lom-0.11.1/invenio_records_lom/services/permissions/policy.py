# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2023 Graz University of Technology.
#
# invenio-records-lom is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Permission-policy class for LOMRecordService-objects."""

from invenio_rdm_records.services.generators import (
    IfFileIsLocal,
    IfRestricted,
    RecordOwners,
)
from invenio_rdm_records.services.permissions import RDMRecordPermissionPolicy
from invenio_records_permissions.generators import (
    AnyUser,
    AuthenticatedUser,
    SystemProcess,
)

from .generators import OERCertifiedUsers, OERCurators


class LOMRecordPermissionPolicy(RDMRecordPermissionPolicy):
    """Flask-principal style permissions for LOM record services.

    Note that the invenio_access.Permission parent-class always adds
    ``superuser-access``, so admin-Identities are always allowed to take any action.
    """

    # no rights for CommunityCurators, as this package doesn't implement communities
    # no rights for SubmissionReviewers, as this package doesn't implement reviews
    #
    # General permission-groups, to be used in below categories
    #
    can_manage = [RecordOwners(), SystemProcess()]
    can_curate = can_manage + [OERCurators()]
    can_review = can_curate
    can_preview = can_manage
    can_view = can_manage

    can_authenticated = [AuthenticatedUser(), SystemProcess()]
    can_all = [AnyUser(), SystemProcess()]

    can_handle_oer = [OERCertifiedUsers(), OERCurators(), SystemProcess()]

    #
    #  Records
    #
    # Allow searching of records
    can_search = can_all
    # Allow reading metadata of a record
    can_read = [
        IfRestricted("record", then_=can_view, else_=can_all),
    ]
    # Allow reading the files of a record
    can_read_files = [
        IfRestricted("files", then_=can_view, else_=can_all),
    ]
    can_get_content_files = [
        # note: even though this is closer to business logic than permissions,
        # it was simpler and less coupling to implement this as permission check
        IfFileIsLocal(then_=can_read_files, else_=[SystemProcess()]),
    ]
    # Allow submitting new record
    can_create = can_handle_oer

    #
    # Drafts
    #
    # Allow ability to search drafts
    can_search_drafts = can_handle_oer
    # Allow reading metadata of a draft
    can_read_draft = can_preview
    # Allow reading files of a draft
    can_draft_read_files = can_preview
    # Allow updating metadata of a draft
    can_update_draft = can_review
    # Allow uploading, updating and deleting files in drafts
    can_draft_create_files = can_review
    can_draft_set_content_files = [
        # if local then same permission as can_draft_create_files
        IfFileIsLocal(then_=can_review, else_=[SystemProcess()]),
    ]
    can_draft_get_content_files = [
        # if local then same permission as can_draft_read_files
        IfFileIsLocal(then_=can_preview, else_=[SystemProcess()]),
    ]
    can_draft_commit_files = [
        # if local then same permission as can_draft_create_files
        IfFileIsLocal(then_=can_review, else_=[SystemProcess()]),
    ]
    can_draft_update_files = can_review
    can_draft_delete_files = can_review

    #
    # PIDs
    #
    can_pid_create = can_review
    can_pid_register = can_review
    can_pid_update = can_review
    can_pid_discard = can_review
    can_pid_delete = can_review

    #
    # Actions
    #
    # Allow to put a record in edit mode (create a draft from record)
    can_edit = can_curate
    # Allow deleting/discarding a draft and all associated files
    can_delete_draft = can_curate
    # Allow creating a new version of an existing published record.
    can_new_version = can_curate
    # Allow publishing a new record or changes to an existing record.
    can_publish = can_review
    # Allow lifting a record or draft.
    can_lift_embargo = can_manage
