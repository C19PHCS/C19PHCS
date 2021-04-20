<template>
  <q-card v-if="componentReady" style="min-width: 600px" class="no-border">
    <q-card-section class="flex text-white bg-primary">
      <div class="text-h6">
        Search For Symptoms
      </div>
      <q-space />
      <q-btn flat size="sm" v-close-popup round icon="close" />
    </q-card-section>
    <q-card-section>
      <div class="person-card-flex q-gutter-sm">
        <q-input
          style="margin: 20px"
          v-model="medicareNumber"
          dense
          outlined
          label="Medicare Number"
        />
        <q-input
          style="margin: 20px"
          type="date"
          v-model="date"
          dense
          outlined
          label="Date"
        />
      </div>
      <q-form @submit="searchSymptoms">
        <div style="min-height: 50px;">
          <q-card-actions align="right">
            <q-btn label="Search" color="primary" type="submit" />
          </q-card-actions>
        </div>
      </q-form>
    </q-card-section>
    <q-card-section>
      <div v-if="haveResults">
        <q-table
          dense
          flat
          bordered
          :columns="columns"
          :data="survey"
          row-key="id"
          :pagination="{ rowsPerPage: 10, sortBy: 'Date From' }"
          :loading="loading"
        >
          <template v-slot:top>
            <table-header title="Symptoms" :hide-add-button="true">
            </table-header>
          </template>
        </q-table>
      </div>
    </q-card-section>
  </q-card>
</template>

<script lang="ts">
import { Person, Survey } from 'src/components/models';
import TableHeader from 'src/components/TableHeader.vue';
import Vue from 'vue';

export default Vue.extend({
  name: 'Symptom',
  props: {
    readOnly: {
      type: Boolean
    },
    person: {
      type: Object as () => Person
    }
  },
  mounted() {
    this.localPerson = this.person;
    this.medicareNumber = this.localPerson.medicareNumber;
    console.log(this.medicareNumber);
    this.componentReady = true;
    this.loading = false;
  },
  data() {
    return {
      componentReady: false,
      medicareNumber: '',
      localPerson: {} as Person,
      haveResults: false,
      survey: [] as Survey[],
      date: Date,
      loading: true,
      columns: [
        {
          name: 'Medicare Number',
          required: true,
          label: 'Medicare Number',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: Survey) => row.medicareNumber,
          sortable: true
        },
        {
          name: 'Date',
          required: true,
          label: 'Date',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: Survey) => row.dateTime,
          sortable: true
        },
        {
          name: 'Tempreture',
          required: true,
          label: 'Tempreture',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: Survey) => row.temprature,
          sortable: true
        },
        {
          name: 'Fever',
          required: true,
          label: 'Fever',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: Survey) => (row.fever ? 'Yes' : 'No'),
          sortable: true
        },
        {
          name: 'Cough',
          required: true,
          label: 'Cough',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: Survey) => (row.cough ? 'Yes' : 'No'),
          sortable: true
        },
        {
          name: 'Shortness Of Breath',
          required: true,
          label: 'Shortness Of Breath',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: Survey) => (row.shortnessOfBreath ? 'Yes' : 'No'),
          sortable: true
        },
        {
          name: 'Loss Of Taste',
          required: true,
          label: 'Loss of Taste',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: Survey) => (row.lossOfTaste ? 'Yes' : 'No'),
          sortable: true
        },
        {
          name: 'Nausea',
          required: true,
          label: 'Nausea',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: Survey) => (row.nausea ? 'Yes' : 'No'),
          sortable: true
        },
        {
          name: 'Stomachache',
          required: true,
          label: 'Stomachache',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: Survey) => (row.stomachAche ? 'Yes' : 'No'),
          sortable: true
        },
        {
          name: 'Diarrhea',
          required: true,
          label: 'Diarrhea',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: Survey) => (row.diarrhea ? 'Yes' : 'No'),
          sortable: true
        },
        {
          name: 'Vommiting',
          required: true,
          label: 'Vomitting',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: Survey) => (row.vomiting ? 'Yes' : 'No'),
          sortable: true
        },
        {
          name: 'Headache',
          required: true,
          label: 'Headache',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: Survey) => (row.headache ? 'Yes' : 'No'),
          sortable: true
        },
        {
          name: 'Muscle Pain',
          required: true,
          label: 'Muscle Pain',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: Survey) => (row.musclePain ? 'Yes' : 'No'),
          sortable: true
        },
        {
          name: 'Sore Throat',
          required: true,
          label: 'Sore Throat',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: Survey) => (row.soreThroat ? 'Yes' : 'No'),
          sortable: true
        },
        {
          name: 'Other Symptoms',
          required: true,
          label: 'Other Symptoms',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: Survey) => row.otherSymptomes,
          sortable: true
        }
      ]
    };
  },
  methods: {
    async searchSymptoms() {
      this.haveResults = false;
      const searchCriteria = {
        medicareNumber: this.medicareNumber,
        date: this.date
      };
      await this.$axios
        .post('/survey/get/', searchCriteria)
        .then(Response => (this.survey = Response.data as Survey[]));
      console.log(this.survey);
      this.haveResults = true;
    }
  },
  components: {
    TableHeader
  }
});
</script>

<style lang="scss" scoped>
.person-card-flex {
  display: flex;
  flex-wrap: wrap;

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
