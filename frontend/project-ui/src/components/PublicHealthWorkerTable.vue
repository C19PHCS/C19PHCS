<template>
  <div v-if="componentReady">
    <q-table
      dense
      flat
      bordered
      :columns="columns"
      :data="workers"
      row-key="id"
      :pagination="{ rowsPerPage: 10, sortBy: 'Date From' }"
      :loading="loading"
    >
      <template v-slot:top>
        <table-header
          title="Public Health Worker"
          @create="createWorker"
          create-tooltip="create new health care worker"
          :hide-add-button="readOnly"
        >
        </table-header>
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
                  @click="editPublicHealthWorker(props.row)"
                  icon="edit"
                  ><q-tooltip>Edit Public Health Worker</q-tooltip></q-btn
                >
                <q-btn
                  v-if="!readOnly"
                  flat
                  color="negative"
                  dense
                  @click="deletePublicHealthWorker(props.row)"
                  icon="delete"
                  ><q-tooltip>Delete Public Health Worker</q-tooltip></q-btn
                >
              </q-td>
            </q-tr>
          </template>
    </q-table>
    <q-dialog v-model="isManagingWorker">
      <manage-public-health-worker :person="localWorker"/>
    </q-dialog> 
  </div>
</template>

<script lang="ts">
import ManagePublicHealthWorker from './ManagePerson.vue';
import { PublicHealthWorker } from 'src/components/models';
import TableHeader from 'src/components/TableHeader.vue'
import Vue from 'vue';


export default Vue.extend({
  name: 'PersonTable',
  props: {
    readOnly: {
      type: Boolean
    }
    
  },
  mounted() {
    this.componentReady = true
    this.workers = []
    this.loading = false
  },
  data() {
    return {
      componentReady: false,
      workers: [] as PublicHealthWorker[],
      localWorker: {} as PublicHealthWorker,
      isManagingWorker: false,
      loading: true,
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
  methods: {
    createWorker(){
      this.isManagingWorker = true
      const person = 'person'
      console.log(person)
    },
    editPublicHealthWorker(worker : PublicHealthWorker){
      console.log(worker)
      this.localWorker = worker
      this.isManagingWorker = true
    },
    deletePublicHealthWorker(worker: PublicHealthWorker){
      console.log(worker)
      this.localWorker = worker
    }
    
  },
  components: {
    TableHeader,
    ManagePublicHealthWorker
  }
});
</script>

    ManagePerson