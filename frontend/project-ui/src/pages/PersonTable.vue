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
              @click="viewPeopleAtAddress(props.row)"
              icon="map"
              ><q-tooltip>View People at this address</q-tooltip></q-btn
            >
            <q-btn
              flat
              color="primary"
              dense
              @click="viewSurvey(props.row)"
              icon="summarize"
              ><q-tooltip>View Survey</q-tooltip></q-btn
            >
            <q-btn
              flat
              color="primary"
              dense
              @click="addSurvey(props.row)"
              icon="add_circle_outline"
              ><q-tooltip>Add Survey</q-tooltip></q-btn
            >
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
    <q-dialog style="min-width: 1000px" v-model="isViewingSurvey">
      <symptom :person="localPerson" />
    </q-dialog>
    <q-dialog v-model="isManagingSurvey">
      <manage-survey @save="saveSurvey" :symptoms="localSymptoms" :person="localPerson" />
    </q-dialog>
    <q-dialog v-model="isManagingPerson">
      <manage-person @save="savePerson" :person="localPerson" />
    </q-dialog>
  </div>
</template>

<script lang="ts">
import ManagePerson from 'src/components/ManagePerson.vue';
import { Person, Symptoms, SymptomSurvey } from 'src/components/models';
import TableHeader from 'src/components/TableHeader.vue';
import Vue from 'vue';
import Symptom from 'src/components/Symptom.vue';
import ManageSurvey from 'src/components/ManageSurvey.vue'

export default Vue.extend({
  name: 'PersonTable',
  props: {
    readOnly: {
      type: Boolean
    }
  },
  async mounted() {
    this.localSymptoms = {
      fever: false,
      cough: false,
      shortnessOfBreath: false,
      lossOfTaste: false,
      nausea: false,
      stomachAche: false,
      diarrhea: false,
      vomiting: false,
      headache: false,
      musclePain: false,
      soreThroat: false,
      otherSymptoms: ''
    };
    await this.$axios
      .get('/general/person/get_all/')
      .then(Response => (this.people = Response.data as Person[]));
    this.componentReady = true;
    this.loading = false;
  },
  data() {
    return {
      componentReady: false,
      people: [] as Person[],
      localPerson: {} as Person,
      localSymptoms: {} as Symptoms,
      isViewingSurvey: false,
      isManagingPerson: false,
      isManagingSurvey: false,
      isViewingAddress: false,
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
    async savePerson(person: Person) {
      console.log(this.localPerson.medicareNumber);
      if (this.localPerson.medicareNumber !== undefined) {
        await this.$axios
          .post('/general/person/edit/', person)
          .then(Response => console.log(Response.data));
      } else {
        await this.$axios
          .post('/general/person/create/', person)
          .then(Response => console.log(Response.data));
      }
      this.isManagingPerson = false;
      this.$emit('refresh');
    },
    async saveSurvey(survey: SymptomSurvey) {
      console.log(survey)
      await this.$axios
        .post('/survey/store/', survey)
        .then(Response => console.log(Response.data));
      this.isManagingSurvey = false;
    },
    viewPeopleAtAddress(row: Person){
      this.localPerson = row;
      this.isViewingAddress = true
    },
    addSurvey(row: Person) {
      this.localPerson = row;
      console.log(row);
      this.isManagingSurvey = true;
    },
    editPerson(row: Person) {
      this.localPerson = row;
      console.log(this.localPerson);
      this.isManagingPerson = true;
    },
    viewSurvey(row: Person){
      this.localPerson = row
      this.isViewingSurvey = true
    },
    async deletePerson(row: Person) {
      const data = {
        medicareNumber: row.medicareNumber
      };
      await this.$axios
        .post('/general/person/delete', data)
        .then(Response => console.log(Response.data));
    }
  },
  components: {
    TableHeader,
    ManagePerson,
    ManageSurvey,
    Symptom
  }
});
</script>

ManagePerson
