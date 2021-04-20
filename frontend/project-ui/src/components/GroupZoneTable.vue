<template>
  <div v-if="componentReady">
    <q-table
      dense
      flat
      bordered
      :columns="columns"
      :data="groupZones"
      row-key="id"
      :pagination="{ rowsPerPage: 10, sortBy: 'Date From' }"
      :loading="loading"
    >
      <template v-slot:top>
        <table-header
          title="Group Zones"
          @create="isManagingGroupZone = true"
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
              @click="editGroupZone(props.row)"
              icon="edit"
              ><q-tooltip>Edit Group Zone</q-tooltip></q-btn
            >
            <q-btn
              v-if="!readOnly"
              flat
              color="negative"
              dense
              @click="deleteGroupZone(props.row)"
              icon="delete"
              ><q-tooltip>Delete Group Zone</q-tooltip></q-btn
            >
          </q-td>
        </q-tr>
      </template>
    </q-table>
    <q-dialog v-model="isManagingGroupZone">
      <manage-group-zone @save="saveGroupZone" :group-zone="localGroupZones" />
    </q-dialog>
  </div>
</template>

<script lang="ts">
import ManageGroupZone from './ManageGroupZone.vue';
import { GroupZone } from 'src/components/models';
import TableHeader from 'src/components/TableHeader.vue'
import Vue from 'vue';

export default Vue.extend({
  name: 'GroupZoneTable',
  props: {
    readOnly: {
      type: Boolean
    }
  },
  async mounted() {
    await this.$axios
      .get('/general/groupZone/get_all/')
      .then(Response => (this.groupZones = Response.data as GroupZone[]));
      console.log(this.groupZones)
    this.componentReady = true;
    this.loading = false;
  },
  data() {
    return {
      componentReady: false,
      groupZones: [] as GroupZone[],
      localGroupZones: {} as GroupZone,
      isManagingGroupZone: false,
      loading: true,
      columns: [
        {
          name: 'Name',
          required: true,
          label: 'Name',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: GroupZone) => row.groupName,
          sortable: true
        }
      ]
    };
  },
  methods: {
    async saveGroupZone(zone: GroupZone) {
      console.log(zone)
      if (zone.groupID !== undefined) {
        await this.$axios
          .post('/general/groupZone/edit/', zone)
          .then(Response => (console.log(Response.data)));
      } else {
        zone.groupID = this.groupZones.length++
        await this.$axios
          .post('/general/groupZone/create/', zone)
          .then(Response => (console.log(Response.data)));
      }
      this.$emit('refresh')
      this.isManagingGroupZone = false
    },
    editGroupZone(row: GroupZone) {
      this.localGroupZones = row;
      console.log(this.localGroupZones);
      this.isManagingGroupZone = true;
    },
    async deleteGroupZone(row: GroupZone) {
      this.localGroupZones = row;
      const data = {
        groupID: row.groupID
      }
      await this.$axios
          .post('/general/groupZone/delete/', data)
          .then(Response => (console.log(Response.data)));
      this.$emit('refresh')
      console.log(row);
    }
  },
  components: {
    TableHeader,
    ManageGroupZone
  }
});
</script>

