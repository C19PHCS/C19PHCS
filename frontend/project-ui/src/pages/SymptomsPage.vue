<template>
  <q-page class="row items-center justify-evenly">
    <div style="max-width: 1100px">
      <symptoms :readOnly="false"/>
    </div>
  </q-page>
</template>

<script lang="ts">
import { Meta } from 'components/models';
import { defineComponent, ref } from '@vue/composition-api';
import Symptoms from 'src/components/Symptoms.vue';

export default defineComponent({
  components: { Symptoms },
  name: 'PageIndex',
  setup() {
    const meta = ref<Meta>({
      totalCount: 1200
    });
    return { meta };
  }
});
</script>
