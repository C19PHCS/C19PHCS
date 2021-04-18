<template>
  <div v-if="componentReady">
    <q-table
      dense
      flat
      bordered
      :columns="columns"
      :data="people"
      row-key="id"
      :pagination="{ rowsPerPage: 10, sortBy: 'Date From' }"
      :loading="loading"
    >
      <template v-slot:top>
        <table-header
          title="People"
          @create="isManagingPerson = true"
          create-tooltip="create new person"
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
              @click="editPerson(props.row)"
              icon="edit"
              ><q-tooltip>Edit Person</q-tooltip></q-btn
            >
            <q-btn
              v-if="!readOnly"
              flat
              color="negative"
              dense
              @click="deletePerson(props.row)"
              icon="delete"
              ><q-tooltip>Delete Person</q-tooltip></q-btn
            >
          </q-td>
        </q-tr>
      </template>
    </q-table>
    <q-dialog v-model="isManagingPerson">
      <manage-person @save="savePerson" :person="localPerson" />
    </q-dialog>
  </div>
</template>

<script lang="ts">
import ManagePerson from 'src/components/ManagePerson.vue';
import { Person } from 'src/components/models';
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
    this.people = [
      {
        medicareNumber: '123abc',
        lastName: 'lastname',
        firstName: 'firstname',
        address: 'address',
        phoneNumber: 'phone',
        email: 'email',
        dateOfBirth: 'dateOFbirth',
        city: 'city',
        province: 'province'
      },
      {
        medicareNumber: '123abc2',
        lastName: 'lastname2',
        firstName: 'firstname2',
        address: 'address2',
        phoneNumber: 'phone2',
        email: 'email2',
        dateOfBirth: 'dateOFbirth2',
        city: 'city2',
        province: 'province2'
      }
    ];
    this.loading = false;
  },
  data() {
    return {
      componentReady: false,
      people: [] as Person[],
      localPerson: {} as Person,
      isManagingPerson: false,
      loading: true,
      columns: [
        {
          name: 'Medicare Number',
          required: true,
          label: 'Medicare Number',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: Person) => row.medicareNumber,
          sortable: true
        },
        {
          name: 'First Name',
          required: true,
          label: 'First Name',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: Person) => row.firstName,
          sortable: true
        },
        {
          name: 'Last Name',
          required: true,
          label: 'Last Name',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: Person) => row.lastName,
          sortable: true
        },
        {
          name: 'Date of birth',
          required: true,
          label: 'Date of birth',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: Person) => row.dateOfBirth,
          sortable: true
        },
        {
          name: 'Phone number',
          required: true,
          label: 'Phone number',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: Person) => row.phoneNumber,
          sortable: true
        },
        {
          name: 'Email address',
          required: true,
          label: 'Email address',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: Person) => row.email,
          sortable: true
        }
      ]
    };
  },
  methods: {
    savePerson(person: Person) {
      console.log(person)
      this.isManagingPerson = false
    },
    editPerson(row: Person) {
      this.localPerson = row;
      console.log(this.localPerson);
      this.isManagingPerson = true;
    },
    deletePerson(row: Person) {
      this.localPerson = row;
      console.log(row);
    }
  },
  components: {
    TableHeader,
    ManagePerson
  }
});
</script>

ManagePerson
