## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />

<%def name="extra_styles()">
  ${parent.extra_styles()}
  <style type="text/css">
    .card.personal {
        margin-bottom: 1rem;
    }
    .field.is-horizontal .field-label .label {
        white-space: nowrap;
        min-width: 10rem;
    }
  </style>
</%def>

<%def name="content_title()">
  ${dynamic_content_title}
</%def>

<%def name="render_instance_header_title_extras()">
  % if request.has_perm('people_profile.view_versions'):
      <div class="level-item" style="margin-left: 2rem;">
        <b-button v-if="!viewingHistory"
                  icon-pack="fas"
                  icon-left="history"
                  @click="viewHistory()">
          View History
        </b-button>
        <div v-if="viewingHistory"
             class="buttons">
          <b-button icon-pack="fas"
                    icon-left="user"
                    @click="viewingHistory = false">
            View Profile
          </b-button>
          <b-button icon-pack="fas"
                    icon-left="redo"
                    @click="refreshHistory()"
                    :disabled="gettingRevisions">
            {{ gettingRevisions ? "Working, please wait..." : "Refresh History" }}
          </b-button>
        </div>
      </div>
  % endif
</%def>

<%def name="page_content()">
  <profile-info @change-content-title="changeContentTitle"
                % if request.has_perm('people_profile.view_versions'):
                :viewing-history="viewingHistory"
                :getting-revisions="gettingRevisions"
                :revisions="revisions"
                :revision-version-map="revisionVersionMap"
                % endif
                >
  </profile-info>
</%def>

<%def name="render_this_page_component()">
  ## TODO: should override this in a cleaner way!  too much duplicate code w/ parent template
  <this-page @change-content-title="changeContentTitle"
             % if can_edit_help:
             :configure-fields-help="configureFieldsHelp"
             % endif
             % if request.has_perm('people_profile.view_versions'):
             :viewing-history="viewingHistory"
             :getting-revisions="gettingRevisions"
             :revisions="revisions"
             :revision-version-map="revisionVersionMap"
             % endif
             >
  </this-page>
</%def>

<%def name="render_this_page()">
  ${self.page_content()}
</%def>

<%def name="render_personal_name_card()">
  <div class="card personal">
    <header class="card-header">
      <p class="card-header-title">Name</p>
    </header>
    <div class="card-content">
      <div class="content">
        <div style="display: flex; justify-content: space-between;">
          <div style="flex-grow: 1; margin-right: 1rem;">

            <b-field horizontal label="First Name">
              <span>{{ person.first_name }}</span>
            </b-field>

            <b-field horizontal label="Middle Name">
              <span>{{ person.middle_name }}</span>
            </b-field>

            <b-field horizontal label="Last Name">
              <span>{{ person.last_name }}</span>
            </b-field>

          </div>
          % if request.has_perm('people_profile.edit_person'):
              <div v-if="editNameAllowed()">
                <b-button type="is-primary"
                          @click="editNameInit()"
                          icon-pack="fas"
                          icon-left="edit">
                  Edit Name
                </b-button>
              </div>
              <b-modal has-modal-card
                       :active.sync="editNameShowDialog">
                <div class="modal-card">

                  <header class="modal-card-head">
                    <p class="modal-card-title">Edit Name</p>
                  </header>

                  <section class="modal-card-body">
                    <b-field label="First Name">
                      <b-input v-model.trim="personFirstName"
                               :maxlength="maxLengths.person_first_name || null">
                      </b-input>
                    </b-field>
                    <b-field label="Middle Name">
                      <b-input v-model.trim="personMiddleName"
                               :maxlength="maxLengths.person_middle_name || null">
                      </b-input>
                    </b-field>
                    <b-field label="Last Name">
                      <b-input v-model.trim="personLastName"
                               :maxlength="maxLengths.person_last_name || null">
                      </b-input>
                    </b-field>
                  </section>

                  <footer class="modal-card-foot">
                    <once-button type="is-primary"
                                 @click="editNameSave()"
                                 :disabled="editNameSaveDisabled"
                                 icon-left="save"
                                 text="Save">
                    </once-button>
                    <b-button @click="editNameShowDialog = false">
                      Cancel
                    </b-button>
                  </footer>
                </div>
              </b-modal>
          % endif
        </div>
      </div>
    </div>
  </div>
</%def>

<%def name="render_personal_address_card()">
  <div class="card personal">
    <header class="card-header">
      <p class="card-header-title">Address</p>
    </header>
    <div class="card-content">
      <div class="content">
        <div style="display: flex; justify-content: space-between;">
          <div style="flex-grow: 1; margin-right: 1rem;">

            <b-field horizontal label="Street 1">
              <span>{{ person.address ? person.address.street : null }}</span>
            </b-field>

            <b-field horizontal label="Street 2">
              <span>{{ person.address ? person.address.street2 : null }}</span>
            </b-field>

            <b-field horizontal label="City">
              <span>{{ person.address ? person.address.city : null }}</span>
            </b-field>

            <b-field horizontal label="State">
              <span>{{ person.address ? person.address.state : null }}</span>
            </b-field>

            <b-field horizontal label="Zipcode">
              <span>{{ person.address ? person.address.zipcode : null }}</span>
            </b-field>

            <b-field v-if="person.address && person.address.invalid"
                     horizontal label="Invalid"
                     class="has-text-danger">
              <span>Yes</span>
            </b-field>

          </div>
          % if request.has_perm('people_profile.edit_person'):
              <b-button type="is-primary"
                        @click="editAddressInit()"
                        icon-pack="fas"
                        icon-left="edit">
                Edit Address
              </b-button>
              <b-modal has-modal-card
                       :active.sync="editAddressShowDialog">
                <div class="modal-card">

                  <header class="modal-card-head">
                    <p class="modal-card-title">Edit Address</p>
                  </header>

                  <section class="modal-card-body">

                    <b-field label="Street 1" expanded>
                      <b-input v-model.trim="personStreet1"
                               :maxlength="maxLengths.address_street || null">
                      </b-input>
                    </b-field>

                    <b-field label="Street 2" expanded>
                      <b-input v-model.trim="personStreet2"
                               :maxlength="maxLengths.address_street2 || null">
                      </b-input>
                    </b-field>

                    <b-field label="Zipcode">
                      <b-input v-model.trim="personZipcode"
                               :maxlength="maxLengths.address_zipcode || null">
                      </b-input>
                    </b-field>

                    <b-field grouped>
                      <b-field label="City">
                        <b-input v-model.trim="personCity"
                                 :maxlength="maxLengths.address_city || null">
                        </b-input>
                      </b-field>
                      <b-field label="State">
                        <b-input v-model.trim="personState"
                                 :maxlength="maxLengths.address_state || null">
                        </b-input>
                      </b-field>
                    </b-field>

                    <b-field label="Invalid">
                      <b-checkbox v-model="personInvalidAddress"
                                  type="is-danger">
                      </b-checkbox>
                    </b-field>

                  </section>

                  <footer class="modal-card-foot">
                    <once-button type="is-primary"
                                 @click="editAddressSave()"
                                 :disabled="editAddressSaveDisabled"
                                 icon-left="save"
                                 text="Save">
                    </once-button>
                    <b-button @click="editAddressShowDialog = false">
                      Cancel
                    </b-button>
                  </footer>
                </div>
              </b-modal>
          % endif
        </div>
      </div>
    </div>
  </div>
</%def>

