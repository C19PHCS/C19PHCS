<template>
  <q-card style="min-width: 600px" class="no-border">
    <q-card-section class="flex text-white bg-primary">
      <div class="text-h6">
        Manage Person
      </div>
      <q-space />
      <q-btn flat size="sm" v-close-popup round icon="close" />
    </q-card-section>
    <q-card-section>
      <div class="person-card-flex q-gutter-sm">
        <q-input
          style="margin-bottom: 20px"
          v-model="localPerson.medicareNumber"
          dense
          outlined
          required
          label="Medicare Number *"
        />
        <q-input
          style="margin-bottom: 20px"
          v-model="localPerson.firstName"
          dense
          outlined
          label="First Name *"
        />
        <q-input
          style="margin-bottom: 20px"
          v-model="localPerson.lastName"
          dense
          outlined
          label="Last Name *"
        />
        <q-input
          style="margin-bottom: 20px"
          v-model="localPerson.dateOfBirth"
          dense
          type="date"
          outlined
          required
          label="Date of birth *"
        />
        <q-input
          style="margin-bottom: 20px"
          v-model="localPerson.phoneNumber"
          dense
          outlined
          label="Phone Number *"
        />
        <q-input
          style="margin-bottom: 20px"
          v-model="localPerson.email"
          dense
          outlined
          label="Email *"
        />
        <q-input
          style="margin-bottom: 20px"
          v-model="localPerson.province"
          dense
          outlined
          label="Province *"
        />
        <q-input
          style="margin-bottom: 20px"
          v-model="localPerson.city"
          dense
          outlined
          label="City *"
        />
        <q-input
          style="margin-bottom: 20px"
          v-model="localPerson.postalCode"
          dense
          outlined
          label="Postal code *"
        />
        <q-input
          style="margin-bottom: 20px"
          v-model="localPerson.country"
          dense
          outlined
          label="Country *"
        />
        <q-input
          class="address-input"
          style="margin-bottom: 20px"
          v-model="localPerson.address"
          dense
          outlined
          label="Address *"
        />
        <q-input
          style="margin-bottom: 20px"
          v-model="localPerson.citizenShip"
          dense
          outlined
          label="Citizenship *"
        />
        <q-input
          style="margin-bottom: 20px"
          v-model="localPerson.motherMedicare"
          dense
          outlined
          label="Mother medicare number *"
        />
        <q-input
          style="margin-bottom: 20px"
          v-model="localPerson.fatherMedicare"
          dense
          outlined
          label="Father medicare number *"
        />
      </div>
    </q-card-section>
    <q-form @submit="confirmSavePerson">
      <div style="min-height: 50px;">
        <q-card-actions align="right">
          <q-btn flat color="primary" label="Cancel" v-close-popup />
          <q-btn label="Save" color="primary" type="submit" />
        </q-card-actions>
      </div>
    </q-form>
  </q-card>
</template>

<script lang="ts">
import Vue from 'vue';
import { Person } from './models';

export default Vue.extend({
  name: 'ManagePerson',
  mounted() {
    this.componentReady = true;
    this.localPerson = JSON.parse(JSON.stringify(this.person)) as Person;
  },
  data() {
    return {
      localPerson: {} as Person,
      componentReady: false
    };
  },
  props: {
    person: {
      type: Object as () => Person
    },
    readOnly: {
      type: Boolean
    }
  },
  methods: {
    confirmSavePerson() {
      this.$emit('save', this.localPerson)
    }
  },
  components: {}
});
</script>

<style lang="scss" scoped>
.person-card-flex {
  display: flex;
  flex-wrap: wrap;

  .q-select,
  .q-input,
  .q-toggle,
  div {
    width: 31%;
  }

  .address-input {
    width: 63%
  }
}

.note-label {
  margin-top: 20px;
  color: rgba(0, 0, 0, 0.6);
  font-size: 14px;
}
</style>
