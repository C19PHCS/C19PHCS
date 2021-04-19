<template>
  <div v-if="componentReady">
    <q-table
      dense
      flat
      bordered
      :columns="columns"
      :data="hospitals"
      row-key="id"
      :pagination="{ rowsPerPage: 10, sortBy: 'Date From' }"
      :loading="loading"
    >
      <template v-slot:top>
        <table-header
          title="Health Care Centers"
          @create="createHospital"
          create-tooltip="create new center"
          :hide-add-button="readOnly"
        >
        </table-header>
      </template>
      <template v-slot:header="props">
        <q-tr :props="props">
          <q-th v-for="col in props.cols" :key="col.name" :props="props">
            {{ col.label }}
          </q-th>
          <q-th>Actions</q-th>
        </q-tr>
      </template>
      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td v-for="col in props.cols" :key="col.name" :props="props">
            <div>
              {{ col.value }}
            </div>
          </q-td>
          <q-td class="table-action-buttons">
            <q-btn
              flat
              color="primary"
              dense
              @click="viewWorkers(props.row)"
              icon="person"
              ><q-tooltip>Edit Center</q-tooltip></q-btn
            >
            <q-btn
              flat
              color="primary"
              dense
              @click="editHospital(props.row)"
              icon="edit"
              ><q-tooltip>Edit Center</q-tooltip></q-btn
            >
            <q-btn
              v-if="!readOnly"
              flat
              color="negative"
              dense
              @click="deleteHospital(props.row)"
              icon="delete"
              ><q-tooltip>Delete Center</q-tooltip></q-btn
            >
          </q-td>
        </q-tr>
      </template>
    </q-table>
    <q-dialog v-model="isManagingHospital">
      <manage-hospital @save="saveHospital" :hospital="localHospital" />
    </q-dialog>
    <q-dialog v-model="isViewingWorkers">
      <view-workers :public-health-center="localHospital" />
    </q-dialog>
  </div>
</template>

<script lang="ts">
import ManageHospital from './ManageHospital.vue';
import { HealthCareCenter } from 'src/components/models';
import TableHeader from 'src/components/TableHeader.vue';
import Vue from 'vue';
import ViewWorkers from './ViewWorkers.vue';

export default Vue.extend({
  name: 'PersonTable',
  props: {
    readOnly: {
      type: Boolean
    }
  },
  async mounted() {
    await this.$axios
      .get('/facilities/')
      .then(Response => (this.hospitals = Response.data as HealthCareCenter[]));
    this.loading = false;
    this.componentReady = true;
  },
  data() {
    return {
      componentReady: false,
      hospitals: [] as HealthCareCenter[],
      localHospital: {} as HealthCareCenter,
      isViewingWorkers: false,
      isManagingHospital: false,
      loading: true,
      columns: [
        {
          name: 'Name',
          required: true,
          label: 'Name',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: HealthCareCenter) => row.name,
          sortable: true
        },
        {
          name: 'Address',
          required: true,
          label: 'Address',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: HealthCareCenter) => row.address,
          sortable: true
        },
        {
          name: 'Web Address',
          required: true,
          label: 'Web Address',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: HealthCareCenter) => row.webAddress,
          sortable: true
        },
        {
          name: 'Phone Number',
          required: true,
          label: 'Phone Number',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: HealthCareCenter) => row.phoneNumber,
          sortable: true
        },
        {
          name: 'Type',
          required: true,
          label: 'Type',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: HealthCareCenter) => row.type,
          sortable: true
        },
        {
          name: 'City',
          required: true,
          label: 'City',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: HealthCareCenter) => row.city,
          sortable: true
        },
        {
          name: 'Province',
          required: true,
          label: 'Province',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: HealthCareCenter) => row.province,
          sortable: true
        },
        {
          name: 'Country',
          required: true,
          label: 'Country',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: HealthCareCenter) => row.country,
          sortable: true
        },
        {
          name: 'DriveThru',
          required: true,
          label: 'DriveThru',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: HealthCareCenter) => row.driveThru,
          sortable: true
        }
      ]
    };
  },
  methods: {
    saveHospital(hospital: HealthCareCenter) {
      console.log(hospital);
      this.isManagingHospital = false;
    },
    viewWorkers(row: HealthCareCenter) {
      this.localHospital = row
      this.isViewingWorkers = true
    },
    createHospital() {
      this.localHospital = {
        id: -1,
        name: null,
        address: null,
        webAddress: null,
        phoneNumber: null,
        type: null,
        city: null,
        province: null,
        country: null,
        driveThru: null
      }
      this.isManagingHospital = true
    },
    editHospital(row: HealthCareCenter) {
      this.localHospital = row;
      this.isManagingHospital = true;
    },
    deleteHospital(row: HealthCareCenter) {
      this.localHospital = row;
      console.log(row);
    }
  },
  components: {
    TableHeader,
    ManageHospital,
    ViewWorkers
  }
});
</script>

ManagePerson