<%def name="render_personal_phone_card()">
  <div class="card personal">
    <header class="card-header">
      <p class="card-header-title">Phone(s)</p>
    </header>
    <div class="card-content">
      <div class="content">

        <b-notification v-if="person.invalid_phone_number"
                        type="is-warning"
                        has-icon icon-pack="fas"
                        :closable="false">
          We appear to have an invalid phone number on file for this person.
        </b-notification>

        % if request.has_perm('people_profile.edit_person'):
            <div class="has-text-right">
              <b-button type="is-primary"
                        icon-pack="fas"
                        icon-left="plus"
                        @click="addPhoneInit()">
                Add Phone
              </b-button>
            </div>
            <b-modal has-modal-card
                     :active.sync="editPhoneShowDialog">
              <div class="modal-card">

                <header class="modal-card-head">
                  <p class="modal-card-title">
                    {{ phoneUUID ? "Edit Phone" : "Add Phone" }}
                  </p>
                </header>

                <section class="modal-card-body">
                  <b-field grouped>

                    <b-field label="Type" expanded>
                      <b-select v-model="phoneType" expanded>
                        <option v-for="option in phoneTypeOptions"
                                :key="option.value"
                                :value="option.value">
                          {{ option.label }}
                        </option>
                      </b-select>
                    </b-field>

                    <b-field label="Number" expanded>
                      <b-input v-model.trim="phoneNumber"
                               ref="editPhoneInput">
                      </b-input>
                    </b-field>
                  </b-field>

                  <b-field label="Preferred?">
                    <b-checkbox v-model="phonePreferred">
                    </b-checkbox>
                  </b-field>

                </section>

                <footer class="modal-card-foot">
                  <b-button type="is-primary"
                            @click="editPhoneSave()"
                            :disabled="editPhoneSaveDisabled"
                            icon-pack="fas"
                            icon-left="save">
                    {{ editPhoneSaveText }}
                  </b-button>
                  <b-button @click="editPhoneShowDialog = false">
                    Cancel
                  </b-button>
                </footer>
              </div>
            </b-modal>
        % endif

        <b-table :data="person.phones">

          <b-table-column field="preference"
                          label="Preferred"
                          v-slot="props">
            {{ props.row.preferred ? "Yes" : "" }}
          </b-table-column>

          <b-table-column field="type"
                          label="Type"
                          v-slot="props">
            {{ props.row.type }}
          </b-table-column>

          <b-table-column field="number"
                          label="Number"
                          v-slot="props">
            {{ props.row.number }}
          </b-table-column>

          % if request.has_perm('people_profile.edit_person'):
          <b-table-column label="Actions"
                          v-slot="props">
            <a href="#" @click.prevent="editPhoneInit(props.row)">
              <i class="fas fa-edit"></i>
              Edit
            </a>
            <a href="#" @click.prevent="deletePhone(props.row)"
               class="has-text-danger">
              <i class="fas fa-trash"></i>
              Delete
            </a>
            <a href="#" @click.prevent="setPreferredPhone(props.row)"
               v-if="!props.row.preferred">
              <i class="fas fa-star"></i>
              Set Preferred
            </a>
          </b-table-column>
          % endif

        </b-table>

      </div>
    </div>
  </div>
</%def>

<%def name="render_personal_email_card()">
  <div class="card personal">
    <header class="card-header">
      <p class="card-header-title">Email(s)</p>
    </header>
    <div class="card-content">
      <div class="content">

        % if request.has_perm('people_profile.edit_person'):
            <div class="has-text-right">
              <b-button type="is-primary"
                        icon-pack="fas"
                        icon-left="plus"
                        @click="addEmailInit()">
                Add Email
              </b-button>
            </div>
            <b-modal has-modal-card
                     :active.sync="editEmailShowDialog">
              <div class="modal-card">

                <header class="modal-card-head">
                  <p class="modal-card-title">
                    {{ emailUUID ? "Edit Email" : "Add Email" }}
                  </p>
                </header>

                <section class="modal-card-body">
                  <b-field grouped>

                    <b-field label="Type" expanded>
                      <b-select v-model="emailType" expanded>
                        <option v-for="option in emailTypeOptions"
                                :key="option.value"
                                :value="option.value">
                          {{ option.label }}
                        </option>
                      </b-select>
                    </b-field>

                    <b-field label="Address" expanded>
                      <b-input v-model.trim="emailAddress"
                               ref="editEmailInput">
                      </b-input>
                    </b-field>

                  </b-field>

                  <b-field v-if="!emailUUID"
                           label="Preferred?">
                    <b-checkbox v-model="emailPreferred">
                    </b-checkbox>
                  </b-field>

                  <b-field v-if="emailUUID"
                           label="Invalid?">
                    <b-checkbox v-model="emailInvalid"
                                :type="emailInvalid ? 'is-danger': null">
                    </b-checkbox>
                  </b-field>

                </section>

                <footer class="modal-card-foot">
                  <b-button type="is-primary"
                            @click="editEmailSave()"
                            :disabled="editEmailSaveDisabled"
                            icon-pack="fas"
                            icon-left="save">
                    {{ editEmailSaveText }}
                  </b-button>
                  <b-button @click="editEmailShowDialog = false">
                    Cancel
                  </b-button>
                </footer>
              </div>
            </b-modal>
        % endif

        <b-table :data="person.emails">

          <b-table-column field="preference"
                          label="Preferred"
                          v-slot="props">
            {{ props.row.preferred ? "Yes" : "" }}
          </b-table-column>

          <b-table-column field="type"
                          label="Type"
                          v-slot="props">
            {{ props.row.type }}
          </b-table-column>

          <b-table-column field="address"
                          label="Address"
                          v-slot="props">
            {{ props.row.address }}
          </b-table-column>

          <b-table-column field="invalid"
                          label="Invalid?"
                          v-slot="props">
            <span v-if="props.row.invalid" class="has-text-danger has-text-weight-bold">Invalid</span>
          </b-table-column>

          % if request.has_perm('people_profile.edit_person'):
              <b-table-column label="Actions"
                              v-slot="props">
                <a href="#" @click.prevent="editEmailInit(props.row)">
                  <i class="fas fa-edit"></i>
                  Edit
                </a>
                <a href="#" @click.prevent="deleteEmail(props.row)"
                   class="has-text-danger">
                  <i class="fas fa-trash"></i>
                  Delete
                </a>
                <a href="#" @click.prevent="setPreferredEmail(props.row)"
                   v-if="!props.row.preferred">
                  <i class="fas fa-star"></i>
                  Set Preferred
                </a>
              </b-table-column>
          % endif

        </b-table>

      </div>
    </div>
  </div>
</%def>

<%def name="render_personal_tab_cards()">
  ${self.render_personal_name_card()}
  ${self.render_personal_address_card()}
  ${self.render_personal_phone_card()}
  ${self.render_personal_email_card()}
</%def>

<%def name="render_personal_tab_template()">
  <script type="text/x-template" id="personal-tab-template">
    <div style="display: flex; justify-content: space-between;">

      <div style="flex-grow: 1; margin-right: 1rem;">
        ${self.render_personal_tab_cards()}
      </div>

      <div>
        % if request.has_perm('people.view'):
            ${h.link_to("View Person", url('people.view', uuid=person.uuid), class_='button')}
        % endif
      </div>

    </div>
  </script>
</%def>

<%def name="render_personal_tab()">
  <b-tab-item label="Personal"
              value="personal"
              icon-pack="fas"
              icon="check">
    <personal-tab :person="person"
                  :member="member"
                  :max-lengths="maxLengths"
                  :phone-type-options="phoneTypeOptions"
                  :email-type-options="emailTypeOptions"
                  @person-updated="personUpdated"
                  @change-content-title="changeContentTitle">
    </personal-tab>
  </b-tab-item>
</%def>

