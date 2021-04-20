<template>
  <q-card style="min-width: 600px" class="no-border">
    <q-card-section class="flex text-white bg-primary">
      <div class="text-h6">
        Manage Health Care Center
      </div>
      <q-space />
      <q-btn flat size="sm" v-close-popup round icon="close" />
    </q-card-section>
    <q-card-section>
      <div class="person-card-flex q-gutter-sm">
        <q-input
          style="margin-bottom: 20px"
          v-model="localHospital.name"
          dense
          outlined
          required
          label="Name *"
        />
        <q-input
          style="margin-bottom: 20px"
          class="address-input"
          v-model="localHospital.address"
          dense
          outlined
          label="Address *"
        />
        <q-input
          style="margin-bottom: 20px"
          v-model="localHospital.webAddress"
          dense
          outlined
          label="Web Address *"
        />
        <q-input
          style="margin-bottom: 20px"
          v-model="localHospital.type"
          dense
          outlined
          label="Type *"
        />
        <q-input
          style="margin-bottom: 20px"
          v-model="localHospital.phoneNumber"
          dense
          outlined
          label="Phone number *"
        />
        <q-input
          style="margin-bottom: 20px"
          v-model="localHospital.country"
          dense
          outlined
          label="Country *"
        />
        <q-input
          style="margin-bottom: 20px"
          v-model="localHospital.province"
          dense
          outlined
          label="Province *"
        />
        <q-input
          style="margin-bottom: 20px"
          v-model="localHospital.city"
          dense
          outlined
          label="City *"
        />
        <q-input
          style="margin-bottom: 20px"
          v-model="localHospital.postalCode"
          dense
          outlined
          label="Postal Code *"
        />
        <q-input
          style="margin-bottom: 20px"
          v-model="localHospital.testingType"
          dense
          outlined
          label="Testing type *"
        />
        <q-input
          style="margin-bottom: 20px"
          v-model="localHospital.driveThru"
          dense
          outlined
          label="Drive Thru *"
        />
      </div>
    </q-card-section>
    <q-form @submit="confirmSaveHospital">
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
import { HealthCareCenter } from './models';

export default Vue.extend({
  name: 'ManagePerson',
  mounted() {
    this.componentReady = true;
    this.localHospital = JSON.parse(JSON.stringify(this.hospital)) as HealthCareCenter;
  },
  data() {
    return {
      localHospital: {} as HealthCareCenter,
      componentReady: false
    };
  },
  props: {
    hospital: {
      type: Object as () => HealthCareCenter
    },
    readOnly: {
      type: Boolean
    }
  },
  methods: {
    confirmSaveHospital() {
      this.$emit('save', this.localHospital)
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
