<template>
  <q-card v-if="componentReady" style="min-width: 600px" class="no-border">
    <q-card-section class="flex text-white bg-primary">
      <div class="text-h6">
        Search For Messages
      </div>
    </q-card-section>
    <q-card-section>
      <div class="person-card-flex q-gutter-sm">
        <q-input
          style="margin: 20px"
          type="date"
          v-model="startDateTime"
          dense
          outlined
          label="Start Date"
        />
        <q-input
          style="margin: 20px"
          type="date"
          v-model="endDateTime"
          dense
          outlined
          label="End Date"
        />
      </div>
    </q-card-section>
    <q-card-section>
      <q-form @submit="searchMessages">
        <div style="min-height: 50px;">
          <q-card-actions align="right">
            <q-btn label="Search" color="primary" type="submit" />
          </q-card-actions>
        </div>
      </q-form>
    </q-card-section>
    <q-card-section>
      <div v-if="hasMessages">
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
            <table-header title="Messages" :hide-add-button="true">
            </table-header>
          </template>
        </q-table>
      </div>
    </q-card-section>
  </q-card>
</template>

<script lang="ts">
import { Messages } from 'src/components/models';
import TableHeader from 'src/components/TableHeader.vue';
import Vue from 'vue';

export default Vue.extend({
  name: 'PersonTable',
  props: {
    readOnly: {
      type: Boolean
    }
  },
  mounted() {
    this.componentReady = true;
    this.loading = false;
  },
  data() {
    return {
      componentReady: false,
      startDateTime: Date,
      endDateTime: Date,
      messages: [] as Messages[],
      hasMessages: false,
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
    async searchMessages() {
      this.hasMessages = false;
      const data = {
        startDateTime: this.startDateTime,
        endDateTime: this.endDateTime
      }
      await this.$axios
        .post('/messages/', data)
        .then(Response => (this.messages = Response.data as Messages[]));
      this.hasMessages = true;
    }
  },
  components: {
    TableHeader
  }
});
</script>