<%def name="render_member_tab()">
  <b-tab-item label="Member"
              value="member"
              icon-pack="fas"
              :icon="members.length ? 'check' : null">

    <div v-if="members.length">

      <div style="display: flex; justify-content: space-between;">
        <p>{{ person.display_name }} has <strong>{{ members.length }}</strong> member account{{ members.length == 1 ? '' : 's' }}</p>
      </div>

      <br />
      <b-collapse v-for="member in members"
                  :key="member.uuid"
                  class="panel"
                  :open="members.length == 1">

        <div slot="trigger"
             slot-scope="props"
             class="panel-heading"
             role="button">
          <b-icon pack="fas"
                  icon="caret-right">
          </b-icon>
          <strong>{{ member._key }} - {{ member.display }}</strong>
        </div>

        <div class="panel-block">
          <div style="display: flex; justify-content: space-between; width: 100%;">
            <div style="flex-grow: 1;">

              <b-field horizontal label="${member_key_label}">
                {{ member._key }}
              </b-field>

              <b-field horizontal label="Account Holder">
                <a v-if="member.person_uuid != person.uuid"
                   :href="member.view_profile_url">
                  {{ member.person_display_name }}
                </a>
                <span v-if="member.person_uuid == person.uuid">
                  {{ member.person_display_name }}
                </span>
              </b-field>

              <b-field horizontal label="Membership Type">
                <a v-if="member.view_membership_type_url"
                   :href="member.view_membership_type_url">
                  {{ member.membership_type_name }}
                </a>
                <span v-if="!member.view_membership_type_url">
                  {{ member.membership_type_name }}
                </span>
              </b-field>

              <b-field horizontal label="Active">
                {{ member.active ? "Yes" : "No" }}
              </b-field>

              <b-field horizontal label="Joined">
                {{ member.joined }}
              </b-field>

              <b-field horizontal label="Withdrew"
                       v-if="member.withdrew">
                {{ member.withdrew }}
              </b-field>

              <b-field horizontal label="Equity Total">
                {{ member.equity_total_display }}
              </b-field>

            </div>
            <div class="buttons" style="align-items: start;">
              ${self.render_member_panel_buttons(member)}
            </div>
          </div>
        </div>
      </b-collapse>
    </div>

    <div v-if="!members.length">
      <p>{{ person.display_name }} does not have a member account.</p>
    </div>

  </b-tab-item>
</%def>

<%def name="render_member_panel_buttons(member)">
  % for button in member_xref_buttons:
      ${button}
  % endfor
  % if request.has_perm('members.view'):
      <b-button tag="a" :href="member.view_url">
        View Member
      </b-button>
  % endif
</%def>

<%def name="render_customer_tab()">
  <b-tab-item label="Customer"
              value="customer"
              icon-pack="fas"
              :icon="customers.length ? 'check' : null">

    <div v-if="customers.length">

      <div style="display: flex; justify-content: space-between;">
        <p>{{ person.display_name }} has <strong>{{ customers.length }}</strong> customer account{{ customers.length == 1 ? '' : 's' }}</p>
      </div>

      <br />
      <b-collapse v-for="customer in customers"
                  :key="customer.uuid"
                  class="panel"
                  :open="customers.length == 1">

        <div slot="trigger"
             slot-scope="props"
             class="panel-heading"
             role="button">
          <b-icon pack="fas"
                  icon="caret-right">
          </b-icon>
          <strong>{{ customer._key }} - {{ customer.name }}</strong>
        </div>

        <div class="panel-block">
          <div style="display: flex; justify-content: space-between; width: 100%;">
            <div style="flex-grow: 1;">

              <b-field horizontal label="${customer_key_label}">
                {{ customer._key }}
              </b-field>

              <b-field horizontal label="Account Name">
                {{ customer.name }}
              </b-field>

              % if expose_customer_shoppers:
                  <b-field horizontal label="Shoppers">
                    <ul>
                      <li v-for="shopper in customer.shoppers"
                          :key="shopper.uuid">
                        <a v-if="shopper.person_uuid != person.uuid"
                           :href="shopper.view_profile_url">
                          {{ shopper.display_name }}
                        </a>
                        <span v-if="shopper.person_uuid == person.uuid">
                          {{ shopper.display_name }}
                        </span>
                      </li>
                    </ul>
                  </b-field>
              % endif

              % if expose_customer_people:
                  <b-field horizontal label="People">
                    <ul>
                      <li v-for="p in customer.people"
                          :key="p.uuid">
                        <a v-if="p.uuid != person.uuid"
                           :href="p.view_profile_url">
                          {{ p.display_name }}
                        </a>
                        <span v-if="p.uuid == person.uuid">
                          {{ p.display_name }}
                        </span>
                      </li>
                    </ul>
                  </b-field>
              % endif

              <b-field horizontal label="Address"
                       v-for="address in customer.addresses"
                       :key="address.uuid">
                {{ address.display }}
              </b-field>

            </div>
            <div class="buttons" style="align-items: start;">
              ${self.render_customer_panel_buttons(customer)}
            </div>
          </div>
        </div>
      </b-collapse>
    </div>

    <div v-if="!customers.length">
      <p>{{ person.display_name }} does not have a customer account.</p>
    </div>

  </b-tab-item> <!-- Customer -->
</%def>

<%def name="render_customer_panel_buttons(customer)">
  <b-button v-for="link in customer.external_links"
            :key="link.url"
            type="is-primary"
            tag="a" :href="link.url" target="_blank"
            icon-pack="fas"
            icon-left="external-link-alt">
    {{ link.label }}
  </b-button>
  % if request.has_perm('customers.view'):
      <b-button tag="a" :href="customer.view_url">
        View Customer
      </b-button>
  % endif
</%def>

<%def name="render_shopper_tab()">
  <b-tab-item label="Shopper"
              value="shopper"
              icon-pack="fas"
              :icon="shoppers.length ? 'check' : null">

    <div v-if="shoppers.length">

      <div style="display: flex; justify-content: space-between;">
        <p>{{ person.display_name }} is shopper for <strong>{{ shoppers.length }}</strong> customer account{{ shoppers.length == 1 ? '' : 's' }}</p>
      </div>

      <br />
      <b-collapse v-for="shopper in shoppers"
                  :key="shopper.uuid"
                  class="panel"
                  :open="shoppers.length == 1">

        <div slot="trigger"
             slot-scope="props"
             class="panel-heading"
             role="button">
          <b-icon pack="fas"
                  icon="caret-right">
          </b-icon>
          <strong>{{ shopper.customer_key }} - {{ shopper.customer_name }}</strong>
        </div>

        <div class="panel-block">
          <div style="display: flex; justify-content: space-between; width: 100%;">
            <div style="flex-grow: 1;">

              <b-field horizontal label="${customer_key_label}">
                {{ shopper.customer_key }}
              </b-field>

              <b-field horizontal label="Account Name">
                {{ shopper.customer_name }}
              </b-field>

              <b-field horizontal label="Account Holder">
                <span v-if="!shopper.account_holder_view_profile_url">
                  {{ shopper.account_holder_name }}
                </span>
                <a v-if="shopper.account_holder_view_profile_url"
                   :href="shopper.account_holder_view_profile_url">
                  {{ shopper.account_holder_name }}
                </a>
              </b-field>

            </div>
##             <div class="buttons" style="align-items: start;">
##               ${self.render_shopper_panel_buttons(shopper)}
##             </div>
          </div>
        </div>
      </b-collapse>
    </div>

    <div v-if="!shoppers.length">
      <p>{{ person.display_name }} is not a shopper.</p>
    </div>

  </b-tab-item> <!-- Shopper -->
