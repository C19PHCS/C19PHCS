<template>
  <div v-if="componentReady">
    <q-table
      dense
      flat
      bordered
      :columns="columns"
      :data="messages"
      row-key="id"
      :pagination="{ rowsPerPage: 10, sortBy: 'Date From' }"
      :loading="loading"
    >
      <template v-slot:top>
        <table-header
          title="Messages"
          :hide-add-button="true"
        >
        </table-header>
      </template>
    </q-table>
  </div>
</template>

<script lang="ts">
import { Messages } from 'src/components/models';
import TableHeader from 'src/components/TableHeader.vue'
import Vue from 'vue';


export default Vue.extend({
  name: 'PersonTable',
  props: {
    readOnly: {
      type: Boolean
    }
    
  },
  async mounted() {
    await this.$axios
      .get('/general/message/get_all/')
      .then(Response => (this.messages = Response.data as Messages[]));
    this.componentReady = true
    this.loading = false
  },
  data() {
    return {
      componentReady: false,
      messages: [] as Messages[],
      loading: true,
      columns: [
        {
          name: 'Date',
          required: true,
          label: 'Date',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: Messages) => row.dateTime,
          sortable: true
        },
        {
          name: 'Email',
          required: true,
          label: 'Email',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: Messages) => row.email,
          sortable: true
        },
        {
          name: 'Name',
          required: true,
          label: 'Name',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: Messages) => row.name,
          sortable: true
        },
        {
          name: 'Region',
          required: true,
          label: 'Region',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: Messages) => row.region,
          sortable: true
        },
        {
          name: 'Old Alert Level',
          required: true,
          label: 'Old Alert Level',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: Messages) => row.oldAlertLevel,
          sortable: true
        },
        {
          name: 'New Alert Level',
          required: true,
          label: 'New Alert Level',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: Messages) => row.newAlertLevel,
          sortable: true
        },
        {
          name: 'Health Recomendation',
          required: true,
          label: 'Health Recomendation',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: Messages) => row.healthRecomendation,
          sortable: true
        },
        {
          name: 'Description',
          required: true,
          label: 'Description',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: Messages) => row.description,
          sortable: true
        },
        {
          name: 'Test Results',
          required: true,
          label: 'Test Results',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: Messages) => row.testResult,
          sortable: true
        }
      ]
    };
  },
  methods: {
    
  },
  components: {
    TableHeader
  }
});
</script>
