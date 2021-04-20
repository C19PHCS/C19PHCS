<template>
  <q-card style="min-width: 400px" class="no-border">
    <q-card-section class="flex text-white bg-primary">
      <div class="text-h6">Alerts</div>
      <q-space />
      <q-btn flat size="sm" v-close-popup round icon="close" />
    </q-card-section>
    <q-card-section>
      <div class="person-card-flex q-gutter-sm">
        <q-table
          style="min-width: 800px"
          dense
          flat
          bordered
          :columns="columns"
          :data="alerts"
          row-key="id"
          :pagination="{ rowsPerPage: 10, sortBy: 'Date From' }"
        >
          <template v-slot:top>
            <table-header title="All Alerts" :hide-add-button="true">
            </table-header>
          </template>
        </q-table>
      </div>
    </q-card-section>
  </q-card>
</template>

<script lang="ts">
import Vue from 'vue';
import { AlertTable } from './models';
import TableHeader from 'src/components/TableHeader.vue';

export default Vue.extend({
  name: 'ManagePerson',
  async mounted() {
    await this.$axios
      .get('general/alert/get_all/')
      .then(Response => (this.alerts = Response.data as AlertTable[]));
  },
  data() {
    return {
      alerts: [] as AlertTable[],
      componentReady: false,
      columns: [
        {
          name: 'Region Name',
          required: true,
          label: 'Region Name',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: AlertTable) => row.regionName,
          sortable: true
        },
        {
          name: 'Alert Level',
          required: true,
          label: 'Alert Level',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: AlertTable) => row.alertLevelId,
          sortable: true
        },
        {
          name: 'Date',
          required: true,
          label: 'Date',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: AlertTable) => row.date,
          sortable: true
        }
      ]
    };
  },
  props: {
    readOnly: {
      type: Boolean
    }
  },
  methods: {},
  components: { TableHeader }
});
</script>

<style lang="scss" scoped>
.person-card-flex {
  display: flex;
  flex-wrap: wrap;
  min-width: 800px;

  .q-select,
  .q-input,
  .q-toggle,
  div {
    width: 31%;
  }

  .address-input {
    width: 63%;
  }
}

.note-label {
  margin-top: 20px;
  color: rgba(0, 0, 0, 0.6);
  font-size: 14px;
}
</style>