</%def>

<%def name="render_employee_tab_template()">
  <script type="text/x-template" id="employee-tab-template">
    <div>
      <div style="display: flex; justify-content: space-between;">

        <div style="flex-grow: 1;">

          <div v-if="employee.uuid">

            <b-field horizontal label="Employee ID">
              <div class="level">
                <div class="level-left">
                  <div class="level-item">
                    <span>{{ employee.id }}</span>
                  </div>
                  % if request.has_perm('employees.edit'):
                      <div class="level-item">
                        <b-button type="is-primary"
                                  icon-pack="fas"
                                  icon-left="edit"
                                  @click="initEditEmployeeID()">
                          Edit ID
                        </b-button>
                        <b-modal has-modal-card
                                 :active.sync="showEditEmployeeIDDialog">
                          <div class="modal-card">

                            <header class="modal-card-head">
                              <p class="modal-card-title">Employee ID</p>
                            </header>

                            <section class="modal-card-body">
                              <b-field label="Employee ID">
                                <b-input v-model="newEmployeeID"></b-input>
                              </b-field>
                            </section>

                            <footer class="modal-card-foot">
                              <b-button @click="showEditEmployeeIDDialog = false">
                                Cancel
                              </b-button>
                              <b-button type="is-primary"
                                        icon-pack="fas"
                                        icon-left="save"
                                        :disabled="updatingEmployeeID"
                                        @click="updateEmployeeID()">
                                {{ editEmployeeIDSaveButtonText }}
                              </b-button>
                            </footer>
                          </div>
                        </b-modal>
                      </div>
                  % endif
                </div>
              </div>
            </b-field>

            <b-field horizontal label="Employee Status">
              <span>{{ employee.status_display }}</span>
            </b-field>

            <b-field horizontal label="Start Date">
              <span>{{ employee.start_date }}</span>
            </b-field>

            <b-field horizontal label="End Date">
              <span>{{ employee.end_date }}</span>
            </b-field>

            <br />
            <p><strong>Employee History</strong></p>
            <br />

            <b-table :data="employeeHistory">

              <b-table-column field="start_date"
                              label="Start Date"
                              v-slot="props">
                {{ props.row.start_date }}
              </b-table-column>

              <b-table-column field="end_date"
                              label="End Date"
                              v-slot="props">
                {{ props.row.end_date }}
              </b-table-column>

              % if request.has_perm('people_profile.edit_employee_history'):
                  <b-table-column field="actions"
                                  label="Actions"
                                  v-slot="props">
                    <a href="#" @click.prevent="editEmployeeHistory(props.row)">
                      <i class="fas fa-edit"></i>
                      Edit
                    </a>
                  </b-table-column>
              % endif

            </b-table>

          </div>

          <p v-if="!employee.uuid">
            ${person} is not an employee.
          </p>

        </div>

        <div>
          <div class="buttons">

            % if request.has_perm('people_profile.toggle_employee'):

                <b-button v-if="!employee.current"
                          type="is-primary"
                          @click="startEmployeeInit()">
                  ${person} is now an Employee
                </b-button>

                <b-button v-if="employee.current"
                          type="is-primary"
                          @click="showStopEmployeeDialog = true">
                  ${person} is no longer an Employee
                </b-button>

                <b-modal has-modal-card
                         :active.sync="startEmployeeShowDialog">
                  <div class="modal-card">

                    <header class="modal-card-head">
                      <p class="modal-card-title">Employee Start</p>
                    </header>

                    <section class="modal-card-body">
                      <b-field label="Employee Number">
                        <b-input v-model="employeeID"></b-input>
                      </b-field>
                      <b-field label="Start Date">
                        <tailbone-datepicker v-model="employeeStartDate"></tailbone-datepicker>
                      </b-field>
                    </section>

                    <footer class="modal-card-foot">
                      <b-button @click="startEmployeeShowDialog = false">
                        Cancel
                      </b-button>
                      <once-button type="is-primary"
                                   @click="startEmployee()"
                                   :disabled="!employeeStartDate"
                                   text="Save">
                      </once-button>
                    </footer>
                  </div>
                </b-modal>

                <b-modal has-modal-card
                         :active.sync="showStopEmployeeDialog">
                  <div class="modal-card">

                    <header class="modal-card-head">
                      <p class="modal-card-title">Employee End</p>
                    </header>

                    <section class="modal-card-body">
                      <b-field label="End Date"
                               :type="employeeEndDate ? null : 'is-danger'">
                        <tailbone-datepicker v-model="employeeEndDate"></tailbone-datepicker>
                      </b-field>
                      <b-field label="Revoke Internal App Access">
                        <b-checkbox v-model="employeeRevokeAccess">
                        </b-checkbox>
                      </b-field>
                    </section>

                    <footer class="modal-card-foot">
                      <b-button @click="showStopEmployeeDialog = false">
                        Cancel
                      </b-button>
                      <once-button type="is-primary"
                                   @click="endEmployee()"
                                   :disabled="!employeeEndDate"
                                   text="Save">
                      </once-button>
                    </footer>
                  </div>
                </b-modal>
            % endif

            % if request.has_perm('people_profile.edit_employee_history'):
                <b-modal has-modal-card
                         :active.sync="showEditEmployeeHistoryDialog">
                  <div class="modal-card">

                    <header class="modal-card-head">
                      <p class="modal-card-title">Edit Employee History</p>
                    </header>

                    <section class="modal-card-body">
                      <b-field label="Start Date">
                        <tailbone-datepicker v-model="employeeHistoryStartDate"></tailbone-datepicker>
                      </b-field>
                      <b-field label="End Date">
                        <tailbone-datepicker v-model="employeeHistoryEndDate"
                                             :disabled="!employeeHistoryEndDateRequired">
                        </tailbone-datepicker>
                      </b-field>
                    </section>

                    <footer class="modal-card-foot">
                      <b-button @click="showEditEmployeeHistoryDialog = false">
                        Cancel
                      </b-button>
                      <once-button type="is-primary"
                                   @click="saveEmployeeHistory()"
                                   :disabled="!employeeHistoryStartDate || (employeeHistoryEndDateRequired && !employeeHistoryEndDate)"
                                   text="Save">
                      </once-button>
                    </footer>
                  </div>
                </b-modal>
            % endif

            % if request.has_perm('employees.view'):
                <b-button v-if="employee.view_url"
                          tag="a" :href="employee.view_url">
                  View Employee
                </b-button>
            % endif

          </div>
        </div>

      </div>
    </div>
  </script>
</%def>

<%def name="render_employee_tab()">
  <b-tab-item label="Employee"
              value="employee"
              icon-pack="fas"
              :icon="employee.current ? 'check' : null">
    <employee-tab :employee="employee"
                  :employee-history="employeeHistory"
                  @employee-updated="employeeUpdated"
                  @employee-history-updated="employeeHistoryUpdated"
                  @change-content-title="changeContentTitle">
    </employee-tab>
  </b-tab-item>
</%def>

