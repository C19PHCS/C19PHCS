<template>
  <q-card style="min-width: 1000px" class="no-border">
    <q-card-section class="flex text-white bg-primary">
      <div class="text-h6">All People living at {{ person.address }}</div>
      <q-space />
      <q-btn flat size="sm" v-close-popup round icon="close" />
    </q-card-section>
    <q-card-section>
      <div class="person-card-flex q-gutter-sm">
        <q-table
          style="min-width: 950px"
          dense
          flat
          bordered
          :columns="columns"
          :data="people"
          row-key="id"
          :pagination="{ rowsPerPage: 10, sortBy: 'Date From' }"
        >
          <template v-slot:top>
            <table-header title="People" :hide-add-button="true">
            </table-header>
          </template>
        </q-table>
      </div>
    </q-card-section>
  </q-card>
</template>

<script lang="ts">
import Vue from 'vue';
import { PeopleAtAddress, Person } from './models';
import TableHeader from 'src/components/TableHeader.vue';

export default Vue.extend({
  name: 'ViewPeopleAtAddress',
  async mounted() {
    this.localPerson = JSON.parse(
      JSON.stringify(this.person)
    ) as Person;
    this.componentReady = true;
    const address = {
      address: this.localPerson.address,
      city: this.localPerson.city,
      province: this.localPerson.province,
      postalCode: this.localPerson.postalCode,
      country: this.localPerson.country
    }
    console.log(address)
    if(address !== null){
      await this.$axios
      .post('/people-at-address/',address)
      .then(Response => (this.people = Response.data as PeopleAtAddress[]));
    }
  },
  data() {
    return {
      people: [] as PeopleAtAddress[],
      componentReady: false,
      localPerson: {} as Person,
      columns: [
        {
          name: 'Medicare Number',
          required: true,
          label: 'Medicare Number',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: PeopleAtAddress) => row.medicareNumber,
          sortable: true
        },
        {
          name: 'Date of birth',
          required: true,
          label: 'Date of birth',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: PeopleAtAddress) => row.dateOfbirth,
          sortable: true
        },
        {
          name: 'First Name',
          required: true,
          label: 'First Name',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: PeopleAtAddress) => row.firstName,
          sortable: true
        },
        {
          name: 'Last name',
          required: true,
          label: 'Last name',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: PeopleAtAddress) => row.lastName,
          sortable: true
        },
        {
          name: 'Citizenship',
          required: true,
          label: 'Citizenship',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: PeopleAtAddress) => row.citizenship,
          sortable: true
        },
        {
          name: 'Email',
          required: true,
          label: 'Email',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: PeopleAtAddress) => row.email,
          sortable: true
        },
        {
          name: 'Phone number',
          required: true,
          label: 'Phone number',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: PeopleAtAddress) => row.phoneNumber,
          sortable: true
        },
        {
          name: 'Fathers First Name',
          required: true,
          label: 'Fathers First Name',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: PeopleAtAddress) => row.fatherFirstName,
          sortable: true
        },
        {
          name: 'Fathers Last Name',
          required: true,
          label: 'Fathers Last Name',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: PeopleAtAddress) => row.fatherLastName,
          sortable: true
        },
        {
          name: 'Mothers First name',
          required: true,
          label: 'Mothers first name',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: PeopleAtAddress) => row.motherFirstName,
          sortable: true
        },
        {
          name: 'Mothers last name',
          required: true,
          label: 'Mothers last name',
          align: 'left',
          headerStyle: 'width: 17vw',
          field: (row: PeopleAtAddress) => row.motherLastName,
          sortable: true
        }
      ]
    };
  },
  props: {
    person: {
      type: Object as () => Person
    },
    readOnly: {
      type: Boolean
    }
  },
  methods: {},
  components: { TableHeader }
});
</script>

<style lang="scss" scoped>
.person-card-flex {
  display: flex;
  flex-wrap: wrap;
  min-width: 800px;

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
