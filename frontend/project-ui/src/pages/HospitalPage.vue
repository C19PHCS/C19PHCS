<template>
  <q-page class="row items-center justify-evenly">
    <div style="max-width: 1400px">
      <hospital-table @refresh="refresh" :key="renderKey" :readOnly="false"/>
    </div>
  </q-page>
</template>

<script lang="ts">
import { Meta } from 'components/models';
import { defineComponent, ref } from '@vue/composition-api';
import HospitalTable from 'components/HospitalTable.vue';

export default defineComponent({
  components: { HospitalTable },
  name: 'HospitalPage',
  data() {
    return {
      renderKey: 0
    }
  },
  setup() {
    const meta = ref<Meta>({
      totalCount: 1200
    });
    return { meta };
  },
  methods: {
    refresh () {
      this.renderKey ++;
    }
  }
});
</script>
