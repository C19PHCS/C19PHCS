<template>
  <div v-if="componentReady">
    <q-table
      dense
      flat
      bordered
      :columns="columns"
      :data="regions"
      row-key="id"
      :pagination="{ rowsPerPage: 10, sortBy: 'Date From' }"
      :loading="loading"
    >
      <template v-slot:top>
        <table-header
          title="Regions"
          @create="isManagingRegion = true"
          create-tooltip="create new region"
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
              v-if="!readOnly"
              flat
              color="negative"
              dense
              @click="setAlertForRegion(props.row)"
              icon="add_alert"
              ><q-tooltip>Set Alert</q-tooltip></q-btn
            >
            <q-btn
              flat
              color="primary"
              dense
              @click="editRegion(props.row)"
              icon="edit"
              ><q-tooltip>Edit Region</q-tooltip></q-btn
            >
            <q-btn
              v-if="!readOnly"
              flat
              color="negative"
              dense
              @click="deleteRegion(props.row)"
              icon="delete"
              ><q-tooltip>Delete Region</q-tooltip></q-btn
            >
          </q-td>
        </q-tr>
      </template>
    </q-table>
    <q-dialog v-model="isManagingRegion">
      <manage-region @save="saveRegion" :region="localRegion" />
    </q-dialog>
    <q-dialog v-model="isManagingAlert">
      <manage-alert @save="saveAlert" :read-only="false" :region="localRegion" />
    </q-dialog>
  </div>
</template>

<script lang="ts">
import ManageRegion from './ManageRegion.vue';
import ManageAlert from './ManageAlert.vue'
import { Alert, Region } from 'src/components/models';
import TableHeader from 'src/components/TableHeader.vue'
import Vue from 'vue';

export default Vue.extend({
  name: 'RegionTable',
  props: {
    readOnly: {
      type: Boolean
    }
  },
  mounted() {
    this.componentReady = true;
    this.regions = [
      {
        name: 'Montreal'
      }
    ]
    this.loading = false;
  },
  data() {
    return {
      componentReady: false,
      regions: [] as Region[],
      localRegion: {} as Region,
      isManagingAlert: false,
      isManagingRegion: false,
      loading: true,
      columns: [
        {
          name: 'Name',
          required: true,
          label: 'Name',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: Region) => row.name,
          sortable: true
        }
      ]
    };
  },
  methods: {
    saveRegion(region: Region) {
      console.log(region)
      this.isManagingRegion = false
    },
    editRegion(row: Region) {
      this.localRegion = row;
      console.log(this.localRegion);
      this.isManagingRegion = true;
    },
    deleteRegion(row: Region) {
      this.localRegion = row;
      console.log(row);
    },
    setAlertForRegion(row: Region) {
      this.localRegion = row;
      this.isManagingAlert = true
    },
    saveAlert(alert: Alert){
      console.log(alert)
    }
  },
  components: {
    TableHeader,
    ManageRegion,
    ManageAlert
  }
});
</script>

ManagePerson