<%def name="render_notes_tab_template()">
  <script type="text/x-template" id="notes-tab-template">
    <div>

      % if request.has_perm('people_profile.add_note'):
          <b-button type="is-primary"
                    class="control"
                    @click="noteNew()"
                    icon-pack="fas"
                    icon-left="plus">
            Add Note
          </b-button>
      % endif

      <b-table :data="notes">

        <b-table-column field="note_type"
                        label="Type"
                        v-slot="props">
          {{ props.row.note_type_display }}
        </b-table-column>

        <b-table-column field="subject"
                        label="Subject"
                        v-slot="props">
          {{ props.row.subject }}
        </b-table-column>

        <b-table-column field="text"
                        label="Text"
                        v-slot="props">
          {{ props.row.text }}
        </b-table-column>

        <b-table-column field="created"
                        label="Created"
                        v-slot="props">
          <span v-html="props.row.created_display"></span>
        </b-table-column>

        <b-table-column field="created_by"
                        label="Created By"
                        v-slot="props">
          {{ props.row.created_by_display }}
        </b-table-column>

        % if request.has_any_perm('people_profile.edit_note', 'people_profile.delete_note'):
            <b-table-column label="Actions"
                            v-slot="props">
              % if request.has_perm('people_profile.edit_note'):
                  <a href="#" @click.prevent="noteEdit(props.row)">
                    <i class="fas fa-edit"></i>
                    Edit
                  </a>
              % endif
              % if request.has_perm('people_profile.delete_note'):
                  <a href="#" @click.prevent="noteDelete(props.row)"
                     class="has-text-danger">
                    <i class="fas fa-trash"></i>
                    Delete
                  </a>
              % endif
            </b-table-column>
        % endif

      </b-table>

      <b-modal :active.sync="noteShowDialog"
               has-modal-card>

        <div class="modal-card">

          <header class="modal-card-head">
            <p class="modal-card-title">
              {{ noteDialogTitle }}
            </p>
          </header>

          <section class="modal-card-body">

            <b-field label="Type"
                     :type="!noteDeleting && !noteType ? 'is-danger' : null">
              <b-select v-model="noteType"
                        :disabled="noteUUID">
                <option v-for="option in noteTypeOptions"
                        :key="option.value"
                        :value="option.value">
                  {{ option.label }}
                </option>
              </b-select>
            </b-field>

            <b-field label="Subject">
              <b-input v-model.trim="noteSubject"
                       :disabled="noteDeleting">
              </b-input>
            </b-field>

            <b-field label="Text">
              <b-input v-model.trim="noteText"
                       type="textarea"
                       :disabled="noteDeleting">
              </b-input>
            </b-field>

            <b-notification v-if="noteDeleting"
                            type="is-danger"
                            :closable="false">
              Are you sure you wish to delete this note?
            </b-notification>

          </section>

          <footer class="modal-card-foot">
            <b-button :type="noteDeleting ? 'is-danger' : 'is-primary'"
                      @click="noteSave()"
                      :disabled="noteSaving || (!noteDeleting && !noteType)"
                      icon-pack="fas"
                      icon-left="save">
              {{ noteSaving ? "Working, please wait..." : noteSaveText }}
            </b-button>
            <b-button @click="noteShowDialog = false">
              Cancel
            </b-button>
          </footer>

        </div>
      </b-modal>

    </div>
  </script>
</%def>

<%def name="render_notes_tab()">
  <b-tab-item label="Notes"
              value="notes"
              icon-pack="fas"
              :icon="notes.length ? 'check' : null">

    <notes-tab :notes="notes"
               :note-type-options="noteTypeOptions"
               @new-notes-data="newNotesData">
    </notes-tab>

  </b-tab-item>
</%def>

<%def name="render_user_tab()">
  <b-tab-item label="User"
              value="user"
              icon-pack="fas"
              :icon="users.length ? 'check' : null">

    <div v-if="users.length">

      <p>{{ person.display_name }} has <strong>{{ users.length }}</strong> user account{{ users.length == 1 ? '' : 's' }}</p>
      <br />
      <div id="users-accordion">

        <b-collapse class="panel"
                    v-for="user in users"
                    :key="user.uuid">

          <div slot="trigger"
               class="panel-heading"
               role="button">
            <strong>{{ user.username }}</strong>
          </div>

          <div class="panel-block">
            <div style="display: flex; justify-content: space-between; width: 100%;">

              <div>
                <div class="field-wrapper id">
                  <div class="field-row">
                    <label>Username</label>
                    <div class="field">
                      {{ user.username }}
                    </div>
                  </div>
                </div>
              </div>

              <div>
                % if request.has_perm('users.view'):
                    <b-button tag="a" :href="user.view_url">
                      View User
                    </b-button>
                % endif
              </div>

            </div>
          </div>
        </b-collapse>
      </div>
    </div>

    <div v-if="!users.length">
      <p>{{ person.display_name }} does not have a user account.</p>
    </div>
  </b-tab-item><!-- User -->
</%def>

<%def name="render_profile_tabs()">
  ${self.render_personal_tab()}
  ${self.render_member_tab()}
  ${self.render_customer_tab()}
  % if expose_customer_shoppers:
  ${self.render_shopper_tab()}
  % endif
  ${self.render_employee_tab()}
  ${self.render_notes_tab()}
  ${self.render_user_tab()}
</%def>

<%def name="render_profile_info_extra_buttons()"></%def>

<%def name="render_profile_info_template()">
  <script type="text/x-template" id="profile-info-template">
    <div>

      ${self.render_profile_info_extra_buttons()}

      <b-tabs v-model="activeTab"
              % if request.has_perm('people_profile.view_versions'):
              v-show="!viewingHistory"
              % endif
              type="is-boxed"
              @input="activeTabChanged">
        ${self.render_profile_tabs()}
      </b-tabs>

      % if request.has_perm('people_profile.view_versions'):

          ${revisions_grid.render_buefy_table_element(data_prop='revisions',
                                                      show_footer=True,
                                                      vshow='viewingHistory',
                                                      loading='gettingRevisions')|n}

          <b-modal :active.sync="showingRevisionDialog">

            <div class="card">
              <div class="card-content">

                <div style="display: flex; justify-content: space-between;">

                  <div>
                    <b-field horizontal label="Changed">
                      <div v-html="revision.changed"></div>
                    </b-field>
                    <b-field horizontal label="Changed by">
                      <div v-html="revision.changed_by"></div>
                    </b-field>
                    <b-field horizontal label="IP Address">
                      <div v-html="revision.remote_addr"></div>
                    </b-field>
                    <b-field horizontal label="Comment">
                      <div v-html="revision.comment"></div>
                    </b-field>
                    <b-field horizontal label="TXN ID">
                      <div v-html="revision.txnid"></div>
                    </b-field>
                  </div>

                  <div>
                    <div>
                      <b-button @click="viewPrevRevision()"
                                :disabled="!revision.prev_txnid">
                        &laquo; Prev
                      </b-button>
                      <b-button @click="viewNextRevision()"
                                :disabled="!revision.next_txnid">
                        &raquo; Next
                      </b-button>
                    </div>
                    <br />
                    <b-button @click="toggleVersionFields()">
                      {{ revisionShowAllFields ? "Show Diffs Only" : "Show All Fields" }}
                    </b-button>
                  </div>

                </div>

                <br />

                <div v-for="version in revision.versions"
                     :key="version.key">

                  <p class="block has-text-weight-bold">
                    {{ version.model_title }}
                  </p>

                  <table class="diff monospace is-size-7"
                         :class="version.diff_class">
                    <thead>
                      <tr>
                        <th>field name</th>
                        <th>old value</th>
                        <th>new value</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="field in version.fields"
                          :key="field"
                          :class="{diff: version.values[field].after != version.values[field].before}"
                          v-show="revisionShowAllFields || version.values[field].after != version.values[field].before">
                        <td class="field">{{ field }}</td>
                        <td class="old-value">{{ version.values[field].before }}</td>
                        <td class="new-value">{{ version.values[field].after }}</td>
                      </tr>
                    </tbody>
                  </table>

                  <br />
                </div>

              </div>
            </div>
          </b-modal>
      % endif

    </div>
  </script>
</%def>

