// This file is part of invenio-records-lom
// Copyright (C) 2022-2023 Graz University of Technology.
//
// invenio-records-lom is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React, { createRef } from "react";
import {
  DeleteButton,
  DepositFormApp,
  DepositStatusBox,
  FileUploader,
  FormFeedback,
  PreviewButton,
  PublishButton,
  SaveButton,
} from "react-invenio-deposit";
import { AccordionField } from "react-invenio-forms";
import {
  Card,
  Container,
  Grid,
  Icon,
  Message,
  Popup,
  Ref,
  Sticky,
} from "semantic-ui-react";
import { i18next } from "@translations/invenio_records_lom/i18next";

import {
  OptionalAccordion,
  RequiredAccordion,
  TestAccordion,
} from "./components";
import { DebugApiClient } from "./debug";
import { LOMDepositRecordSerializer } from "./serializers";

// TODO: convert to function copmponent
export default class LOMDepositForm extends React.Component {
  constructor(props) {
    super(props);
    this.config = props.config || {};

    // check if files are present
    this.noFiles = false;
    if (
      !Array.isArray(this.props.files.entries) ||
      (!this.props.files.entries.length && this.props.record.is_published)
    ) {
      this.noFiles = true;
    }
  }

  sidebarRef = createRef();

  render() {
    const recordSerializer = new LOMDepositRecordSerializer(
      this.config.current_locale || this.config.default_locale,
      this.config.vocabularies
    );
    return (
      <DepositFormApp
        config={this.config}
        files={this.props.files}
        permissions={this.props.permissions}
        preselectedCommunity={undefined}
        record={this.props.record}
        // below arguments overwrite default-behavior
        apiClient={
          new DebugApiClient(this.props.config.createUrl, recordSerializer)
        }
        recordSerializer={recordSerializer}
        // apiClient={new LOMDepositApiClient()}  // defaults to RDM
        // fileApiClient={new LOMDepositFileApiClient()}  // defaults to RDMDepositFileApiClient
        // draftsService={new LOMDepositDraftsService()}  // defaults to RDMDepositDraftsService, which defers to apiClient
        // filesService={new LOMDepositFilesService()}  // defaults to RDMDeposiFilesService, which defers to fileApiClient
      >
        <FormFeedback
          fieldPath="message"
          labels={{
            // TODO:
            // uses paths of length two for now
            // this works for now, as every category has only one sub-field that can have errors
            // use longer paths once implemented in invenio...
            "metadata.general": i18next.t("Title"),
            "metadata.lifecycle": i18next.t("Contributors"),
            "metadata.technical": i18next.t("Format"),
            "metadata.educational": i18next.t("Resource Type"),
            "metadata.rights": i18next.t("License"),
            "metadata.classification": i18next.t("OEFOS"),
          }}
        />
        {/* TODO: Community-Header */}
        <Container id="deposit-form" className="rel-mt-1">
          <Grid className="mt-25">
            <Grid.Column mobile={16} tablet={16} computer={11}>
              <AccordionField
                active
                includesPaths={["files.enabled"]}
                label={
                  <>
                    <Icon
                      color="red"
                      name="asterisk"
                      style={{ float: "left", marginRight: 14 }}
                    />
                    {i18next.t("Files")}
                  </>
                }
              >
                {this.noFiles && this.props.record.is_published && (
                  <div className="text-align-center pb-10">
                    <em>{i18next.t("The record has no files.")}</em>
                  </div>
                )}
                <FileUploader
                  isDraftRecord={!this.props.record.is_published}
                  quota={this.config.quota}
                  decimalSizeDisplay={this.config.decimal_size_display}
                />
              </AccordionField>
              <RequiredAccordion />
              <OptionalAccordion />
              {/*<TestAccordion />*/}
            </Grid.Column>
            <Ref innerRef={this.sidebarRef}>
              <Grid.Column
                mobile={16}
                tablet={16}
                computer={5}
                className="deposit-sidebar"
              >
                <Sticky context={this.sidebarRef} offset={20}>
                  <Card>
                    <Card.Content>
                      <DepositStatusBox />
                    </Card.Content>
                    <Card.Content>
                      <Grid relaxed>
                        <Grid.Column
                          computer={8}
                          mobile={16}
                          className="pb-0 left-btn-col"
                        >
                          <SaveButton fluid />
                        </Grid.Column>

                        <Grid.Column
                          computer={8}
                          mobile={16}
                          className="pb-0 right-btn-col"
                        >
                          <PreviewButton fluid />
                        </Grid.Column>

                        <Grid.Column width={16} className="pt-10">
                          <PublishButton fluid />
                        </Grid.Column>
                      </Grid>
                    </Card.Content>
                  </Card>
                  <Card className="access-right">
                    <Card.Content>
                      <Card.Header>
                        <label
                          className="field-label-class invenio-field-label"
                          htmlFor="access"
                        >
                          <Icon name="shield" />
                          {i18next.t("Visibility")}
                          <Popup
                            trigger={
                              <Icon className="ml-10" name="info circle" />
                            }
                            content={i18next.t(
                              "OER-uploads are always public."
                            )}
                          />
                        </label>
                      </Card.Header>
                    </Card.Content>
                    <Card.Content>
                      <Message
                        icon
                        positive
                        visible
                        data-test-id="access-message"
                      >
                        <Icon name="lock open" />
                        <Message.Content>
                          <Message.Header>{i18next.t("Public")}</Message.Header>
                          {i18next.t(
                            "The record and files are publicly accessible."
                          )}
                        </Message.Content>
                      </Message>
                    </Card.Content>
                  </Card>
                  <Card>
                    <Card.Content>
                      <DeleteButton
                        fluid
                        isPublished={this.props.record.is_published}
                      />
                    </Card.Content>
                  </Card>
                </Sticky>
              </Grid.Column>
            </Ref>
          </Grid>
        </Container>
      </DepositFormApp>
    );
  }
}
