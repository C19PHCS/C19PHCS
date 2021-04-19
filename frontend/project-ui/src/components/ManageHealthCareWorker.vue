<template>
  <q-card style="min-width: 600px" class="no-border">
    <q-card-section class="flex text-white bg-primary">
      <div class="text-h6">
        Manage Health Care Worker
      </div>
      <q-space />
      <q-btn flat size="sm" v-close-popup round icon="close" />
    </q-card-section>
    <q-card-section>
      <div class="person-card-flex q-gutter-sm">
        <q-input
          style="margin-bottom: 20px"
          v-model="localHealthCareWorker.medicareNumber"
          dense
          outlined
          required
          label="Medicare Number *"
        />
        <q-input
          style="margin-bottom: 20px"
          v-model="localHealthCareWorker.firstName"
          dense
          outlined
          label="First Name *"
        />
        <q-input
          style="margin-bottom: 20px"
          v-model="localHealthCareWorker.lastName"
          dense
          outlined
          label="Last Name *"
        />
        <q-input
          style="margin-bottom: 20px"
          v-model="localHealthCareWorker.phoneNumber"
          dense
          outlined
          label="Phone Number *"
        />
        <q-input
          style="margin-bottom: 20px"
          v-model="localHealthCareWorker.email"
          dense
          outlined
          label="Email *"
        />
        <q-input
          style="margin-bottom: 20px"
          v-model="localHealthCareWorker.province"
          dense
          outlined
          label="Province *"
        />
        <q-input
          style="margin-bottom: 20px"
          v-model="localHealthCareWorker.city"
          dense
          outlined
          label="City *"
        />
        <q-input
          class="address-input"
          style="margin-bottom: 20px"
          v-model="localHealthCareWorker.address"
          dense
          outlined
          label="Address *"
        />
        <q-input
          style="margin-bottom: 20px"
          v-model="localHealthCareWorker.workerId"
          dense
          outlined
          label="Worker Id *"
        />
        <q-input
          style="margin-bottom: 20px"
          v-model="localHealthCareWorker.publicHealthCareCenterId"
          dense
          outlined
          label="Center Id *"
        />
      </div>
    </q-card-section>
    <q-form @submit="confirmSaveHealthCareWorker">
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
import { PublicHealthWorker } from './models';

export default Vue.extend({
  name: 'ManageHealthCareWorker',
  mounted() {
    this.componentReady = true;
    this.localHealthCareWorker = JSON.parse(JSON.stringify(this.localHealthCareWorker)) as PublicHealthWorker;
  },
  data() {
    return {
      localHealthCareWorker: {} as PublicHealthWorker,
      componentReady: false
    };
  },
  props: {
    worker: {
      type: Object as () => PublicHealthWorker
    },
    readOnly: {
      type: Boolean
    }
  },
  methods: {
    confirmSaveHealthCareWorker() {
      console.log(this.worker);
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