<%def name="render_this_page_template()">
  ${parent.render_this_page_template()}
  ${self.render_personal_tab_template()}
  ${self.render_employee_tab_template()}
  ${self.render_notes_tab_template()}
  ${self.render_profile_info_template()}
</%def>

<%def name="declare_personal_tab_vars()">
  <script type="text/javascript">

    let PersonalTabData = {

        editNameShowDialog: false,
        personFirstName: null,
        personMiddleName: null,
        personLastName: null,

        editAddressShowDialog: false,
        personStreet1: null,
        personStreet2: null,
        personCity: null,
        personState: null,
        personZipcode: null,
        personInvalidAddress: false,

        editPhoneShowDialog: false,
        phoneUUID: null,
        phoneType: null,
        phoneNumber: null,
        phonePreferred: false,
        savingPhone: false,

        editEmailShowDialog: false,
        emailUUID: null,
        emailType: null,
        emailAddress: null,
        emailPreferred: null,
        emailInvalid: false,
        editEmailSaving: false,
    }

    let PersonalTab = {
        template: '#personal-tab-template',
        mixins: [SubmitMixin],
        props: {
            person: Object,
            member: Object,
            phoneTypeOptions: Array,
            emailTypeOptions: Array,
            maxLengths: Object,
        },
        computed: {
            % if request.has_perm('people_profile.edit_person'):
                editNameSaveDisabled: function() {

                    // first and last name are required
                    if (!this.personFirstName || !this.personLastName) {
                        return true
                    }

                    // otherwise don't disable; let user save
                    return false
                },

                editAddressSaveDisabled: function() {

                    // TODO: should require anything here?

                    // otherwise don't disable; let user save
                    return false
                },

                editPhoneSaveText() {
                    if (this.savingPhone) {
                        return "Working..."
                    }
                    return "Save"
                },

                editPhoneSaveDisabled: function() {
                    if (this.savingPhone) {
                        return true
                    }

                    // phone type is required
                    if (!this.phoneType) {
                        return true
                    }

                    // phone number is required
                    if (!this.phoneNumber) {
                        return true
                    }

                    // otherwise don't disable; let user save
                    return false
                },

                editEmailSaveText() {
                    if (this.editEmailSaving) {
                        return "Working, please wait..."
                    }
                    return "Save"
                },

                editEmailSaveDisabled: function() {

                    // disable if currently submitting form
                    if (this.editEmailSaving) {
                        return true
                    }

                    // email type is required
                    if (!this.emailType) {
                        return true
                    }

                    // email address is required
                    if (!this.emailAddress) {
                        return true
                    }

                    // otherwise don't disable; let user save
                    return false
                },
            % endif
        },
        methods: {

            changeContentTitle(newTitle) {
                this.$emit('change-content-title', newTitle)
            },

            % if request.has_perm('people_profile.edit_person'):

                editNameAllowed() {
                    return true
                },

                editNameInit() {
                    this.personFirstName = this.person.first_name
                    this.personMiddleName = this.person.middle_name
                    this.personLastName = this.person.last_name
                    this.editNameShowDialog = true
                },

                editNameSave() {
                    let url = '${url('people.profile_edit_name', uuid=person.uuid)}'

                    let params = {
                        first_name: this.personFirstName,
                        middle_name: this.personMiddleName,
                        last_name: this.personLastName,
                    }

                    let that = this
                    this.submitData(url, params, function(response) {
                        that.$emit('person-updated', response.data.person)
                        that.editNameShowDialog = false
                        // TODO: not sure this is standard upstream, or just in bespoke?
                        if (response.data.dynamic_content_title) {
                            that.$emit('change-content-title', response.data.dynamic_content_title)
                        }
                    })
                },

                editAddressInit() {
                    let address = this.person.address
                    this.personStreet1 = address ? address.street : null
                    this.personStreet2 = address ? address.street2 : null
                    this.personCity = address ? address.city : null
                    this.personState = address ? address.state : null
                    this.personZipcode = address ? address.zipcode : null
                    this.personInvalidAddress = address ? address.invalid : false
                    this.editAddressShowDialog = true
                },

                editAddressSave() {
                    let url = '${url('people.profile_edit_address', uuid=person.uuid)}'

                    let params = {
                        street: this.personStreet1,
                        street2: this.personStreet2,
                        city: this.personCity,
                        state: this.personState,
                        zipcode: this.personZipcode,
                        invalid: this.personInvalidAddress,
                    }

                    let that = this
                    this.submitData(url, params, function(response) {
                        that.$emit('person-updated', response.data.person)
                        that.editAddressShowDialog = false
                    })
                },

                addPhoneInit() {
                    this.editPhoneInit({
                        uuid: null,
                        type: 'Home',
                        number: null,
                        preferred: false,
                    })
                },

                editPhoneInit(phone) {
                    this.phoneUUID = phone.uuid
                    this.phoneType = phone.type
                    this.phoneNumber = phone.number
                    this.phonePreferred = phone.preferred
                    this.editPhoneShowDialog = true
                    this.$nextTick(function() {
                        this.$refs.editPhoneInput.focus()
                    })
                },

                editPhoneSave() {
                    this.savingPhone = true

                    let url
                    let params = {
                        phone_number: this.phoneNumber,
                        phone_type: this.phoneType,
                        phone_preferred: this.phonePreferred,
                    }

                    if (this.phoneUUID) {
                        url = '${url('people.profile_update_phone', uuid=person.uuid)}'
                        params.phone_uuid = this.phoneUUID
                    } else {
                        url = '${url('people.profile_add_phone', uuid=person.uuid)}'
                    }

                    let that = this
                    this.submitData(url, params, function(response) {
                        that.$emit('person-updated', response.data.person)
                        that.editPhoneShowDialog = false
                        that.savingPhone = false
                    })
                },

                deletePhone(phone) {
                    let url = '${url('people.profile_delete_phone', uuid=person.uuid)}'

                    let params = {
                        phone_uuid: phone.uuid,
                    }

                    let that = this
                    this.submitData(url, params, function(response) {
                        that.$emit('person-updated', response.data.person)
                        that.$buefy.toast.open({
                            message: "Phone number was deleted.",
                            type: 'is-info',
                            duration: 3000, // 3 seconds
                        })
                    })
                },

                setPreferredPhone(phone) {
                    let url = '${url('people.profile_set_preferred_phone', uuid=person.uuid)}'

                    let params = {
                        phone_uuid: phone.uuid,
                    }

                    let that = this
                    this.submitData(url, params, function(response) {
                        that.$emit('person-updated', response.data.person)
                        that.$buefy.toast.open({
                            message: "Phone preference updated!",
                            type: 'is-info',
                            duration: 3000, // 3 seconds
                        })
                    })
                },

                addEmailInit() {
                    this.editEmailInit({
                        uuid: null,
                        type: 'Home',
                        address: null,
                        invalid: false,
                        preferred: false,
                    })
                },

                editEmailInit(email) {
                    this.emailUUID = email.uuid
                    this.emailType = email.type
                    this.emailAddress = email.address
                    this.emailInvalid = email.invalid
                    this.emailPreferred = email.preferred
                    this.editEmailShowDialog = true
                    this.$nextTick(function() {
                        this.$refs.editEmailInput.focus()
                    })
                },

                editEmailSave() {
                    this.editEmailSaving = true

                    let url = null
                    let params = {
                        email_address: this.emailAddress,
                        email_type: this.emailType,
                    }

                    if (this.emailUUID) {
                        url = '${url('people.profile_update_email', uuid=person.uuid)}'
                        params.email_uuid = this.emailUUID
                        params.email_invalid = this.emailInvalid
                    } else {
                        url = '${url('people.profile_add_email', uuid=person.uuid)}'
                        params.email_preferred = this.emailPreferred
                    }

                    let that = this
                    this.submitData(url, params, function(response) {
                        that.$emit('person-updated', response.data.person)
                        that.editEmailShowDialog = false
                        that.editEmailSaving = false
                    }, function(error) {
                        that.editEmailSaving = false
                    })
                },

                deleteEmail(email) {
                    let url = '${url('people.profile_delete_email', uuid=person.uuid)}'

                    let params = {
                        email_uuid: email.uuid,
                    }

                    let that = this
                    this.submitData(url, params, function(response) {
                        that.$emit('person-updated', response.data.person)
                        that.$buefy.toast.open({
                            message: "Email address was deleted.",
                            type: 'is-info',
                            duration: 3000, // 3 seconds
                        })
                    })
                },

                setPreferredEmail(email) {
                    let url = '${url('people.profile_set_preferred_email', uuid=person.uuid)}'

                    let params = {
                        email_uuid: email.uuid,
                    }

                    let that = this
                    this.submitData(url, params, function(response) {
                        that.$emit('person-updated', response.data.person)
                        that.$buefy.toast.open({
                            message: "Email preference updated!",
                            type: 'is-info',
                            duration: 3000, // 3 seconds
                        })
                    })
                },

            % endif
        },
    }

  </script>
