<template>
  <q-card style="min-width: 600px" class="no-border">
    <q-card-section class="flex text-white bg-primary">
      <div class="text-h6">
        Manage Alert for {{ region.name }}
      </div>
      <q-space />
      <q-btn flat size="sm" v-close-popup round icon="close" />
    </q-card-section>
    <q-card-section>
      <div class="person-card-flex q-gutter-sm">
        <q-input
          style="margin-bottom: 20px"
          v-model="localRegion.name"
          :readonly="true"
          dense
          outlined
          label="Region Name"
        />
        <q-input
          style="margin-bottom: 20px"
          v-model="localAlert.alertLevel"
          type="number"
          dense
          outlined
          label="Level *"
        />
      </div>
    </q-card-section>
    <q-form @submit="confirmSaveAlert">
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
import { Alert, Region } from './models';

export default Vue.extend({
  name: 'ManagePerson',
  mounted() {
    this.localRegion = JSON.parse(JSON.stringify(this.region)) as Region;
    this.localAlert.regionName = this.localRegion.name
    this.componentReady = true;
  },
  data() {
    return {
      localRegion: {} as Region,
      localAlert: {} as Alert,
      componentReady: false
    };
  },
  props: {
    region: {
      type: Object as () => Region
    },
    readOnly: {
      type: Boolean
    }
  },
  methods: {
    async confirmSaveAlert() {
      const data = {
        alertLevel: +this.localAlert.alertLevel,
        regionName: this.localAlert.regionName
      }
      await this.$axios
          .post('/set-region-alert/', data)
          .then(Response => (console.log(Response.data)));
      this.$emit('save', this.localAlert)
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
