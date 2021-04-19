<template>
  <q-card style="min-width: 1000px" class="no-border">
    <q-card-section class="flex text-white bg-primary">
      <div class="text-h6">All Workers At {{ publicHealthCenter.name }}</div>
      <q-space />
      <q-btn flat size="sm" v-close-popup round icon="close" />
    </q-card-section>
    <q-card-section>
      <div class="person-card-flex q-gutter-sm">
        <q-table
          style="min-width: 950px"
          dense
          flat
          bordered
          :columns="columns"
          :data="workers"
          row-key="id"
          :pagination="{ rowsPerPage: 10, sortBy: 'Date From' }"
        >
          <template v-slot:top>
            <table-header title="Workers" :hide-add-button="true">
            </table-header>
          </template>
        </q-table>
      </div>
    </q-card-section>
  </q-card>
</template>

<script lang="ts">
import Vue from 'vue';
import { HealthCareCenter, PublicHealthWorker } from './models';
import TableHeader from 'src/components/TableHeader.vue';

export default Vue.extend({
  name: 'ManagePerson',
  async mounted() {
    this.localHospital = JSON.parse(
      JSON.stringify(this.publicHealthCenter)
    ) as HealthCareCenter;
    this.componentReady = true;
    const id = this.publicHealthCenter.id;
    await this.$axios
      .get(`/workers_at_facility/${id}`)
      .then(Response => (this.workers = Response.data as PublicHealthWorker[]));
  },
  data() {
    return {
      workers: [] as PublicHealthWorker[],
      componentReady: false,
      localHospital: {} as HealthCareCenter,
      columns: [
        {
          name: 'Medicare Number',
          required: true,
          label: 'Medicare Number',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: PublicHealthWorker) => row.medicareNumber,
          sortable: true
        },
        {
          name: 'First Name',
          required: true,
          label: 'First Name',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: PublicHealthWorker) => row.firstName,
          sortable: true
        },
        {
          name: 'Last Name',
          required: true,
          label: 'Last Name',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: PublicHealthWorker) => row.lastName,
          sortable: true
        },
        {
          name: 'Date of birth',
          required: true,
          label: 'Date of birth',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: PublicHealthWorker) => row.dateOfBirth,
          sortable: true
        },
        {
          name: 'Phone number',
          required: true,
          label: 'Phone number',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: PublicHealthWorker) => row.phoneNumber,
          sortable: true
        },
        {
          name: 'Email address',
          required: true,
          label: 'Email address',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: PublicHealthWorker) => row.email,
          sortable: true
        },
        {
          name: 'Health Worker Id',
          required: true,
          label: 'Health Worker Id',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: PublicHealthWorker) => row.workerId,
          sortable: true
        },
        {
          name: 'Health Center Id',
          required: true,
          label: 'Health Center Id',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: PublicHealthWorker) => row.publicHealthCareCenterId,
          sortable: true
        }
      ]
    };
  },
  props: {
    publicHealthCenter: {
      type: Object as () => HealthCareCenter
    },
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