</%def>

<%def name="make_personal_tab_component()">
  ${self.declare_personal_tab_vars()}
  <script type="text/javascript">

    PersonalTab.data = function() { return PersonalTabData }
    Vue.component('personal-tab', PersonalTab)

  </script>
</%def>

<%def name="declare_employee_tab_vars()">
  <script type="text/javascript">

    let EmployeeTabData = {

        startEmployeeShowDialog: false,
        employeeID: null,
        employeeStartDate: null,
        showStopEmployeeDialog: false,
        employeeEndDate: null,
        employeeRevokeAccess: false,
        showEditEmployeeHistoryDialog: false,
        employeeHistoryUUID: null,
        employeeHistoryStartDate: null,
        employeeHistoryEndDate: null,
        employeeHistoryEndDateRequired: false,

        % if request.has_perm('employees.edit'):
        showEditEmployeeIDDialog: false,
        newEmployeeID: null,
        updatingEmployeeID: false,
        % endif
    }

    let EmployeeTab = {
        template: '#employee-tab-template',
        mixins: [SubmitMixin],
        props: {
            employee: Object,
            employeeHistory: Array,
        },

        computed: {

            % if request.has_perm('employees.edit'):

                editEmployeeIDSaveButtonText() {
                    if (this.updatingEmployeeID) {
                        return "Working, please wait..."
                    }
                    return "Save"
                },

            % endif
        },

        methods: {

            changeContentTitle(newTitle) {
                this.$emit('change-content-title', newTitle)
            },

            % if request.has_perm('employees.edit'):

                initEditEmployeeID() {
                    this.newEmployeeID = this.employee.id
                    this.updatingEmployeeID = false
                    this.showEditEmployeeIDDialog = true
                },

                updateEmployeeID() {
                    this.updatingEmployeeID = true

                    let url = '${url('people.profile_update_employee_id', uuid=instance.uuid)}'

                    let params = {
                        'employee_id': this.newEmployeeID,
                    }

                    let that = this
                    this.submitData(url, params, function(response) {
                        that.$emit('employee-updated', response.data.employee)
                        that.showEditEmployeeIDDialog = false
                        that.updatingEmployeeID = false
                    })
                },

            % endif

            % if request.has_perm('people_profile.toggle_employee'):

                startEmployeeInit() {
                    this.employeeID = this.employee.id || null
                    this.startEmployeeShowDialog = true
                },

                startEmployee() {
                    let url = '${url('people.profile_start_employee', uuid=person.uuid)}'

                    let params = {
                        id: this.employeeID,
                        start_date: this.employeeStartDate,
                    }

                    let that = this
                    this.submitData(url, params, function(response) {
                        that.startEmployeeSuccess(response.data)
                    })
                },

                startEmployeeSuccess(data) {
                    this.$emit('employee-updated', data.employee)
                    this.$emit('employee-history-updated', data.employee_history_data)
                    this.$emit('change-content-title', data.dynamic_content_title)

                    // let derived component do more here if needed
                    this.startEmployeeSuccessExtra(data)

                    this.startEmployeeShowDialog = false
                },

                startEmployeeSuccessExtra(data) {},

                endEmployee() {
                    let url = '${url('people.profile_end_employee', uuid=person.uuid)}'

                    let params = {
                        end_date: this.employeeEndDate,
                        revoke_access: this.employeeRevokeAccess,
                    }

                    let that = this
                    this.submitData(url, params, function(response) {
                        that.endEmployeeSuccess(response.data)
                    })
                },

                endEmployeeSuccess(data) {
                    this.$emit('employee-updated', data.employee)
                    this.$emit('employee-history-updated', data.employee_history_data)
                    this.$emit('change-content-title', data.dynamic_content_title)

                    // let derived component do more here if needed
                    this.startEmployeeSuccessExtra(data)

                    this.showStopEmployeeDialog = false
                },

                endEmployeeSuccessExtra(data) {},

            % endif

            % if request.has_perm('people_profile.edit_employee_history'):

                editEmployeeHistory(row) {
                    this.employeeHistoryUUID = row.uuid
                    this.employeeHistoryStartDate = row.start_date
                    this.employeeHistoryEndDate = row.end_date
                    this.employeeHistoryEndDateRequired = !!row.end_date
                    this.showEditEmployeeHistoryDialog = true
                },

                saveEmployeeHistory() {
                    let url = '${url('people.profile_edit_employee_history', uuid=person.uuid)}'

                    let params = {
                        uuid: this.employeeHistoryUUID,
                        start_date: this.employeeHistoryStartDate,
                        end_date: this.employeeHistoryEndDate,
                    }

                    let that = this
                    this.submitData(url, params, function(response) {
                        that.$emit('employee-updated', response.data.employee)
                        that.$emit('employee-history-updated', response.data.employee_history_data)
                        that.showEditEmployeeHistoryDialog = false
                    })
                },

            % endif
        },
    }

  </script>
</%def>

<%def name="make_employee_tab_component()">
  ${self.declare_employee_tab_vars()}
  <script type="text/javascript">

    EmployeeTab.data = function() { return EmployeeTabData }
    Vue.component('employee-tab', EmployeeTab)

  </script>
</%def>

