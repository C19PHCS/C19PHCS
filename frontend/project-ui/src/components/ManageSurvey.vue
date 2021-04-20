<template>
  <q-card v-if="componentReady" style="min-width: 600px" class="no-border">
    <q-card-section class="flex text-white bg-primary">
      <div class="text-h6">
        Manage Survey
      </div>
      <q-space />
      <q-btn flat size="sm" v-close-popup round icon="close" />
    </q-card-section>
    <q-card-section>
      <div class="person-card-flex q-gutter-sm">
        <q-input
          style="margin-bottom: 20px"
          v-model="localSurvey.medicareNumber"
          dense
          outlined
          required
          label="Medicare Number *"
        />
        <q-input
          style="margin-bottom: 20px"
          v-model="localSurvey.dateOfBirth"
          dense
          outlined
          required
          label="Date of birth *"
        />
        <q-input
          style="margin-bottom: 20px"
          v-model="localSurvey.temperature"
          type= "number"
          dense
          outlined
          required
          label="Temprature *"
        />
      </div>
      <q-separator color="primary"/>
      <div class="person-card-flex q-gutter-sm">
        <q-checkbox keep-color v-model="localSurvey.symptoms.cough" label="Cough" color="cyan" />
        <q-checkbox keep-color v-model="localSurvey.symptoms.shortnessOfBreath" label="Shortness of breath" color="cyan" />
        <q-checkbox keep-color v-model="localSurvey.symptoms.lossOfTaste" label="Loss of taste" color="cyan" />
        <q-checkbox keep-color v-model="localSurvey.symptoms.nausea" label="Nausea" color="cyan" />
        <q-checkbox keep-color v-model="localSurvey.symptoms.fever" label="Fever" color="cyan" />
        <q-checkbox keep-color v-model="localSurvey.symptoms.stomachAche" label="Stomachache" color="cyan" />
        <q-checkbox keep-color v-model="localSurvey.symptoms.diarrhea" label="Diarrhea" color="cyan" />
        <q-checkbox keep-color v-model="localSurvey.symptoms.vomiting" label="Vomitting" color="cyan" />
        <q-checkbox keep-color v-model="localSurvey.symptoms.headache" label="Headache" color="cyan" />
        <q-checkbox keep-color v-model="localSurvey.symptoms.musclePain" label="Muscle pain" color="cyan" />
        <q-checkbox keep-color v-model="localSurvey.symptoms.soreThroat" label="Sore throat" color="cyan" />
        <q-input
          style="margin-bottom: 20px"
          v-model="localSurvey.symptoms.otherSymptoms"
          dense
          outlined
          required
          label="Other Symptoms *"
        />
      </div>
    </q-card-section>
    <q-form @submit="confirmSaveSurvey">
      <div style="min-height: 50px;">
        <q-card-actions align="right">
          <q-btn flat color="primary" label="Cancel" v-close-popup />
          <q-btn label="Save" color="primary" type="submit" />
        </q-card-actions>
      </div>
    </q-form>
  </q-card>
</template>

<script lang="ts">
import Vue from 'vue';
import { Person, Symptoms, SymptomSurvey } from './models';

export default Vue.extend({
  name: 'ManageSurvey',
  mounted() {
    this.localSurvey.symptoms = this.symptoms
    this.localPerson = this.person
    this.localSurvey.medicareNumber = this.localPerson.medicareNumber
    this.componentReady = true;
  },
  data() {
    return {
      localSurvey: {} as SymptomSurvey,
      localPerson: {} as Person,
      componentReady: false
    };
  },
  props: {
    person: {
      type: Object as () => Person
    },
    symptoms: {
      type: Object as () => Symptoms
    },
    readOnly: {
      type: Boolean
    }
  },
  methods: {
    confirmSaveSurvey() {
      console.log(this.localSurvey.temperature)
      this.$emit('save', this.localSurvey)
    }
  },
  components: {}
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
    width: 63%
  }
}

.note-label {
  margin-top: 20px;
  color: rgba(0, 0, 0, 0.6);
  font-size: 14px;
}
</style>