<%def name="declare_notes_tab_vars()">
  <script type="text/javascript">

    let NotesTabData = {
        noteShowDialog: false,
        noteUUID: null,
        noteType: null,
        noteSubject: null,
        noteText: null,
        noteDeleting: false,
        noteSaving: false,
    }

    let NotesTab = {
        template: '#notes-tab-template',
        mixins: [SimpleRequestMixin],
        props: {
            notes: Array,
            noteTypeOptions: Array,
        },

        computed: {

            noteDialogTitle() {
                if (this.noteUUID) {
                    if (this.noteDeleting) {
                        return "Delete Note"
                    }
                    return "Edit Note"
                }
                return "New Note"
            },

            noteSaveText() {
                if (this.noteDeleting) {
                    return "Delete Note"
                }
                return "Save Note"
            },

        },

        methods: {

            % if request.has_perm('people_profile.add_note'):

                noteNew() {
                    this.noteUUID = null
                    this.noteType = null
                    this.noteSubject = null
                    this.noteText = null
                    this.noteDeleting = false
                    this.noteShowDialog = true
                },

            % endif

            % if request.has_perm('people_profile.edit_note'):

                noteEdit(note) {
                    this.noteUUID = note.uuid
                    this.noteType = note.note_type
                    this.noteSubject = note.subject
                    this.noteText = note.text
                    this.noteDeleting = false
                    this.noteShowDialog = true
                },

            % endif

            % if request.has_perm('people_profile.delete_note'):

                noteDelete(note) {
                    this.noteUUID = note.uuid
                    this.noteType = note.note_type
                    this.noteSubject = note.subject
                    this.noteText = note.text
                    this.noteDeleting = true
                    this.noteShowDialog = true
                },

            % endif

            % if request.has_any_perm('people_profile.add_note', 'people_profile.edit_note', 'people_profile.delete_note'):

                noteSave() {
                    this.noteSaving = true

                    let url = null
                    if (!this.noteUUID) {
                        url = '${master.get_action_url('profile_add_note', instance)}'
                    } else if (this.noteDeleting) {
                        url = '${master.get_action_url('profile_delete_note', instance)}'
                    } else {
                        url = '${master.get_action_url('profile_edit_note', instance)}'
                    }

                    let params = {
                        uuid: this.noteUUID,
                        note_type: this.noteType,
                        note_subject: this.noteSubject,
                        note_text: this.noteText,
                    }

                    this.simplePOST(url, params, response => {
                        this.$emit('new-notes-data', response.data.notes)
                        this.noteSaving = false
                        this.noteShowDialog = false
                    }, response => {
                        this.notesSaving = false
                    })
                },

            % endif
        },
    }

  </script>
</%def>

<%def name="make_notes_tab_component()">
  ${self.declare_notes_tab_vars()}
  <script type="text/javascript">

    NotesTab.data = function() { return NotesTabData }
    Vue.component('notes-tab', NotesTab)

  </script>
</%def>

<%def name="declare_profile_info_vars()">
  <script type="text/javascript">

    let ProfileInfoData = {
        activeTab: location.hash ? location.hash.substring(1) : undefined,
        person: ${json.dumps(person_data)|n},
        customers: ${json.dumps(customers_data)|n},
        % if expose_customer_shoppers:
        shoppers: ${json.dumps(shoppers_data)|n},
        % endif
        member: null,           // TODO
        members: ${json.dumps(members_data)|n},
        employee: ${json.dumps(employee_data)|n},
        employeeHistory: ${json.dumps(employee_history_data)|n},
        notes: ${json.dumps(notes_data)|n},
        noteTypeOptions: ${json.dumps(note_type_options)|n},
        users: ${json.dumps(users_data)|n},
        phoneTypeOptions: ${json.dumps(phone_type_options)|n},
        emailTypeOptions: ${json.dumps(email_type_options)|n},
        maxLengths: ${json.dumps(max_lengths)|n},

        % if request.has_perm('people_profile.view_versions'):
        loadingRevisions: false,
        showingRevisionDialog: false,
        revision: {},
        revisionShowAllFields: false,
        % endif
    }

    let ProfileInfo = {
        template: '#profile-info-template',
        mixins: [FormPosterMixin],

        % if request.has_perm('people_profile.view_versions'):
        props: {
            viewingHistory: Boolean,
            gettingRevisions: Boolean,
            revisions: Array,
            revisionVersionMap: null,
        },
        % endif

        computed: {},
        methods: {

            newNotesData(notes) {
                this.notes = notes
            },

            personUpdated(person) {
                this.person = person
            },

            employeeUpdated(employee) {
                this.employee = employee
            },

            employeeHistoryUpdated(employeeHistory) {
                this.employeeHistory = employeeHistory
            },

            changeContentTitle(newTitle) {
                this.$emit('change-content-title', newTitle)
            },

            activeTabChanged(value) {
                location.hash = value
                this.activeTabChangedExtra(value)
            },

            activeTabChangedExtra(value) {},

            % if request.has_perm('people_profile.view_versions'):

                viewRevision(row) {
                    this.revision = this.revisionVersionMap[row.txnid]
                    this.showingRevisionDialog = true
                },

                viewPrevRevision() {
                    let txnid = this.revision.prev_txnid
                    this.revision = this.revisionVersionMap[txnid]
                },

                viewNextRevision() {
                    let txnid = this.revision.next_txnid
                    this.revision = this.revisionVersionMap[txnid]
                },

                toggleVersionFields() {
                    this.revisionShowAllFields = !this.revisionShowAllFields
                },

            % endif
        },
    }

  </script>
</%def>

<%def name="make_profile_info_component()">
  ${self.declare_profile_info_vars()}
  <script type="text/javascript">

    ProfileInfo.data = function() { return ProfileInfoData }

    Vue.component('profile-info', ProfileInfo)

  </script>
</%def>

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  <script type="text/javascript">

    % if request.has_perm('people_profile.view_versions'):
    ThisPage.props.viewingHistory = Boolean
    ThisPage.props.gettingRevisions = Boolean
    ThisPage.props.revisions = Array
    ThisPage.props.revisionVersionMap = null
    % endif

    ThisPage.methods.changeContentTitle = function(newTitle) {
        this.$emit('change-content-title', newTitle)
    }

    var SubmitMixin = {
        data() {
            return {
                csrftoken: ${json.dumps(request.session.get_csrf_token() or request.session.new_csrf_token())|n},
            }
        },

        methods: {
            submitData(url, params, success, failure) {
                let headers = {
                    'X-CSRF-TOKEN': this.csrftoken,
                }
                this.$http.post(url, params, {headers: headers}).then((response) => {
                    if (response.data.success) {
                        if (success) {
                            success(response)
                        }
                    } else {
                        this.$buefy.toast.open({
                            message: "Save failed:  " + (response.data.error || "(unknown error)"),
                            type: 'is-danger',
                            duration: 4000, // 4 seconds
                        })
                        if (failure) {
                            failure()
                        }
                    }
                }).catch((error) => {
                    this.$buefy.toast.open({
                        message: "Save failed:  (unknown error)",
                        type: 'is-danger',
                        duration: 4000, // 4 seconds
                    })
                    if (failure) {
                        failure()
                    }
                })
            },
        },
    }

  </script>
</%def>

<%def name="make_this_page_component()">
  ${parent.make_this_page_component()}
  ${self.make_personal_tab_component()}
  ${self.make_employee_tab_component()}
  ${self.make_notes_tab_component()}
  ${self.make_profile_info_component()}
</%def>

<%def name="modify_whole_page_vars()">
  ${parent.modify_whole_page_vars()}

  % if request.has_perm('people_profile.view_versions'):
      <script type="text/javascript">

        WholePageData.viewingHistory = false
        WholePageData.gettingRevisions = false
        WholePageData.gotRevisions = false
        WholePageData.revisions = []
        WholePageData.revisionVersionMap = null

        WholePage.methods.viewHistory = function() {
            this.viewingHistory = true

            if (!this.gotRevisions && !this.gettingRevisions) {
                this.getRevisions()
            }
        }

        WholePage.methods.refreshHistory = function() {
            if (!this.gettingRevisions) {
                this.getRevisions()
            }
        }

        WholePage.methods.getRevisions = function() {
            this.gettingRevisions = true

            let url = '${url('people.view_profile_revisions', uuid=person.uuid)}'
            this.simpleGET(url, {}, response => {
                this.revisions = response.data.data
                this.revisionVersionMap = response.data.vmap
                this.gotRevisions = true
                this.gettingRevisions = false
            }, response => {
                this.gettingRevisions = false
            })
        }

      </script>
  % endif
</%def>


${parent.body()}
